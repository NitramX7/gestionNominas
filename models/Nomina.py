from odoo import api, fields, models


class Nomina(models.Model):
    _name = 'gestion.nomina'
    _description = 'Nómina'
    _order = 'fecha desc, id desc'

    name = fields.Char(string='Referencia', copy=False, default='Nueva')
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        related='company_id.currency_id',
        store=True,
        readonly=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
    )
    sueldo_base = fields.Monetary(
        string='Sueldo base',
        currency_field='currency_id',
        required=True,
    )
    linea_ids = fields.One2many(
        'gestion.nomina.linea',
        'nomina_id',
        string='Bonificaciones y deducciones',
    )
    irpf_porcentaje = fields.Float(string='IRPF (%)', digits=(16, 2))
    irpf_pagado = fields.Monetary(
        string='IRPF pagado',
        currency_field='currency_id',
        compute='_compute_totales',
        store=True,
    )
    total_bonificaciones = fields.Monetary(
        string='Total bonificaciones',
        currency_field='currency_id',
        compute='_compute_totales',
        store=True,
    )
    total_deducciones = fields.Monetary(
        string='Total deducciones',
        currency_field='currency_id',
        compute='_compute_totales',
        store=True,
    )
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    justificante_pdf = fields.Binary(
        string='Justificante PDF',
        attachment=True,
        help='Documento PDF con el justificante de la transferencia.',
    )
    state = fields.Selection(
        [
            ('draft', 'Redactada'),
            ('confirm', 'Confirmada'),
            ('paid', 'Pagada'),
        ],
        string='Estado',
        default='draft',
    )

    @api.depends('linea_ids.monto', 'linea_ids.tipo', 'sueldo_base', 'irpf_porcentaje')
    def _compute_totales(self):
        for record in self:
            bonus = sum(record.linea_ids.filtered(lambda l: l.tipo == 'bonus').mapped('monto'))
            deduction = sum(record.linea_ids.filtered(lambda l: l.tipo == 'deduction').mapped('monto'))
            record.total_bonificaciones = bonus
            record.total_deducciones = deduction
            base_irpf = record.sueldo_base + bonus
            record.irpf_pagado = base_irpf * (record.irpf_porcentaje / 100.0) if record.irpf_porcentaje else 0.0


class NominaLinea(models.Model):
    _name = 'gestion.nomina.linea'
    _description = 'Línea de bonificación o deducción'

    nomina_id = fields.Many2one(
        'gestion.nomina',
        string='Nómina',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Concepto', required=True)
    tipo = fields.Selection(
        [('bonus', 'Bonificación'), ('deduction', 'Deducción')],
        string='Tipo',
        required=True,
        default='bonus',
    )
    monto = fields.Monetary(
        string='Importe',
        currency_field='currency_id',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        related='nomina_id.currency_id',
        store=True,
        readonly=True,
    )
