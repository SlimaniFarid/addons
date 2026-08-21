import re

# This script manually fixes the specific problematic t-out lines by rewriting them
# with proper XML escaping

files_to_fix = {
    r'D:\AI Addons\18\sf_senior_living\report\report_care_plan.xml': {
        "t-out='doc.objectives or '<p>Aucun objectif d\u00e9fini</p>''": 't-out="doc.objectives or \'<p>Aucun objectif d&eacute;fini</p>\'"',
        't-out="doc.notes or \'<p>Aucune note</p>\'"': 't-out="doc.notes or \'<p>Aucune note</p>\'"',
    },
    r'D:\AI Addons\18\sf_senior_living\report\report_activity_planning.xml': {
        "t-out='day_name + ' ' + day_date.strftime('%d/%m')'": 't-out="day_name + \' \' + day_date.strftime(\'%d/%m\')"',
        "t-out='act.name'": 't-out="act.name"',
    },
    r'D:\AI Addons\18\sf_senior_living\report\report_ars_compliance.xml': {
        't-out="doc.name"': 't-out="doc.name"',
    },
    r'D:\AI Addons\18\sf_senior_living\report\report_weekly_menu.xml': {
        "t-out='day_name + ' ' + day_date.strftime('%d/%m')'": 't-out="day_name + \' \' + day_date.strftime(\'%d/%m\')"',
        "t-out='menu.dishes or ''": 't-out="menu.dishes or \'\'"',
    },
}

for f, replacements in files_to_fix.items():
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Also protect & in the rest of the file
    content = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', 
                     lambda m: m.group(0).replace('&', '&PROTECTED_AMP;'), content)
    content = content.replace('&', '&')
    content = content.replace('&PROTECTED_AMP;', '&')
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)