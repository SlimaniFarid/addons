import re, os
root = r'D:\AI Addons\18\sf_senior_living'
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.xml'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()
            def fix_attr(m):
                full = m.group(0)
                if full.startswith('<?xml'):
                    return full
                attr = m.group(1)
                val = m.group(2)
                val = val.replace("'", '&apos;')
                return attr + '="' + val + '"'
            content = re.sub(r'(\w+)=("([^"]*)")', fix_attr, content)
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print('Fixed: ' + os.path.basename(path))