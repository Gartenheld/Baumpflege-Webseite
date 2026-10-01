"""Logo-Vorschläge Baumpflege Happe als SVG.

Platzhalter in den Fragmenten: {P} = Hauptfarbe (Schrift, Symbol), {A} = Akzentfarbe, {U} = eindeutige ID.
"""
import math

from textpath import Font, _num

NAME = 'Baumpflege Happe'
TAGLINE = 'Baumpflege · Baumfällung · Landschaftspflege'

# ---------------------------------------------------------------- Schriften
F1_SERIF = Font('source-serif-4/files/source-serif-4-latin-opsz-normal.woff2', wght=600, opsz=60)
F1_SANS = Font('source-sans-3/files/source-sans-3-latin-wght-normal.woff2', wght=600)
F2_SERIF = Font('fraunces/files/fraunces-latin-full-normal.woff2', wght=560, opsz=96, SOFT=50, WONK=0)
F2_SANS = Font('figtree/files/figtree-latin-wght-normal.woff2', wght=600)
F3_SANS = Font('instrument-sans/files/instrument-sans-latin-wdth-normal.woff2', wght=640, wdth=88)
F3_TAG = Font('instrument-sans/files/instrument-sans-latin-wdth-normal.woff2', wght=560, wdth=100)


# ---------------------------------------------------------------- Symbole
# Jedes Symbol: (svg-Fragment, breite, höhe) in eigenen Koordinaten.

def symbol_krone():
    """Vorschlag 1: Krone als Fläche, Astwerk ausgespart, Stamm darunter."""
    w, h = 120, 136
    branches = [('M60 97 V70', 8), ('M60 78 C52 72 44 66 34 62', 6), ('M60 72 C68 64 76 58 86 54', 6),
                ('M60 70 C58 58 56 48 50 36', 5.5), ('M56 52 C60 46 64 40 68 30', 4.5),
                ('M44 66 C40 58 38 52 37 44', 4), ('M78 58 C80 50 82 44 82 38', 4)]
    lines = ''.join(f'<path d="{d}" stroke-width="{sw}"/>' for d, sw in branches)
    svg = f'''<mask id="k{{U}}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
<rect width="{w}" height="{h}" fill="#fff"/>
<g fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round">{lines}</g>
</mask>
<circle cx="60" cy="54" r="50" fill="{{P}}" mask="url(#k{{U}})"/>
<path d="M54.6 101.5 H65.4 L66.6 127 C66.9 130.6 68.8 132.4 73 133 H47 C51.2 132.4 53.1 130.6 53.4 127 Z" fill="{{P}}"/>'''
    return svg, w, h


def symbol_blattbaum():
    """Vorschlag 2: Blatt, dessen Mittelrippe zum Stamm wird (Linienzeichnung)."""
    w, h = 120, 132
    veins = ''.join(f'<path d="{d}"/>' for d in ['M60 86 C53 80 47 74 43 66', 'M60 72 C67 66 72 60 76 52',
                                                  'M60 58 C54 52 51 46 49 38', 'M60 46 C64 42 67 37 69 31'])
    svg = ('<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="7">'
           '<path d="M60 8 C86 24 98 54 84 80 C77 92 68 98 60 99 C52 98 43 92 36 80 C22 54 34 24 60 8 Z" stroke="{A}"/>'
           f'<g stroke="{{P}}"><path d="M60 126 V24"/>{veins}<path d="M47 126 H73"/></g></g>')
    return svg, w, h


def _blob(cx, cy, r, amp, seed, n=72):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        rr = r + amp * (math.sin(3 * t + seed) * 0.6 + math.sin(5 * t + seed * 2.3) * 0.4)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    d = f'M{_num(pts[0][0])} {_num(pts[0][1])}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f'C{_num(c1[0])} {_num(c1[1])} {_num(c2[0])} {_num(c2[1])} {_num(p2[0])} {_num(p2[1])}'
    return d + 'Z'


def symbol_jahresringe():
    """Vorschlag 3: Jahresringe eines Stammquerschnitts, mit Trockenriss."""
    w, h = 120, 120
    outer = _blob(60, 60, 52, 1.8, 0.7)
    r1 = _blob(59, 62, 38, 2.2, 1.3 + 3.8)
    r2 = _blob(55.5, 66, 22, 1.4, 1.3 + 2.2)
    svg = f'''<mask id="r{{U}}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
<rect width="{w}" height="{h}" fill="#fff"/>
<path d="M54 67.5 L70 50 L74 47 L104 17" stroke="#000" stroke-width="6.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#r{{U}})" fill="none" stroke="{{P}}">
<path d="{outer}" stroke-width="9"/>
<path d="{r1}" stroke-width="7"/>
<path d="{r2}" stroke-width="6.5"/>
</g>
<circle cx="52" cy="69.5" r="6" fill="{{A}}"/>'''
    return svg, w, h


# ---------------------------------------------------------------- Bausteine

def text_el(font, text, size, x, y, color='{P}', tracking=0.0, features=None):
    d, wid, b = font.path(text, size, x=x, y=y, tracking=tracking, features=features)
    return f'<path d="{d}" fill="{color}"/>', wid, b


def place(symbol, x, y, height):
    svg, w, h = symbol
    s = height / h
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.5f})">{svg}</g>', w * s


def wrap(body, w, h, pad=0):
    vb = f'{_num(-pad)} {_num(-pad)} {_num(w + 2 * pad)} {_num(h + 2 * pad)}'
    return {'body': body, 'viewBox': vb, 'w': w + 2 * pad, 'h': h + 2 * pad}


# ---------------------------------------------------------------- Vorschlag 1: Klassisch

def v1_wordmark(x=0, y=0, tagline=True):
    """Zweizeilig: Baumpflege / Happe, Unterzeile in Kapitälchen-Optik."""
    size = 64
    cap = F1_SERIF.cap * size / F1_SERIF.upem
    lh = size * 0.98
    p1, w1, _ = text_el(F1_SERIF, 'Baumpflege', size, x, y + cap)
    p2, w2, _ = text_el(F1_SERIF, 'Happe', size, x, y + cap + lh)
    parts = [p1, p2]
    width = max(w1, w2)
    height = cap + lh + size * 0.24  # Unterlänge von p
    if tagline:
        ts = 14
        tcap = F1_SANS.cap * ts / F1_SANS.upem
        ty = y + height + 16 + tcap
        p3, w3, _ = text_el(F1_SANS, TAGLINE.upper(), ts, x, ty, color='{A}', tracking=0.12)
        parts.append(p3)
        width = max(width, w3)
        height = ty - y
    return ''.join(parts), width, height


def v1(variant):
    tag = not variant.endswith('_kurz')
    variant = variant.replace('_kurz', '')
    if variant == 'wort':
        body, w, h = v1_wordmark(tagline=tag)
        return wrap(body, w, h, pad=8)
    if variant == 'quer':
        tw, th = v1_wordmark(0, 0, tagline=tag)[1:]
        sym_h = th * 1.08
        s, sw = place(symbol_krone(), 0, -th * 0.04, sym_h)
        gap = sym_h * 0.22
        t, tw, th = v1_wordmark(sw + gap, 0, tagline=tag)
        return wrap(s + t, sw + gap + tw, th, pad=8)
    if variant == 'stapel':
        t0, tw, th = v1_wordmark(0, 0, tagline=tag)
        sym_h = 150
        sym = symbol_krone()
        sw = sym[1] * sym_h / sym[2]
        width = max(tw, sw)
        s, _ = place(sym, (width - sw) / 2, 0, sym_h)
        t, _, _ = v1_wordmark((width - tw) / 2, sym_h + 36, tagline=tag)
        return wrap(s + t, width, sym_h + 36 + th, pad=8)
    if variant == 'symbol':
        svg, w, h = symbol_krone()
        return wrap(svg, w, h, pad=4)


# ---------------------------------------------------------------- Vorschlag 2: Natürlich-warm

def v2_wordmark(x=0, y=0, tagline=True, size=62):
    cap = F2_SERIF.cap * size / F2_SERIF.upem
    p1, w1, _ = text_el(F2_SERIF, NAME, size, x, y + cap, tracking=-0.005)
    parts = [p1]
    width = w1
    height = cap + size * 0.22
    if tagline:
        # Unterzeile auf die Breite des Namens ausgleichen
        base = F2_SANS.width(TAGLINE, 10)
        ts = 10 * (w1 * 0.995) / base
        ts = min(ts, 19)
        tcap = F2_SANS.cap * ts / F2_SANS.upem
        ty = y + height + 12 + tcap
        tw = F2_SANS.width(TAGLINE, ts)
        p3, w3, _ = text_el(F2_SANS, TAGLINE, ts, x + (w1 - tw) / 2, ty, color='{A}')
        parts.append(p3)
        height = ty - y + ts * 0.2
    return ''.join(parts), width, height


def v2(variant):
    tag = not variant.endswith('_kurz')
    variant = variant.replace('_kurz', '')
    if variant == 'wort':
        body, w, h = v2_wordmark(tagline=tag)
        return wrap(body, w, h, pad=8)
    if variant == 'quer':
        _, tw, th = v2_wordmark(0, 0, tagline=tag)
        sym_h = th * 1.25
        s, sw = place(symbol_blattbaum(), 0, -th * 0.16, sym_h)
        gap = sym_h * 0.16
        t, tw, th = v2_wordmark(sw + gap, 0, tagline=tag)
        return wrap(s + t, sw + gap + tw, th, pad=12)
    if variant == 'stapel':
        _, tw, th = v2_wordmark(0, 0, tagline=tag)
        sym_h = 160
        sym = symbol_blattbaum()
        sw = sym[1] * sym_h / sym[2]
        width = max(tw, sw)
        s, _ = place(sym, (width - sw) / 2, 0, sym_h)
        t, _, _ = v2_wordmark((width - tw) / 2, sym_h + 30, tagline=tag)
        return wrap(s + t, width, sym_h + 30 + th, pad=8)
    if variant == 'symbol':
        svg, w, h = symbol_blattbaum()
        return wrap(svg, w, h, pad=4)


# ---------------------------------------------------------------- Vorschlag 3: Modern-reduziert

def v3_wordmark(x=0, y=0, tagline=True, size=50):
    cap = F3_SANS.cap * size / F3_SANS.upem
    p1, w1, _ = text_el(F3_SANS, NAME.upper(), size, x, y + cap, tracking=0.06)
    parts = [p1]
    width = w1
    height = cap
    if tagline:
        base = F3_TAG.width(TAGLINE.upper(), 10, tracking=0.16)
        ts = min(10 * w1 / base, 15)
        tr = 0.16
        # Laufweite so anpassen, dass die Unterzeile genau die Namensbreite hat
        for _ in range(30):
            tw = F3_TAG.width(TAGLINE.upper(), ts, tracking=tr)
            tr += (w1 - tw) / (ts * (len(TAGLINE) - 1)) * 0.9
        tcap = F3_TAG.cap * ts / F3_TAG.upem
        ty = y + cap + 18 + tcap
        p3, _, _ = text_el(F3_TAG, TAGLINE.upper(), ts, x, ty, color='{A}', tracking=tr)
        parts.append(p3)
        height = ty - y
    return ''.join(parts), width, height


def v3(variant):
    tag = not variant.endswith('_kurz')
    variant = variant.replace('_kurz', '')
    if variant == 'wort':
        body, w, h = v3_wordmark(tagline=tag)
        return wrap(body, w, h, pad=8)
    if variant == 'quer':
        _, tw, th = v3_wordmark(0, 0, tagline=tag)
        sym_h = th * 1.55
        s, sw = place(symbol_jahresringe(), 0, (th - sym_h) / 2, sym_h)
        gap = sym_h * 0.26
        t, tw, th = v3_wordmark(sw + gap, 0, tagline=tag)
        top = min(0, (th - sym_h) / 2)
        body = f'<g transform="translate(0 {_num(-top)})">{s}{t}</g>'
        return wrap(body, sw + gap + tw, max(th, sym_h), pad=8)
    if variant == 'stapel':
        _, tw, th = v3_wordmark(0, 0, tagline=tag)
        sym_h = 130
        sym = symbol_jahresringe()
        sw = sym[1] * sym_h / sym[2]
        width = max(tw, sw)
        s, _ = place(sym, (width - sw) / 2, 0, sym_h)
        t, _, _ = v3_wordmark((width - tw) / 2, sym_h + 34, tagline=tag)
        return wrap(s + t, width, sym_h + 34 + th, pad=8)
    if variant == 'symbol':
        svg, w, h = symbol_jahresringe()
        return wrap(svg, w, h, pad=4)


VORSCHLAEGE = {1: v1, 2: v2, 3: v3}
VARIANTEN = ['quer', 'stapel', 'wort', 'symbol']


def svg_doc(logo, P, A, uid='x', title='Baumpflege Happe'):
    body = logo['body'].replace('{P}', P).replace('{A}', A).replace('{U}', uid)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{logo["viewBox"]}" '
            f'width="{_num(logo["w"])}" height="{_num(logo["h"])}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>')
