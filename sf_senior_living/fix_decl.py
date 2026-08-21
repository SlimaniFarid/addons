import re, os
root = r'D:\AI Addons\18\sf_senior_living'
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.xml'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()
            # Fix corrupted XML declaration
            content = content.replace('<?xml version=""1.0"" encoding=""utf-8"">', '<?xml version="1.0" encoding="utf-8"?>')
            content = content.replace('<?xml version=""1.0"" encoding=""utf-8""?>', '<?xml version="1.0" encoding="utf-8"?>')
            # Fix any remaining doubled quotes in declaration
            content = re.sub(r'<\?xml version=""""([^""]*)"" encoding=""""([^""]*)""\?>', r'<?xml version="\1" encoding="\2"?>', content)
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print(f'Fixed: {f}')