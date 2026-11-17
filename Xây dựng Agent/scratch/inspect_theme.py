with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if any(k in line for k in ['btnProceedToStep3', 'btnProceedToStep4', 'btnAdvanceToStep5', 'signOffSolutions', 'approveDataCleaning', 'exportDashboardHtml', 'exportPnlHtml', 'addCustomChartToReport']):
        print(f"Line {idx+1}: {line.strip()[:100]}")
