# Erzeugt Favicon, App-Icons und das Logo für Suchmaschinen aus den freigestellten Logos in brand/logo/aktuell.
# Aufruf (im Projektordner): python tools/logo-generator/icons.py
# Ergebnis in public/: favicon.ico (16, 32, 48), icon-192.png, apple-touch-icon.png (180) und logo.png (600 x 600).
# Das Monogramm steht auf einer cremefarbenen Kachel, damit es auch in dunklen Browser-Tabs gut sichtbar ist.
from PIL import Image, ImageDraw

Q = 'brand/logo/aktuell/'
CREME = (243, 245, 236, 255)
mono = Image.open(Q + 'baumpflege-happe_monogramm_dunkel.png').convert('RGBA')
schrift = Image.open(Q + 'baumpflege-happe_schriftzug_dunkel.png').convert('RGBA')


def kachel(groesse, rand, rund=True):
    s = groesse * 4  # vierfach zeichnen, dann verkleinern (weiche Kanten)
    c = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    if rund:
        ImageDraw.Draw(c).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * 0.22), fill=CREME)
    else:
        c.paste(CREME, (0, 0, s, s))
    m = mono.copy()
    m.thumbnail((int(s * (1 - 2 * rand)),) * 2, Image.LANCZOS)
    c.alpha_composite(m, ((s - m.width) // 2, (s - m.height) // 2))
    return c.resize((groesse, groesse), Image.LANCZOS)


# Kleine Größen mit weniger Rand, damit das H im Tab groß genug bleibt
ico = [kachel(g, r) for g, r in ((16, 0.05), (32, 0.09), (48, 0.12))]
ico[-1].save('public/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:-1])
kachel(192, 0.16).save('public/icon-192.png', optimize=True)
kachel(180, 0.17, rund=False).convert('RGB').save('public/apple-touch-icon.png', optimize=True)

# Logo für Suchmaschinen: Monogramm über dem Schriftzug auf Weiß
logo = Image.new('RGB', (600, 600), (255, 255, 255))
m = mono.copy(); m.thumbnail((230, 230), Image.LANCZOS)
w = schrift.copy(); w.thumbnail((430, 430), Image.LANCZOS)
hoehe = m.height + 42 + w.height
y = (600 - hoehe) // 2
logo.paste(m, ((600 - m.width) // 2, y), m)
logo.paste(w, ((600 - w.width) // 2, y + m.height + 42), w)
logo.save('public/logo.png', optimize=True)
print('ok')
