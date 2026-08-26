from odoo import api, fields, models


class SpaSequenceMixin(models.AbstractModel):
    _name = 'sf.spa.sequence.mixin'
    _description = 'Spa Sequence Mixin'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence_code = self._get_sequence_code()
            if sequence_code and not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or '/'
            if 'company_id' not in vals:
                vals['company_id'] = self.env.company.id
        return super().create(vals_list)

    def _get_sequence_code(self):
        return getattr(self, '_sequence_code', None)


class SpaCompanyMixin(models.AbstractModel):
    _name = 'sf.spa.company.mixin'
    _description = 'Spa Company Mixin'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )