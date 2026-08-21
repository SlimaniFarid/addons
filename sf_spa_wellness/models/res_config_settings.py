from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    slot_duration_minutes = fields.Integer(
        string='Default Slot Duration (min)',
        config_parameter='sf_spa_wellness.slot_duration_minutes',
        default=30,
    )
    no_show_policy = fields.Selection([
        ('0', 'No Charge (0%)'),
        ('50', 'Half Price (50%)'),
        ('100', 'Full Price (100%)'),
    ], string='No-Show Policy', config_parameter='sf_spa_wellness.no_show_policy', default='50')
    free_cancellation_hours = fields.Integer(
        string='Free Cancellation (hours)',
        config_parameter='sf_spa_wellness.free_cancellation_hours',
        default=24,
    )
    default_monthly_credits = fields.Float(
        string='Default Monthly Credits',
        config_parameter='sf_spa_wellness.default_monthly_credits',
        default=4.0,
    )
    income_account_service_id = fields.Many2one(
        'account.account',
        string='Income Account - Services',
        config_parameter='sf_spa_wellness.income_account_service_id',
        domain="[('account_type', '=', 'income')]",
    )
    income_account_package_id = fields.Many2one(
        'account.account',
        string='Income Account - Packages',
        config_parameter='sf_spa_wellness.income_account_package_id',
        domain="[('account_type', '=', 'income')]",
    )
    income_account_cure_id = fields.Many2one(
        'account.account',
        string='Income Account - Cures',
        config_parameter='sf_spa_wellness.income_account_cure_id',
        domain="[('account_type', '=', 'income')]",
    )
    income_account_membership_id = fields.Many2one(
        'account.account',
        string='Income Account - Memberships',
        config_parameter='sf_spa_wellness.income_account_membership_id',
        domain="[('account_type', '=', 'income')]",
    )
    income_account_retail_id = fields.Many2one(
        'account.account',
        string='Income Account - Retail',
        config_parameter='sf_spa_wellness.income_account_retail_id',
        domain="[('account_type', '=', 'income')]",
    )
    sale_journal_id = fields.Many2one(
        'account.journal',
        string='Default Sales Journal',
        config_parameter='sf_spa_wellness.sale_journal_id',
        domain="[('type', '=', 'sale')]",
    )
    membership_credit_reset_day = fields.Integer(
        string='Membership Credit Reset Day',
        config_parameter='sf_spa_wellness.membership_credit_reset_day',
        default=1,
    )
    reevaluation_frequency_months = fields.Integer(
        string='Re-evaluation Frequency (months)',
        config_parameter='sf_spa_wellness.reevaluation_frequency_months',
        default=3,
    )