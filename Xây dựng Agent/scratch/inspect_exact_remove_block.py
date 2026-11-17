with open('ui/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1370, min(1500, len(lines))):
    print(f"L{i+1}: {repr(lines[i])}")
