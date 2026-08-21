# Line-by-line fix for the specific problematic lines

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
        # Fix t-out attributes that contain unescaped double quotes
        # Look for: t-out="... "..." "..." (multiple double quotes)
        if 't-out="' in line and line.count('"') > 2:
            # Find the t-out attribute
            start = line.find('t-out="')
            if start != -1:
                # Find the end of the attribute (the second-to-last " before />)
                # This is tricky - let's just replace all " inside with "
                # But only between the first " after t-out= and the last " before />
                attr_start = start + len('t-out="')
                # Find the closing /> or >
                end_pos = line.find('/>', attr_start)
                if end_pos == -1:
                    end_pos = line.find('>', attr_start)
                if end_pos != -1:
                    before = line[:attr_start]
                    value = line[attr_start:end_pos]
                    after = line[end_pos:]
                    # Escape all " in value
                    value = value.replace('"', '"')
                    line = before + value + after
        
        # Also fix single-quoted t-out
        if "t-out='" in line and line.count("'") > 2:
            start = line.find("t-out='")
            if start != -1:
                attr_start = start + len("t-out='")
                end_pos = line.find('/>', attr_start)
                if end_pos == -1:
                    end_pos = line.find('>', attr_start)
                if end_pos != -1:
                    before = line[:attr_start]
                    value = line[attr_start:end_pos]
                    after = line[end_pos:]
                    value = value.replace("'", "&apos;").replace('"', '"')
                    line = before + value + after
        
        # Protect & entities
        import re
        line = re.sub(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);', 
                      lambda m: m.group(0).replace('&', '&PROTECTED_AMP;'), line)
        line = line.replace('&', '&')
        line = line.replace('&PROTECTED_AMP;', '&')
        
        new_lines.append(line)
    
    with open(f, 'w', encoding='utf-8') as fp:
        fp.writelines(new_lines)
    print('Fixed: ' + f)