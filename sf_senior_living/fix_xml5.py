import re

files_to_fix = [
    r'D:\AI Addons\18\sf_senior_living\report\report_care_plan.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_activity_planning.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_ars_compliance.xml',
    r'D:\AI Addons\18\sf_senior_living\report\report_weekly_menu.xml',
    r'D:\AI Addons\18\sf_senior_living\views\menu_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_activity_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_contract_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_nursing_note_views.xml',
    r'D:\AI Addons\18\sf_senior_living\views\sf_senior_resident_views.xml',
]

for f in files_to_fix:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Fix t-out attributes: escape inner double quotes as "
    def fix_tout(match):
        full = match.group(0)
        # Match t-out="..." and escape inner "
        val_match = re.search(r't-out="([^"]*)"', full)
        if val_match:
            val = val_match.group(1)
            val = val.replace('"', '"')
            return 't-out="' + val + '"'
        return full
    
    content = re.sub(r't-out="[^"]*"', fix_tout, content)
    
    # Also fix single-quoted t-out if any remain
    def fix_tout_single(match):
        full = match.group(0)
        val_match = re.search(r"t-out='([^']*)'", full)
        if val_match:
            val = val_match.group(1)
            val = val.replace('"', '"')
            return 't-out="' + val + '"'
        return full
    
    content = re.sub(r"t-out='[^']*'", fix_tout_single, content)
    
    # Protect existing entities
    content = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', 
                     lambda m: m.group(0).replace('&', '&PROTECTED_AMP;'), content)
    # Replace bare &
    content = content.replace('&', '&')
    # Restore protected
    content = content.replace('&PROTECTED_AMP;', '&')
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)