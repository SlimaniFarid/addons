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
    
    # Restore corrupted tags
    content = content.replace('&LT_PROTECTED;', '<')
    content = content.replace('&GT_PROTECTED;', '>')
    content = content.replace('&AMP_PROTECTED;', '&')
    content = content.replace('&QUOT_PROTECTED;', '"')
    content = content.replace('&APOS_PROTECTED;', '&apos;')
    
    # Now properly escape unescaped &
    def replace_amp(match):
        text = match.group(0)
        if re.match(r'^&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);$', text):
            return text
        return '&'
    
    content = re.sub(r'&(?!([a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)', '&', content)
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)