import re

with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update HTML and Body Background to #fde2e4
text = re.sub(
    r'<html lang="vi" class="[^"]*">',
    r'<html lang="vi" class="h-full bg-[#fde2e4] text-[#1b322f] antialiased">',
    text
)
text = re.sub(
    r'<body class="[^"]*bg-gradient-to-br[^"]*">',
    r'<body class="h-full flex p-2 sm:p-4 lg:p-6 justify-center items-center overflow-x-hidden bg-[#fde2e4]">',
    text
)

# 2. Update Tailwind config
old_tw_block = text[text.find('colors: {'):text.find('boxShadow: {')]
new_tw_block = """colors: {
                        forshop: {
                            sidebar: '#1e3532',       /* Contrast Deep Slate Green */
                            sidebarDark: '#142624',
                            sidebarHover: '#294844',
                            primary: '#c5dedd',       /* Mint Green (Success & Verification) */
                            mint: '#c5dedd',          /* Sage Mint #c5dedd */
                            mintDark: '#183634',      /* Readable Mint Contrast */
                            pink: '#fad2e1',          /* Rose Pink #fad2e1 (Action Buttons) */
                            pinkDark: '#3d1825',      /* Readable Pink Contrast */
                            blush: '#fde2e4',         /* Overall Page Background #fde2e4 */
                            dark: '#1b322f',          /* Crisp Headings & Body */
                            pageBg: '#fde2e4',
                            cardBg: '#ffffff',
                            cardMint: '#c5dedd',
                            cardPink: '#fad2e1',
                            cardBlush: '#fde2e4'
                        }
                    },
                    """
text = text.replace(old_tw_block, new_tw_block)

# 3. Main Workspace background
text = text.replace('id="mainWorkspaceContainer" class="flex-1 flex flex-col overflow-y-auto px-6 sm:px-8 lg:px-10 py-6 space-y-6 bg-[#F2E5E4]/25"',
                    'id="mainWorkspaceContainer" class="flex-1 flex flex-col overflow-y-auto px-6 sm:px-8 lg:px-10 py-6 space-y-6 bg-[#fde2e4]/35"')

# 4. Landing container border & ambient lights
text = text.replace('border-2 border-[#B8D9D3]', 'border-2 border-[#fad2e1]')
text = text.replace('bg-[#75BFB2]/40', 'bg-[#c5dedd]/40')
text = text.replace('bg-[#D991A4]/40', 'bg-[#fad2e1]/40')

# 5. Hero CTA button (màu hồng cho nút hành động #fad2e1)
hero_btn_old = text[text.find('<button type="button" onclick="navigateTo(\'app\'); goToStep(1);'):]
hero_btn_old = hero_btn_old[:hero_btn_old.find('</button>')+9]
hero_btn_new = """<button type="button" onclick="navigateTo('app'); goToStep(1);" class="btn-smooth w-full sm:w-auto px-8 py-4 bg-[#fad2e1] hover:bg-[#f8b4cb] text-[#3d1825] font-black text-xs sm:text-sm tracking-wide rounded-2xl shadow-lg border-2 border-[#f2a8c0] flex items-center justify-center gap-3 cursor-pointer transform hover:scale-105 transition-all">
                            <span>VÀO KHÔNG GIAN LÀM VIỆC</span>
                            <i class="fa-solid fa-arrow-right text-[#3d1825] text-base"></i>
                        </button>"""
text = text.replace(hero_btn_old, hero_btn_new)

# 6. Hero 3 Highlight Pillars
text = text.replace('border-2 border-[#75BFB2]', 'border-2 border-[#c5dedd]')
text = text.replace('border-2 border-[#D991A4]', 'border-2 border-[#fad2e1]')
text = text.replace('text-[#75BFB2]', 'text-[#c5dedd]')
text = text.replace('text-[#D991A4]', 'text-[#fad2e1]')

with open(r'd:\Xây dựng Agent\ui\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Phase 1 applied successfully!")
