import re

with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# -------------------------------------------------------------
# 1. ACTION BUTTONS: Màu hồng #fad2e1, chữ #3d1825, viền #f2a8c0
# -------------------------------------------------------------

# Step 1 Action Box button ("LÀM SẠCH TỆP ➔")
text = re.sub(
    r'<button type="button" onclick="advanceFromStep1ToStep2\(\)" class="btn-smooth px-4 py-2 bg-gradient-to-r from-\[#203833\] to-\[#2E544C\][^"]*"',
    r'<button type="button" onclick="advanceFromStep1ToStep2()" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] text-xs font-black rounded-xl shadow-xs shrink-0 cursor-pointer border-2 border-[#f2a8c0]"',
    text
)

# Step 1 Advance Button ("SANG BƯỚC 2: QUÉT & LÀM SẠCH DỮ LIỆU")
text = re.sub(
    r'<button type="button" id="btnAdvanceToStep2" onclick="advanceFromStep1ToStep2\(\)" class="btn-smooth px-6 py-2\.5 bg-gradient-to-r from-\[#203833\] via-\[#2A4C45\] to-\[#75BFB2\][^"]*"',
    r'<button type="button" id="btnAdvanceToStep2" onclick="advanceFromStep1ToStep2()" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer"',
    text
)

# Step 1 Google Sheet "Nạp Link" Button
text = re.sub(
    r'<button type="button" onclick="loadFromGSheetUrl\(\)" class="btn-smooth px-4 py-2 bg-\[#203833\][^"]*"',
    r'<button type="button" onclick="loadFromGSheetUrl()" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] text-xs font-black rounded-xl shadow-xs flex items-center gap-1.5 cursor-pointer border border-[#f2a8c0]"',
    text
)

# Step 2 Approve Cleaning Button ("ĐỒNG Ý VỚI CÁC HƯỚNG GIẢI QUYẾT LÀM SẠCH")
text = re.sub(
    r'<button type="button" onclick="approveDataCleaning\(\)" class="btn-smooth w-full py-3\.5 [^"]*"',
    r'<button type="button" onclick="approveDataCleaning()" class="btn-smooth w-full py-3.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs sm:text-sm tracking-wide rounded-2xl shadow-md border-2 border-[#f2a8c0] flex items-center justify-center gap-2.5 cursor-pointer"',
    text
)

# Step 2 Proceed to Step 3 ("TIẾP TỤC SANG BƯỚC 3: PHÂN TÍCH CHUYÊN SÂU ➔")
text = re.sub(
    r'<button type="button" onclick="confirmCleanedDataAndProceed\(\)" id="btnProceedToStep3" class="btn-smooth px-6 py-2\.5 [^"]*"',
    r'<button type="button" onclick="confirmCleanedDataAndProceed()" id="btnProceedToStep3" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer"',
    text
)

# Step 3 Proceed to Step 4 ("SANG BƯỚC 4: KẾT QUẢ & ĐỀ XUẤT GIẢI PHÁP")
text = re.sub(
    r'<button type="button" onclick="advanceFromStep3ToStep4\(\)" class="btn-smooth w-full sm:w-auto px-6 py-2\.5 rounded-xl [^"]*"',
    r'<button type="button" onclick="advanceFromStep3ToStep4()" class="btn-smooth w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs shadow-md border-2 border-[#f2a8c0] flex items-center justify-center gap-2 cursor-pointer"',
    text
)

# Step 3 Add Custom Chart Button
text = re.sub(
    r'<button type="button" onclick="addCustomChartToReport\(\)" id="btnAddCustomChartToReport" class="btn-smooth px-4 py-2 [^"]*"',
    r'<button type="button" onclick="addCustomChartToReport()" id="btnAddCustomChartToReport" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] text-xs font-black rounded-xl border border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-2"',
    text
)

# Step 4 Sign-Off Button ("XÁC NHẬN ĐÃ RÀ SOÁT VÀ PHÊ DUYỆT HỆ THỐNG GIẢI PHÁP HÀNH ĐỘNG")
text = re.sub(
    r'<button type="button" onclick="signOffSolutions\(\)" class="btn-smooth w-full py-3\.5 [^"]*"',
    r'<button type="button" onclick="signOffSolutions()" class="btn-smooth w-full py-3.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs sm:text-sm tracking-wide rounded-2xl shadow-md border-2 border-[#f2a8c0] flex items-center justify-center gap-2.5 cursor-pointer"',
    text
)

# Step 4 Advance to Step 5 ("SANG BƯỚC 5: XEM BÁO CÁO KẾT QUẢ & XUẤT TỆP")
text = re.sub(
    r'<button type="button" onclick="advanceFromStep4ToStep5\(\)" class="btn-smooth px-6 py-2\.5 [^"]*"',
    r'<button type="button" onclick="advanceFromStep4ToStep5()" class="btn-smooth px-6 py-2.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer"',
    text
)

# Step 5 Export Buttons (Dashboard, PnL, Print)
text = re.sub(
    r'<button type="button" onclick="exportDashboardHtml\(\)" class="btn-smooth px-4 py-2 [^"]*"',
    r'<button type="button" onclick="exportDashboardHtml()" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] text-xs font-black rounded-xl border border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-1.5"',
    text
)
text = re.sub(
    r'<button type="button" onclick="exportPnlHtml\(\)" class="btn-smooth px-4 py-2 [^"]*"',
    r'<button type="button" onclick="exportPnlHtml()" class="btn-smooth px-4 py-2 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] text-xs font-black rounded-xl border border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-1.5"',
    text
)
text = re.sub(
    r'<button type="button" onclick="window\.print\(\)" class="btn-smooth px-4 py-2 bg-white [^"]*"',
    r'<button type="button" onclick="window.print()" class="btn-smooth px-4 py-2 bg-white hover:bg-[#fad2e1]/30 text-[#3d1825] text-xs font-bold rounded-xl border border-[#fad2e1] shadow-xs cursor-pointer flex items-center gap-1.5"',
    text
)

# Feedback Modal Submit Button
text = re.sub(
    r'<button type="button" onclick="submitFeedback\(\)" class="btn-smooth px-5 py-2\.5 [^"]*"',
    r'<button type="button" onclick="submitFeedback()" class="btn-smooth px-5 py-2.5 bg-[#fad2e1] hover:bg-[#f7bcd0] text-[#3d1825] font-black text-xs rounded-xl border border-[#f2a8c0] shadow-xs cursor-pointer flex items-center gap-2"',
    text
)

# -------------------------------------------------------------
# 2. SUCCESS STATES: Xanh mint #c5dedd, chữ #183634, viền #9fc5c3
# -------------------------------------------------------------

# File upload success JS
text = text.replace(
    'iconContainer.className = "w-14 h-14 mx-auto rounded-2xl bg-emerald-100 border-2 border-emerald-500 text-emerald-600 shadow-md flex items-center justify-center text-2xl transition-all scale-110";',
    'iconContainer.className = "w-14 h-14 mx-auto rounded-2xl bg-[#c5dedd] border-2 border-[#9fc5c3] text-[#183634] shadow-md flex items-center justify-center text-2xl transition-all scale-110";'
)
text = text.replace(
    'icon.className = "fa-solid fa-circle-check text-2xl text-emerald-600";',
    'icon.className = "fa-solid fa-circle-check text-2xl text-[#183634]";'
)
text = text.replace(
    'title.innerHTML = `<span class="text-emerald-700 font-black"><i class="fa-solid fa-circle-check mr-1.5"></i> Tải Dữ Liệu Hoàn Tất!</span>`;',
    'title.innerHTML = `<span class="text-[#183634] font-black"><i class="fa-solid fa-circle-check mr-1.5"></i> Tải Dữ Liệu Hoàn Tất!</span>`;'
)
text = text.replace(
    'pBar.className = "h-full bg-emerald-500 transition-all duration-300";',
    'pBar.className = "h-full bg-[#c5dedd] border-t border-[#9fc5c3] transition-all duration-300";'
)

# Selected File Pill in Step 1
text = text.replace(
    '<div id="selectedFilePill" class="hidden mt-2 inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#B8D9D3] text-[#203833] border border-[#75BFB2] text-xs font-bold shadow-xs">',
    '<div id="selectedFilePill" class="hidden mt-2 inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#c5dedd] text-[#183634] border border-[#9fc5c3] text-xs font-bold shadow-xs">'
)

# Step 2 Verification Badge in JS
text = text.replace(
    'verifyBadge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#B8D9D3]/40 text-[#203833] border border-[#75BFB2]";',
    'verifyBadge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#c5dedd] text-[#183634] border border-[#9fc5c3]";'
)
text = text.replace(
    'verifyBadge.innerHTML = `<i class="fa-solid fa-circle-check text-[#75BFB2] mr-1"></i> ĐÃ PHÊ DUYỆT LÀM SẠCH`;',
    'verifyBadge.innerHTML = `<i class="fa-solid fa-circle-check text-[#183634] mr-1"></i> ĐÃ PHÊ DUYỆT LÀM SẠCH`;'
)

# Step 3 Verification Badge in JS
text = text.replace(
    'badge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#B8D9D3]/40 text-[#203833] border border-[#75BFB2]";',
    'badge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#c5dedd] text-[#183634] border border-[#9fc5c3]";'
)
text = text.replace(
    'badge.innerHTML = `<i class="fa-solid fa-circle-check text-[#75BFB2] mr-1"></i> ĐÃ KIỂM ĐỊNH TOÀN DIỆN`;',
    'badge.innerHTML = `<i class="fa-solid fa-circle-check text-[#183634] mr-1"></i> ĐÃ KIỂM ĐỊNH TOÀN DIỆN`;'
)

# Step 4 Verification Badges in JS
text = text.replace(
    'badge.className = "px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#B8D9D3] text-[#203833] border border-[#75BFB2]";',
    'badge.className = "px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#c5dedd] text-[#183634] border border-[#9fc5c3]";'
)
text = text.replace(
    'badge.innerHTML = `<i class="fa-solid fa-stamp text-[#75BFB2] mr-1.5"></i> ĐÃ KÝ PHÊ DUYỆT`;',
    'badge.innerHTML = `<i class="fa-solid fa-stamp text-[#183634] mr-1.5"></i> ĐÃ KÝ PHÊ DUYỆT`;'
)

# Step 4 Step-Approval Badge
text = text.replace(
    'badge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#B8D9D3] text-[#203833] border border-[#75BFB2]";',
    'badge.className = "px-3 py-1 rounded-full text-[11px] font-bold bg-[#c5dedd] text-[#183634] border border-[#9fc5c3]";'
)
text = text.replace(
    'badge.innerHTML = `<i class="fa-solid fa-circle-check text-[#75BFB2] mr-1"></i> ĐÃ PHÊ DUYỆT BƯỚC NÀY`;',
    'badge.innerHTML = `<i class="fa-solid fa-circle-check text-[#183634] mr-1"></i> ĐÃ PHÊ DUYỆT BƯỚC NÀY`;'
)

# Sidebar Active Step Class in JS
text = text.replace(
    "sideBtn.classList.add('bg-[#75BFB2]', 'text-[#203833]', 'font-black', 'shadow-sm');",
    "sideBtn.classList.add('bg-[#c5dedd]', 'text-[#183634]', 'font-black', 'shadow-sm');"
)
text = text.replace(
    "sideAudit.classList.add('bg-[#75BFB2]', 'text-[#203833]', 'font-black', 'shadow-sm');",
    "sideAudit.classList.add('bg-[#c5dedd]', 'text-[#183634]', 'font-black', 'shadow-sm');"
)
text = text.replace(
    "sideChat.classList.add('bg-[#75BFB2]', 'text-[#203833]', 'font-black', 'shadow-sm');",
    "sideChat.classList.add('bg-[#c5dedd]', 'text-[#183634]', 'font-black', 'shadow-sm');"
)

# Sidebar Active Step 1 Initial HTML
text = text.replace(
    'id="side-step-1" class="side-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-[#75BFB2] text-[#203833] font-extrabold shadow-sm',
    'id="side-step-1" class="side-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-[#c5dedd] text-[#183634] font-black shadow-sm'
)

# Sidebar Inactive text & borders
text = text.replace('text-[#B8D9D3]', 'text-[#c5dedd]/80')
text = text.replace('border-[#75BFB2]/20', 'border-[#c5dedd]/20')
text = text.replace('border-[#75BFB2]/30', 'border-[#c5dedd]/30')
text = text.replace('border-[#75BFB2]/40', 'border-[#c5dedd]/40')

with open(r'd:\Xây dựng Agent\ui\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Phase 2 applied successfully!")
