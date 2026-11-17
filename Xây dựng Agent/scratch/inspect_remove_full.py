with open('ui/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1354, min(1495, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
