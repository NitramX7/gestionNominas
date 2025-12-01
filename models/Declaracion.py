from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Declaracion(models.Model):
    _name = 'gestion.declaracion'
    _description = 'Declaracion de renta anual'
    _order = 'anio desc, employee_id'

    name = fields.Char(string='Referencia', copy=False, default='Nueva')
    company_id = fields.Many2one(
        'res.company',
        string='Compania',
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
    anio = fields.Integer(string='Anio', required=True)
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
    )
    nomina_ids = fields.Many2many(
        'gestion.nomina',
        'gestion_declaracion_nomina_rel',
        'declaracion_id',
        'nomina_id',
        string='Nominas',
        domain="[('employee_id', '=', employee_id)]",
    )
    sueldo_bruto_total = fields.Monetary(
        string='Sueldo bruto total',
        currency_field='currency_id',
        compute='_compute_totales',
        store=True,
    )
    irpf_pagado_total = fields.Monetary(
        string='IRPF pagado total',
        currency_field='currency_id',
        compute='_compute_totales',
        store=True,
    )

    @api.depends('nomina_ids.sueldo_base', 'nomina_ids.total_bonificaciones', 'nomina_ids.total_deducciones', 'nomina_ids.irpf_pagado')
    def _compute_totales(self):
        for record in self:
            bruto = 0.0
            irpf_total = 0.0
            for nomina in record.nomina_ids:
                bruto += (nomina.sueldo_base +
                          nomina.total_bonificaciones - nomina.total_deducciones)
                irpf_total += nomina.irpf_pagado
            record.sueldo_bruto_total = bruto
            record.irpf_pagado_total = irpf_total

    @api.constrains('nomina_ids', 'anio')
    def _check_nominas(self):
        for record in self:
            if len(record.nomina_ids) > 14:
                raise ValidationError(
                    'Una declaracion solo puede tener hasta 14 nominas.')
            for nomina in record.nomina_ids:
                if nomina.fecha and nomina.fecha.year != record.anio:
                    raise ValidationError(
                        'Todas las nominas deben pertenecer al mismo anio de la declaracion.')
