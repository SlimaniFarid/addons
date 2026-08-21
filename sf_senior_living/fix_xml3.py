import re

files_to_fix = [
    r'D:\AI Addons\18\sf_senior_living\report\report_activity_planning.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_ars_compliance.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_care_plan.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_weekly_menu.xml',
]

for f in files_to_fix:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Fix the single quote issues in t-out attributes - replace single quotes with double quotes inside
    content = content.replace("t-out=\"doc.objectives or '<p>Aucun objectif d", 't-out=\'doc.objectives or "<p>Aucun objectif d')
    content = content.replace("d\u00e9fini</p>'\"", 'd\u00e9fini</p>\"\'')
    
    # Fix other potential t-out issues
    content = content.replace("t-out=\"doc.notes or '", 't-out=\'doc.notes or "')
    content = content.replace("'\" />", '"\' />')
    
    # Fix the & issue - protect existing entities first
    def protect_entity(match):
        return match.group(0).replace('&', '&PROTECTED_AMP;')
    
    content = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', protect_entity, content)
    # Replace bare &
    content = content.replace('&', '&')
    # Restore protected
    content = content.replace('&PROTECTED_AMP;', '&')
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)