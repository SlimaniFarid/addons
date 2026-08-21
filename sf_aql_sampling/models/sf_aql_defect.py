# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfAqlDefect(models.Model):
    _name = 'sf.aql.defect'
    _description = 'AQL Defect'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id asc'

    inspection_id = fields.Many2one('sf.aql.inspection', string='Inspection',
                                    required=True, ondelete='cascade', index=True)
    defect_code = fields.Char(string='Defect Code')
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Severity', required=True, default='minor')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_quantity_positive',
         'CHECK (quantity > 0)',
         'The defect quantity must be greater than zero.'),
    ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for defect in self:
            if defect.quantity <= 0:
                raise ValidationError(_('The defect quantity must be greater than zero.'))

    def _check_editable(self):
        self.ensure_one()
        if self.inspection_id.state in ('released', 'rejected', 'cancelled'):
            raise UserError(_('A finished inspection cannot be modified.'))

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('inspection_id'):
                parent = self.env['sf.aql.inspection'].browse(vals['inspection_id'])
                if parent.state in ('released', 'rejected', 'cancelled'):
                    raise UserError(_('A finished inspection cannot be modified.'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._check_editable()
        return super().write(vals)

    def unlink(self):
        for record in self:
            record._check_editable()
        return super().unlink()