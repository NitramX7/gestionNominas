from odoo import fields, models


class Bonificacion(models.Model):
    _name = 'gestion.bonificacion'
    _description = 'Bonificacion o deduccion de nomina'
    _order = 'nomina_id, id'

    nomina_id = fields.Many2one(
        'gestion.nomina',
        string='Nomina',
        required=True,
        ondelete='cascade',
    )
    concepto = fields.Char(string='Concepto', required=True)
    importe_bruto = fields.Monetary(
        string='Importe bruto',
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
