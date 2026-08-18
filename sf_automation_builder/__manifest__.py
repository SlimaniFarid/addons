{
    'name': 'Visual No-Code Automation Builder',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Zapier-like visual builder: triggers → actions → conditions for Odoo models + external APIs',
    'description': """Visual No-Code Automation Builder
=================================

Native "Zapier for Odoo" - no code, fully visual.

Canvas:
- Drag-and-drop nodes (React Flow / Vue Flow based)
- Triggers: record create/update/delete, field change, cron, webhook, email, API call, manual
- Actions: create/update/search records, send email, HTTP request, run Python, call AI, webhook
- Logic: conditions (if/else), loops (for each), delays, formatters, code snippet
- Variables: pass data between nodes (JSON path, Jinja2 templates)
- Error handling: retry, fallback branch, notification

Connectors (built-in):
- Odoo ORM (any model)
- HTTP/REST (auth: bearer, basic, OAuth2, API key)
- Email (SMTP, templates)
- AI (OpenAI, Claude, Gemini, Mistral - BYOK)
- Webhooks (incoming/outgoing)
- File storage (local, S3, Azure Blob)

Governance:
- Version control (draft/published/archived)
- Execution logs with input/output/errors
- Rate limiting, quota per automation
- Role-based access (who can create/edit/run)
- Audit trail

Deployment:
- Runs asynchronously via queue_job (if installed) or cron
- Manual test run with sample data
- Import/export JSON for backup/sharing

No Python knowledge required. Power users can add custom JS/Python snippets.""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 349.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'web'],
    'depends_optional': ['queue_job'],
    'data': [
        'security/ir.model.access.csv',
        'views/automation_menus.xml',
        'views/automation_flow_views.xml',
        'views/automation_node_views.xml',
        'views/automation_log_views.xml',
        'data/automation_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


