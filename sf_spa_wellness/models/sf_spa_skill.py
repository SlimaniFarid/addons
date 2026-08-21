from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaSkill(models.Model):
    _name = 'sf.spa.skill'
    _description = 'Spa Skill'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.skill'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    category = fields.Selection([
        ('massage', 'Massage'),
        ('hydrotherapy', 'Hydrotherapy'),
        ('aesthetic', 'Aesthetic'),
        ('kinesiotherapy', 'Kinesiotherapy'),
        ('wellness_coach', 'Wellness Coach'),
        ('other', 'Other'),
    ], string='Category', required=True)
    description = fields.Text(string='Description')
    therapist_ids = fields.Many2many(
        'sf.spa.therapist',
        'sf_spa_therapist_skill_rel',
        'skill_id',
        'therapist_id',
        string='Therapists'
    )
    service_ids = fields.Many2many(
        'sf.spa.service',
        'sf_spa_service_skill_rel',
        'skill_id',
        'service_id',
        string='Services Requiring This Skill'
    )

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.category:
                name = f'[{record.category}] {name}'
            result.append((record.id, name))
        return result