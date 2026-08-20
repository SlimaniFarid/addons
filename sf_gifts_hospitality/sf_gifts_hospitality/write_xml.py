lines = [
    b'<?xml version="1.0" encoding="utf-8"?>\r',
    b'<odoo>\r',
    b'    <template id="report_gift_register">\r',
    b'        <t t-call="web.html_container">\r',
    b'            <t t-foreach="docs" t-as="o">\r',
    b'                <t t-set="company" t-value="o.company_id or res_company"/>\r',
    b'                <t t-call="web.external_layout">\r',
    b'                    <div class="page">\r',
    b'                        <h2>Gifts & Hospitality Register</h2>\r',
    b'                        <table class="table table-sm">\r',
    b'                            <tr><th>Name</th><th>Employee</th><th>Direction</th><th>Date</th><th>Category</th><th>Value</th><th>Status</th></tr>\r',
    b'                            <tr>\r',
    b'                                <td><span t-field="o.name"/></td>\r',
    b'                                <td><span t-field="o.employee_id"/></td>\r',
    b'                                <td><span t-field="o.direction"/></td>\r',
    b'                                <td><span t-field="o.date"/></td>\r',
    b'                                <td><span t-field="o.category"/></td>\r',
    b'                                <td><span t-field="o.estimated_value"/></td>\r',
    b'                                <td><span t-field="o.state"/></td>\r',
    b'                            </tr>\r',
    b'                        </table>\r',
    b'                    </div>\r',
    b'                </t>\r',
    b'            </t>\r',
    b'        </t>\r',
    b'    </template>\r',
    b'</odoo>\r'
]
with open(r'D:\AI Addons\18\sf_gifts_hospitality\views\report_gift_register.xml', 'wb') as f:
    f.write(b'\n'.join(lines))
print('Written')