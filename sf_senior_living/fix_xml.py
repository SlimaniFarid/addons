import re

files_to_fix = [
    r'D:\AI Addons\18\sf_senior_living\security\sf_senior_living_security.xml',
    r'D:\AI Addons\18\sf_senior_living\views\menu_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_activity_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_contract_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_nursing_note_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_resident_views.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_activity_planning.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_ars_compliance.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_care_plan.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_weekly_menu.xml',
]

for f in files_to_fix:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Replace unescaped & with & but preserve existing entities
    # First, protect already escaped entities
    content = content.replace('<', '&LT_PROTECTED;')
    content = content.replace('>', '&GT_PROTECTED;')
    content = content.replace('&', '&AMP_PROTECTED;')
    content = content.replace('"', '&QUOT_PROTECTED;')
    content = content.replace('&apos;', '&APOS_PROTECTED;')
    # Protect numeric entities
    content = re.sub(r'&#x[0-9a-fA-F]+;', lambda m: m.group(0).replace('&', '&AMP_PROTECTED;'), content)
    content = re.sub(r'&#[0-9]+;', lambda m: m.group(0).replace('&', '&AMP_PROTECTED;'), content)
    
    # Now replace remaining bare &
    content = content.replace('&', '&')
    
    # Restore protected
    content = content.replace('&LT_PROTECTED;', '<')
    content = content.replace('&GT_PROTECTED;', '>')
    content = content.replace('&AMP_PROTECTED;', '&')
    content = content.replace('&QUOT_PROTECTED;', '"')
    content = content.replace('&APOS_PROTECTED;', '&apos;')
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)