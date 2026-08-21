from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Senior Living Configuration
    sf_senior_gir_alert_days = fields.Integer(
        string='GIR Alert Days Before',
        default=30,
        config_parameter='sf_senior_living.gir_alert_days',
    )
    sf_senior_gir_alert_days_urgent = fields.Integer(
        string='GIR Urgent Alert Days Before',
        default=7,
        config_parameter='sf_senior_living.gir_alert_days_urgent',
    )
    sf_senior_pps_alert_days = fields.Integer(
        string='PPS Alert Days Before',
        default=60,
        config_parameter='sf_senior_living.pps_alert_days',
    )
    sf_senior_care_fee_monthly = fields.Monetary(
        string='Default Monthly Care Fee',
        currency_field='company_currency_id',
        config_parameter='sf_senior_living.care_fee_monthly',
    )
    sf_senior_service_fee_monthly = fields.Monetary(
        string='Default Monthly Service/Activity Fee',
        currency_field='company_currency_id',
        config_parameter='sf_senior_living.service_fee_monthly',
    )
    sf_senior_max_room_reservation_days = fields.Integer(
        string='Max Room Reservation Days',
        default=30,
        config_parameter='sf_senior_living.max_room_reservation_days',
    )
    sf_senior_medical_portal_consent = fields.Boolean(
        string='Require Medical Portal Consent',
        default=True,
        config_parameter='sf_senior_living.medical_portal_consent',
    )

    # Account Configuration
    sf_senior_income_account_accommodation_id = fields.Many2one(
        'account.account',
        string='Accommodation Income Account',
        domain="[('account_type', '=', 'income')]",
        config_parameter='sf_senior_living.income_account_accommodation_id',
    )
    sf_senior_income_account_dependency_id = fields.Many2one(
        'account.account',
        string='Dependency Income Account',
        domain="[('account_type', '=', 'income')]",
        config_parameter='sf_senior_living.income_account_dependency_id',
    )
    sf_senior_income_account_care_id = fields.Many2one(
        'account.account',
        string='Care Income Account',
        domain="[('account_type', '=', 'income')]",
        config_parameter='sf_senior_living.income_account_care_id',
    )
    sf_senior_income_account_service_id = fields.Many2one(
        'account.account',
        string='Service Income Account',
        domain="[('account_type', '=', 'income')]",
        config_parameter='sf_senior_living.income_account_service_id',
    )
    sf_senior_income_account_meal_id = fields.Many2one(
        'account.account',
        string='Meal Income Account',
        domain="[('account_type', '=', 'income')]",
        config_parameter='sf_senior_living.income_account_meal_id',
    )
    sf_senior_journal_id = fields.Many2one(
        'account.journal',
        string='Default Sales Journal',
        domain="[('type', '=', 'sale')]",
        config_parameter='sf_senior_living.journal_id',
    )

    # Contract Template
    sf_senior_contract_template_id = fields.Many2one(
        'ir.actions.report',
        string='Contract Template',
        domain="[('model', '=', 'sf.senior.contract')]",
        config_parameter='sf_senior_living.contract_template_id',
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )

    def set_values(self):
        super().set_values()
        # Propagate to all residences
        residences = self.env['sf.senior.residence'].search([])
        for residence in residences:
            residence.write({
                'gir_alert_days_before': self.sf_senior_gir_alert_days,
                'gir_alert_days_before_urgent': self.sf_senior_gir_alert_days_urgent,
                'pps_alert_days_before': self.sf_senior_pps_alert_days,
                'care_fee_monthly': self.sf_senior_care_fee_monthly,
                'service_fee_monthly': self.sf_senior_service_fee_monthly,
                'max_room_reservation_days': self.sf_senior_max_room_reservation_days,
                'medical_portal_consent': self.sf_senior_medical_portal_consent,
                'income_account_accommodation_id': self.sf_senior_income_account_accommodation_id.id,
                'income_account_dependency_id': self.sf_senior_income_account_dependency_id.id,
                'income_account_care_id': self.sf_senior_income_account_care_id.id,
                'income_account_service_id': self.sf_senior_income_account_service_id.id,
                'income_account_meal_id': self.sf_senior_income_account_meal_id.id,
                'journal_id': self.sf_senior_journal_id.id,
                'contract_template_id': self.sf_senior_contract_template_id.id,
            })

    @api.model
    def get_values(self):
        res = super().get_values()
        # Get from first residence or defaults
        residence = self.env['sf.senior.residence'].search([], limit=1)
        if residence:
            res.update({
                'sf_senior_gir_alert_days': residence.gir_alert_days_before,
                'sf_senior_gir_alert_days_urgent': residence.gir_alert_days_before_urgent,
                'sf_senior_pps_alert_days': residence.pps_alert_days_before,
                'sf_senior_care_fee_monthly': residence.care_fee_monthly,
                'sf_senior_service_fee_monthly': residence.service_fee_monthly,
                'sf_senior_max_room_reservation_days': residence.max_room_reservation_days,
                'sf_senior_medical_portal_consent': residence.medical_portal_consent,
                'sf_senior_income_account_accommodation_id': residence.income_account_accommodation_id.id,
                'sf_senior_income_account_dependency_id': residence.income_account_dependency_id.id,
                'sf_senior_income_account_care_id': residence.income_account_care_id.id,
                'sf_senior_income_account_service_id': residence.income_account_service_id.id,
                'sf_senior_income_account_meal_id': residence.income_account_meal_id.id,
                'sf_senior_journal_id': residence.journal_id.id,
                'sf_senior_contract_template_id': residence.contract_template_id.id,
            })
        return res