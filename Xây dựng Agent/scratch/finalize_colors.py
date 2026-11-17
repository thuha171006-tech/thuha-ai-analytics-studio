import re

with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update JS button classes in approve/reset logic
text = text.replace(
    'btnApprove.className = "btn-smooth px-5 py-2.5 bg-[#75BFB2] hover:bg-[#5EABA0] text-white text-xs font-extrabold rounded-xl shadow-md shadow-[#75BFB2]/20 flex items-center gap-2 cursor-pointer shrink-0";',
    'btnApprove.className = "btn-smooth px-5 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer shrink-0";'
)
text = text.replace(
    'btn.className = "btn-smooth px-5 py-2.5 bg-[#75BFB2] hover:bg-[#5EABA0] text-white text-xs font-extrabold rounded-xl shadow-md shadow-[#75BFB2]/20 flex items-center gap-2 cursor-pointer shrink-0";',
    'btn.className = "btn-smooth px-5 py-2.5 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] text-xs font-black rounded-xl shadow-md border-2 border-[#f2a8c0] flex items-center gap-2 cursor-pointer shrink-0";'
)

# 2. Update modal angles button classes
text = text.replace(
    "btnBg: 'bg-[#75BFB2] hover:bg-[#203833]',",
    "btnBg: 'bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] border border-[#f2a8c0]',"
)
text = text.replace(
    "btnBg: 'bg-[#75BFB2] hover:bg-[#5EABA0]',",
    "btnBg: 'bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] border border-[#f2a8c0]',"
)

# 3. Update Chart.js default colors
text = text.replace(
    "const colors = ['#75BFB2', '#fad2e1', '#c5dedd', '#fad2e1', '#203833', '#872D43', '#5EABA0'];",
    "const colors = ['#c5dedd', '#fad2e1', '#fde2e4', '#1e3532', '#9fc5c3', '#f2a8c0', '#203833'];"
)
text = text.replace(
    "actualType === 'line' ? 'rgba(117, 191, 178, 0.35)' : '#75BFB2'",
    "actualType === 'line' ? 'rgba(197, 222, 221, 0.45)' : '#c5dedd'"
)
text = text.replace(
    "actualType === 'line' ? '#75BFB2' : (isDoughnut ? '#ffffff' : '#75BFB2')",
    "actualType === 'line' ? '#1e3532' : (isDoughnut ? '#ffffff' : '#c5dedd')"
)

# Replace remaining bar chart background '#75BFB2' with '#c5dedd'
text = text.replace("backgroundColor: '#75BFB2'", "backgroundColor: '#c5dedd'")
text = text.replace("borderColor: '#75BFB2'", "borderColor: '#c5dedd'")
text = text.replace("pointBackgroundColor: '#75BFB2'", "pointBackgroundColor: '#1e3532'")
text = text.replace("pointBorderColor: '#75BFB2'", "pointBorderColor: '#c5dedd'")

# Replace step banner header gradients
text = text.replace(
    "bg-gradient-to-r from-[#203833] via-[#2A4C45] to-[#75BFB2]",
    "bg-gradient-to-r from-[#1e3532] via-[#24433f] to-[#3a635e]"
)
text = text.replace(
    "text-[#75BFB2]",
    "text-[#c5dedd]"
)
text = text.replace(
    "border-[#75BFB2]",
    "border-[#c5dedd]"
)
text = text.replace(
    "bg-[#75BFB2]",
    "bg-[#c5dedd]"
)
text = text.replace(
    "ring-[#75BFB2]",
    "ring-[#c5dedd]"
)

with open(r'd:\Xây dựng Agent\ui\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Finalized colors in ui/index.html!")
