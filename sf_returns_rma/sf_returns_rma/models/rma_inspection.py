from odoo import api, fields, models


class RMAInspection(models.Model):
    _name = 'rma.inspection'
    _description = 'RMA Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rma_id = fields.Many2one('rma.request', string='RMA Request', required=True, ondelete='cascade')
    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda s: s.env.user)
    inspection_date = fields.Date(string='Inspection Date', default=fields.Date.today)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ], string='Status', default='pending', tracking=True)

    line_ids = fields.One2many('rma.inspection.line', 'inspection_id', string='Inspection Lines')
    overall_condition = fields.Selection([
        ('new', 'New/Unopened'),
        ('like_new', 'Like New'),
        ('used', 'Used - Good'),
        ('worn', 'Worn'),
        ('damaged', 'Damaged'),
        ('missing_parts', 'Missing Parts'),
    ], string='Overall Condition')

    disposition_recommendation = fields.Selection([
        ('restock', 'Restock as New'),
        ('repack', 'Repack & Restock'),
        ('repair', 'Send to Repair'),
        ('refurbish', 'Refurbish'),
        ('scrap', 'Scrap'),
        ('return_vendor', 'Return to Vendor'),
    ], string='Recommendation')

    notes = fields.Text(string='Notes')
    photos = fields.Many2many('ir.attachment', string='Photos')

    def action_complete(self):
        for insp in self:
            insp.state = 'done'
            insp.rma_id.write({'state': 'dispositioned'})
            # Create disposition based on recommendation
            disp = self.env['rma.disposition'].create({
                'rma_id': insp.rma_id.id,
                'inspection_id': insp.id,
                'action': insp.disposition_recommendation,
            })
            insp.rma_id.disposition_id = disp.id


class RMAInspectionLine(models.Model):
    _name = 'rma.inspection.line'
    _description = 'Inspection Line'

    inspection_id = fields.Many2one('rma.inspection', string='Inspection', required=True, ondelete='cascade')
    rma_line_id = fields.Many2one('rma.line', string='RMA Line', required=True)
    product_id = fields.Many2one(related='rma_line_id.product_id', store=True)

    condition = fields.Selection([
        ('new', 'New/Unopened'),
        ('like_new', 'Like New'),
        ('used', 'Used - Good'),
        ('worn', 'Worn'),
        ('damaged', 'Damaged'),
        ('missing_parts', 'Missing Parts'),
    ], string='Condition', required=True)

    working = fields.Boolean(string='Functional')
    missing_accessories = fields.Boolean(string='Missing Accessories')
    packaging_intact = fields.Boolean(string='Packaging Intact')
    notes = fields.Char(string='Notes')