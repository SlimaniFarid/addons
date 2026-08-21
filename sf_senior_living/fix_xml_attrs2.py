import re, os
root = r'D:\AI Addons\18\sf_senior_living'
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.xml'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as fp:
                lines = fp.readlines()
            new_lines = []
            for line in lines:
                # Skip XML declaration line
                if line.lstrip().startswith('<?xml'):
                    new_lines.append(line)
                    continue
                # Fix single quotes in attribute values
                def fix_attr(m):
                    attr = m.group(1)
                    val = m.group(2)
                    val = val.replace("'", '&apos;')
                    return attr + '="' + val + '"'
                line = re.sub(r'(\w+)=("([^"]*)")', fix_attr, line)
                new_lines.append(line)
            with open(path, 'w', encoding='utf-8') as fp:
                fp.writelines(new_lines)
            print('Fixed: ' + os.path.basename(path))