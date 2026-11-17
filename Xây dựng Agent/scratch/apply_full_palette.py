import re

# ==============================================================================
# 1. UPDATE ui/index.html
# ==============================================================================
with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace all old cream #F2E5E4 with #fde2e4
text = text.replace('#F2E5E4', '#fde2e4')

# Replace all old light mint #B8D9D3 with #c5dedd
text = text.replace('#B8D9D3', '#c5dedd')

# Replace all old dusty rose #D9A3AC with #fad2e1
text = text.replace('#D9A3AC', '#fad2e1')

# Replace remaining action buttons that still used #75BFB2 or gradients with #fad2e1
action_replacements = [
    # btnApproveCleaning
    (
        r'<button type="button" onclick="approveAllCleaningSolutions\(\)" id="btnApproveCleaning"[^>]*>',
        '<button type="button" onclick="approveAllCleaningSolutions()" id="btnApproveCleaning" class="btn-smooth px-5 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer shrink-0">'
    ),
    # generateUserCustomChart
    (
        r'<button type="button" onclick="generateUserCustomChart\(\)"[^>]*>',
        '<button type="button" onclick="generateUserCustomChart()" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer">'
    ),
    # addCustomChartToReport
    (
        r'<button type="button" onclick="addCustomChartToReport\(\)" id="btnAddCustomChartToReport"[^>]*>',
        '<button type="button" onclick="addCustomChartToReport()" id="btnAddCustomChartToReport" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl border-2 border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-2">'
    ),
    # signAndApproveSolutions / btnSignSolutions
    (
        r'<button onclick="signAndApproveSolutions\(\)" id="btnSignSolutions"[^>]*>',
        '<button onclick="signAndApproveSolutions()" id="btnSignSolutions" class="btn-smooth w-full py-3.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs sm:text-sm tracking-wide rounded-2xl shadow-md border-2 border-[#f2a8c0] flex items-center justify-center gap-2.5 cursor-pointer">'
    ),
    # exportExcel
    (
        r'<button onclick="exportExcel\(\)"[^>]*>',
        '<button onclick="exportExcel()" class="btn-smooth w-full py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs rounded-xl shadow-xs border border-[#f2a8c0] flex items-center justify-center gap-2 cursor-pointer">'
    ),
    # startNewProjectWorkflow
    (
        r'<button type="button" onclick="startNewProjectWorkflow\(\)"[^>]*>',
        '<button type="button" onclick="startNewProjectWorkflow()" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer">'
    ),
    # applyHumanControlOverrides
    (
        r'<button onclick="applyHumanControlOverrides\(\)"[^>]*>',
        '<button onclick="applyHumanControlOverrides()" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer">'
    ),
    # runAiOverviewNow
    (
        r'<button type="button" onclick="runAiOverviewNow\(\)"[^>]*>',
        '<button type="button" onclick="runAiOverviewNow()" class="btn-smooth px-5 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer">'
    ),
    # Header refresh data button
    (
        r'<button type="button" onclick="refreshDataBtn\(\)" id="btnHeaderRefresh"[^>]*>',
        '<button type="button" onclick="refreshDataBtn()" id="btnHeaderRefresh" title="Bấm để quét và phân tích lại dữ liệu" class="btn-smooth px-4 py-2 rounded-xl bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black shadow-xs flex items-center gap-2 cursor-pointer border border-[#f2a8c0]">'
    ),
    # Header upload file button
    (
        r'<button type="button" onclick="document\.getElementById\(\'appHeaderFileInput\'\)\.click\(\)"[^>]*>',
        '<button type="button" onclick="document.getElementById(\'appHeaderFileInput\').click()" title="Nạp tệp Excel hoặc CSV mới" class="btn-smooth px-4 py-2 rounded-xl bg-white hover:bg-[#fad2e1]/30 text-[#3d1825] border-2 border-[#fad2e1] text-xs font-black shadow-xs flex items-center gap-2 cursor-pointer">'
    ),
    # Save context button
    (
        r'<button type="button" onclick="saveBusinessContext\(\)"[^>]*>',
        '<button type="button" onclick="saveBusinessContext()" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl border border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-1.5">'
    )
]

for pat, rep in action_replacements:
    text = re.sub(pat, rep, text)

# Update Toast Notification Success Class to Mint
text = text.replace(
    ": (type === 'success' ? 'bg-[#203833] text-[#c5dedd]/80 border-[#75BFB2] shadow-[#75BFB2]/30'",
    ": (type === 'success' ? 'bg-[#1e3532] text-[#c5dedd] border-[#c5dedd] shadow-[#c5dedd]/30'"
)

# Replace any remaining #D991A4 with #fad2e1
text = text.replace('#D991A4', '#fad2e1')

with open(r'd:\Xây dựng Agent\ui\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("ui/index.html updated successfully!")


# ==============================================================================
# 2. UPDATE core/html_exporter.py
# ==============================================================================
with open(r'd:\Xây dựng Agent\core\html_exporter.py', 'r', encoding='utf-8') as f:
    exp_text = f.read()

exp_text = exp_text.replace('#F2E5E4', '#fde2e4')
exp_text = exp_text.replace('#B8D9D3', '#c5dedd')
exp_text = exp_text.replace('#D9A3AC', '#fad2e1')
exp_text = exp_text.replace('#D991A4', '#fad2e1')
exp_text = exp_text.replace('#75BFB2', '#c5dedd')

with open(r'd:\Xây dựng Agent\core\html_exporter.py', 'w', encoding='utf-8') as f:
    f.write(exp_text)

print("core/html_exporter.py updated successfully!")
