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
        lines = fp.readlines()
    
    new_lines = []
    for line in lines:
        # Fix t-out attributes with inner double quotes
        # Pattern: t-out="... "..." "..." (multiple double quotes)
        # We need to escape all inner double quotes as "
        while True:
            # Find t-out=" followed by content with unescaped "
            match = re.search(r'(t-out="[^"]*)"([^"]*")', line)
            if not match:
                break
            # Found an inner "
            before = match.group(1)
            after = match.group(2)
            line = before + '"' + after
        
        # Also fix any remaining bare &
        # Protect existing entities first
        line = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', 
                      lambda m: m.group(0).replace('&', '&PROTECTED_AMP;'), line)
        line = line.replace('&', '&')
        line = line.replace('&PROTECTED_AMP;', '&')
        
        new_lines.append(line)
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.writelines(new_lines)
    print('Fixed: ' + f)