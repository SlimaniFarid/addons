import re

# This script manually fixes the specific problematic t-out lines

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
    
    # Fix 1: t-out="... "..." "..." - escape inner double quotes as "
    # Pattern: t-out="[^"]*"([^"]*)"[^"]*"
    # We need to find all double quotes inside t-out attributes and escape them
    def fix_tout_attrs(match):
        # match.group(0) is the full t-out attribute
        attr = match.group(0)
        # Find the value part (between first " and last ")
        first_quote = attr.find('"')
        last_quote = attr.rfind('"')
        if first_quote != -1 and last_quote > first_quote:
            before = attr[:first_quote+1]
            value = attr[first_quote+1:last_quote]
            after = attr[last_quote:]
            # Escape inner double quotes
            value = value.replace('"', '"')
            return before + value + after
        return attr
    
    # Apply fix to all t-out attributes
    content = re.sub(r't-out="[^"]*(?:"[^"]*)*"', fix_tout_attrs, content)
    
    # Fix 2: Also fix single-quoted t-out attributes
    def fix_tout_single(match):
        attr = match.group(0)
        first_quote = attr.find("'")
        last_quote = attr.rfind("'")
        if first_quote != -1 and last_quote > first_quote:
            before = attr[:first_quote+1]
            value = attr[first_quote+1:last_quote]
            after = attr[last_quote:]
            # Escape inner single quotes
            value = value.replace("'", "&apos;")
            # Also escape inner double quotes
            value = value.replace('"', '"')
            return before + value + after
        return attr
    
    content = re.sub(r"t-out='[^']*(?:'[^']*)*'", fix_tout_single, content)
    
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