# Surgical fix for known problematic lines

import re

# Specific fixes for each file
fixes = {
    r'D:\AI Addons\18\sf_senior_living\report\report_care_plan.xml': [
        (r'<div t-out="doc\.objectives or "<p>Aucun objectif d', 
         '<div t-out="doc.objectives or \'<p>Aucun objectif d'),
        (r'<p>Aucun objectif défini</p>""',
         '<p>Aucun objectif d\u00e9fini</p>\''),
    ],
    r'D:\AI Addons\18\sf_senior_living\report\report_activity_planning.xml': [
        (r'<h4><t t-esc="day_name""/> <t t-esc="day_date\.strftime',
         '<h4><t t-esc="day_name"/> <t t-esc="day_date.strftime'),
    ],
    r'D:\AI Addons\18\sf_senior_living\report\report_ars_compliance.xml': [
        (r'<p><t t-esc="doc\.name"',
         '<p><t t-esc="doc.name"'),
    ],
    r'D:\AI Addons\18\sf_senior_living\report\report_weekly_menu.xml': [
        (r'<h4><t t-esc="day_name"',
         '<h4><t t-esc="day_name"'),
    ],
}

for f, file_fixes in fixes.items():
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    for pattern, replacement in file_fixes:
        content = re.sub(pattern, replacement, content)
    
    # Also globally fix any remaining t-out with inner "
    def fix_tout(match):
        full = match.group(0)
        # Extract value between first and last quote
        first = full.find('"')
        last = full.rfind('"')
        if first != -1 and last > first:
            before = full[:first+1]
            val = full[first+1:last]
            after = full[last:]
            val = val.replace('"', '"')
            return before + val + after
        return full
    
    content = re.sub(r't-out="[^"]*"', fix_tout, content)
    content = re.sub(r"t-out='[^']*'", fix_tout, content)
    
    # Protect & entities
    content = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', 
                     lambda m: m.group(0).replace('&', '&PROTECTED_AMP;'), content)
    content = content.replace('&', '&')
    content = content.replace('&PROTECTED_AMP;', '&')
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print('Fixed: ' + f)