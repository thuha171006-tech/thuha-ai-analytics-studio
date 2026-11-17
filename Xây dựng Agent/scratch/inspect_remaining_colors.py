with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '#75BFB2' in l and any(k in l for k in ['<button', '<a ', 'onclick', 'border', 'badge']):
        print(f"Line {i+1}: {l.strip()[:90]}")
