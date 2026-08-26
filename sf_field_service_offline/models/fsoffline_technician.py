from odoo import api, fields, models
from odoo.exceptions import UserError


class FSOfflineTechnician(models.Model):
    _name = 'fsoffline.technician'
    _description = 'Field Service Offline Technician'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', ondelete='set null')
    active = fields.Boolean(default=True)

    # Device info
    device_id = fields.Char(string='Device ID', help='Unique device identifier')
    device_model = fields.Char(string='Device Model')
    device_os = fields.Char(string='OS Version')
    app_version = fields.Char(string='App Version')

    # Sync status
    last_sync = fields.Datetime(string='Last Sync', readonly=True)
    sync_status = fields.Selection([
        ('never', 'Never Synced'),
        ('ok', 'Synced'),
        ('pending', 'Pending Changes'),
        ('conflict', 'Conflicts'),
        ('error', 'Sync Error'),
    ], string='Sync Status', default='never', readonly=True)
    pending_changes = fields.Integer(string='Pending Changes', default=0)
    last_conflict = fields.Datetime(string='Last Conflict')

    # Capabilities
    has_gps = fields.Boolean(string='GPS Available', default=True)
    has_camera = fields.Boolean(string='Camera Available', default=True)
    has_barcode = fields.Boolean(string='Barcode Scanner', default=True)

    # Cache status
    cache_updated = fields.Datetime(string='Cache Updated')
    workorder_count = fields.Integer(string='Cached Work Orders')
    equipment_count = fields.Integer(string='Cached Equipment')

    def action_sync_now(self):
        for tech in self:
            tech.sync_status = 'ok'
            tech.last_sync = fields.Datetime.now()
            tech.pending_changes = 0

    def action_reset_cache(self):
        for tech in self:
            tech.workorder_count = 0
            tech.equipment_count = 0
            tech.cache_updated = fields.Datetime.now()


class FSOfflineSyncLog(models.Model):
    _name = 'fsoffline.sync.log'
    _description = 'Offline Sync Log'
    _order = 'create_date desc'

    technician_id = fields.Many2one('fsoffline.technician', string='Technician', required=True, ondelete='cascade')
    direction = fields.Selection([
        ('push', 'Push to Server'),
        ('pull', 'Pull from Server'),
    ], string='Direction', required=True)
    state = fields.Selection([
        ('started', 'Started'),
        ('success', 'Success'),
        ('partial', 'Partial Success'),
        ('failed', 'Failed'),
    ], string='Status', default='started')

    records_pushed = fields.Integer(string='Records Pushed', default=0)
    records_pulled = fields.Integer(string='Records Pulled', default=0)
    conflicts_detected = fields.Integer(string='Conflicts', default=0)
    conflict_details = fields.Text(string='Conflict Details')
    error_message = fields.Text(string='Error')
    duration_ms = fields.Integer(string='Duration (ms)')


class FSOfflineWorkOrderCache(models.Model):
    _name = 'fsoffline.workorder.cache'
    _description = 'Cached Work Order for Offline Use'

    technician_id = fields.Many2one('fsoffline.technician', string='Technician', required=True, ondelete='cascade')
    workorder_id = fields.Many2one('project.task', string='Work Order', required=True, ondelete='cascade')
    cached_data = fields.Text(string='Cached Data (JSON)')
    cached_at = fields.Datetime(string='Cached At', default=fields.Datetime.now)
    is_dirty = fields.Boolean(string='Has Local Changes', default=False)
    local_version = fields.Integer(string='Local Version', default=0)
    server_version = fields.Integer(string='Server Version', default=0)