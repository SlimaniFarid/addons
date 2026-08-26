from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaPackageSession(models.Model):
    _name = 'sf.spa.package.session'
    _description = 'Package Session'
    _inherit = ['sf.spa.company.mixin']

    package_id = fields.Many2one('sf.spa.service', string='Package', required=True, ondelete='cascade', domain=[('is_package', '=', True)])
    service_id = fields.Many2one('sf.spa.service', string='Included Service', required=True, domain=[('is_package', '=', False), ('is_cure', '=', False)])
    quantity = fields.Integer(string='Quantity', default=1)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_('Quantity must be positive.'))

    @api.constrains('package_id', 'service_id')
    def _check_not_self(self):
        for record in self:
            if record.package_id == record.service_id:
                raise ValidationError(_('A package cannot include itself.'))