import re

with open(r'd:\Xây dựng Agent\ui\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML/Body background
content = re.sub(
    r'<html lang="vi" class="[^"]*">',
    r'<html lang="vi" class="h-full bg-[#fde2e4] text-[#1b322f] antialiased">',
    content
)

content = re.sub(
    r'<body class="[^"]*bg-gradient-to-br[^"]*">',
    r'<body class="h-full flex p-2 sm:p-4 lg:p-6 justify-center items-center overflow-x-hidden bg-[#fde2e4]">',
    content
)

# 2. Update Tailwind config colors
old_tailwind = """                        forshop: {
                            sidebar: '#203833',       /* Deep Contrast Teal Slate */
                            sidebarDark: '#172A26',
                            sidebarHover: '#2E4E47',
                            primary: '#75BFB2',       /* Swatch 3: Fresh Seafoam Mint Teal */
                            teal: '#75BFB2',          /* Swatch 3: #75BFB2 */
                            tealLight: '#B8D9D3',     /* Swatch 4: #B8D9D3 */
                            rose: '#D991A4',          /* Swatch 2: #D991A4 (Vibrant Accent Rose) */
                            roseSoft: '#D9A3AC',      /* Swatch 1: #D9A3AC (Dusty Rose) */
                            cream: '#F2E5E4',         /* Swatch 5: #F2E5E4 (Alabaster Cream Blush) */
                            dark: '#203833',          /* Contrast Dark Slate */
                            pageBg: '#F2E5E4',
                            cardBg: '#ffffff',
                            cardBlue: '#B8D9D3',
                            cardPink: '#D9A3AC',
                            cardPurple: '#D991A4',
                            cardAmber: '#F2E5E4',
                            cardGreen: '#75BFB2'
                        }"""

new_tailwind = """                        forshop: {
                            sidebar: '#1e3532',       /* Deep Contrast Slate Green */
                            sidebarDark: '#152725',
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
                        }"""

if old_tailwind in content:
    content = content.replace(old_tailwind, new_tailwind)
    print("Updated Tailwind config.")
else:
    print("Tailwind config block not matched exactly, checking...")

# 3. Ambient Lights on Landing
content = content.replace('bg-[#75BFB2]/40', 'bg-[#c5dedd]/40')
content = content.replace('bg-[#D991A4]/40', 'bg-[#fad2e1]/40')
content = content.replace('bg-[#B8D9D3]/40', 'bg-[#c5dedd]/40')

print("Ambient lights updated.")
