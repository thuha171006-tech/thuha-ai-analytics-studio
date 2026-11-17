with open('ui/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1350, 1375):
    print(f"L{i+1}: {lines[i].rstrip()}")
