# CarAnteem brand kit (for the content assistant)

## Who we are
CarAnteem (كارانتيم): Jordanian app for original car parts and engine-oil packages.
Core promises: original parts, matched to the car's chassis number (VIN) before shipping,
cash on delivery, delivery to all 12 governorates, a team ready to answer on WhatsApp (0785040907).
App download link: caranteem.com/download.php?q=1  ·  Instagram account id (Windsor): 17841474348741895

## Look
- Colors: red #C8102E (accent variants #D0102C / #E0153A), black #0B0B0E / #111114, white, soft gray #8E8E96 and paper #F7F6F3.
- Font: Tajawal (weights 500/700/800/900), files in node_modules/@fontsource/tajawal/files.
- Logo: logo_w.png (white; on light backgrounds use the SVG filter in the templates to turn it black). App icon = emblem.png on a red rounded square — app-icon use only (e.g. a phone screen). Do NOT put the red square on end cards or covers: the real logo is never red; end cards use logo_w.png alone (Mustafa, 23/11).
- On white/light reels and covers the logo must be FULL solid black (Mustafa, 24/11): use the filter values "0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 3 0" (black + alpha x3), not the old soft-gray one.
- Wording: say «فحمات البريك» / «فحمات», never «تيل» (Mustafa, 24/11).
- Rotate the dominant color daily: white -> red -> black -> white ... (check the last published post).
- Vertical 1080x1920 for reels; keep text inside the centre (y 285-1635) so the 4:5 feed crop never cuts it.

## Voice
Jordanian Arabic, short, confident, a little provocative, never insulting. Value before price.
Hooks that worked: questions to the driver, "مش لأي حدا", "كارانتيم مش صفحة فيسبوك", 3-question checklists, myth/fact.

## Templates (each is a page with window.TOTAL and frame(t); copy and change the scene list)
- ikea.html: kinetic typography, red/white cuts on the beat, echo words, flying products (owner's favourite style).
- investigation.html: white paper, typewriter, magnifying lens, red stamps.
- cinematic.html: dark premium, product spotlight shots, big statements.
- app_character.html (+ man2.js): ordinary guy next to a giant phone with real app screens (s1/car/cats/brk/done/s3/s5.jpg).
- motion_tips.html, questions_black.html: numbered tips on black.
Products (transparent PNG): o_tot (Totachi), sf (Senfineco), c_lm (Liqui Moly), o_kixx, o_valv, o_ofilt/o_afilt (filters), c_ak/c_ate/c_textar (brake pads), c_denso2/c_he/c_mobis (plugs), c_inj (injector cleaner), c_mos.
Never redraw or invent product packaging, logos or certifications; use these images as they are.

## Music
Never reuse the previous reel's track. Generate a new one with python (numpy/scipy) by adapting one of
music_house.py, music_detective.py, music_dark_cinematic.py, music_pop.py (change BPM, key, cut times, seed).
Mux: ffmpeg -i silent.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-16:TP=-1.5" -c:a aac -shortest out.mp4

## Facts you may use (verified)
3,400+ customers · 5,000+ orders · 15,800+ cars saved in the app garage · packages: Totachi 30.90 JD, Liqui Moly 44.90,
Senfineco 39.90, Shell 24.90, Valvoline 28.90, Kixx 29.90 (4L + oil filter + air filter + delivery). Oil change every ~5 months.
Do not invent any other number, price, discount or claim. Do not show competitor names or logos.

## Rules
- Never publish anything without Mustafa's explicit approval of that exact post.
- Never use customer names, phones, emails or screenshots without written consent.
- Render with: node render.js <page.html> silent.mp4 ; previews: node shot.js <page.html> 1 5 9 ...
