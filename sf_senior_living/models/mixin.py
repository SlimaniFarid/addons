from odoo import api, models, fields


class SfSeniorSequenceMixin(models.AbstractModel):
    _name = 'sf.senior.sequence.mixin'
    _description = 'Senior Living Sequence Mixin'

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
        self.ensure_one()
        sequence_map = {
            'sf.senior.residence': 'sf.senior.residence',
            'sf.senior.building': 'sf.senior.building',
            'sf.senior.room': 'sf.senior.room',
            'sf.senior.resident': 'sf.senior.resident',
            'sf.senior.contract': 'sf.senior.contract',
            'sf.senior.care_plan': 'sf.senior.care_plan',
            'sf.senior.prescription': 'sf.senior.prescription',
            'sf.senior.nursing_note': 'sf.senior.nursing_note',
            'sf.senior.gir_evaluation': 'sf.senior.gir_evaluation',
            'sf.senior.activity': 'sf.senior.activity',
            'sf.senior.meal_regime': 'sf.senior.meal_regime',
            'sf.senior.menu': 'sf.senior.menu',
            'sf.senior.meal_order': 'sf.senior.meal_order',
            'sf.senior.invoice_line': 'sf.senior.invoice_line',
            'sf.senior.family_message': 'sf.senior.family_message',
        }
        return sequence_map.get(self._name)


class SfSeniorCompanyMixin(models.AbstractModel):
    _name = 'sf.senior.company.mixin'
    _description = 'Senior Living Company Mixin'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )