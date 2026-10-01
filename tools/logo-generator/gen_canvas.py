"""Erzeugt die Zeichenflächen des Design-Canvas (Schritt 2: Logo und Farben)."""
import json
import os

from colors import contrast, nearest_ral, hex2rgb
from logos import VORSCHLAEGE

ROOT = 'canvas'
os.makedirs(f'{ROOT}/project', exist_ok=True)

RAL_DE = {
    'RAL 6005': 'Moosgrün', 'RAL 6011': 'Resedagrün', 'RAL 9001': 'Cremeweiß', 'RAL 1011': 'Braunbeige',
    'RAL 7021': 'Schwarzgrau', 'RAL 6025': 'Farngrün', 'RAL 9003': 'Signalweiß', 'RAL 9002': 'Grauweiß',
    'RAL 6004': 'Blaugrün', 'RAL 8023': 'Orangebraun',
}

# ------------------------------------------------------------------ Farbwelten
WELTEN = {
    'A': dict(name='Waldgrün und Leinen', p='#1F3D2B', a='#6F8A5E', g='#F5F1E8', t='#1A1F1B', hi='#B07A2A',
              tint='#E4EADD', cta='#1F3D2B', lp='#F5F1E8', la='#B9C9A8',
              farben=[('Hauptfarbe', 'Waldgrün', '#1F3D2B'), ('Akzent', 'Salbei', '#6F8A5E'),
                      ('Grund', 'Leinen', '#F5F1E8'), ('Hervorhebung', 'Ocker', '#B07A2A'), ('Schrift', 'Fast Schwarz', '#1A1F1B')],
              fahrzeug='Weißes Fahrzeug, Schrift und Symbol in Waldgrün, Unterzeile in Salbei',
              kleidung='Waldgrün, Logo in Leinen und hellem Salbei'),
    'B': dict(name='Anthrazit und Moos', p='#2B2F2D', a='#5E7D32', g='#F6F6F2', t='#1E211F', hi='#5E7D32',
              tint='#E3E8D8', cta='#5E7D32', lp='#F6F6F2', la='#A3BE73',
              farben=[('Hauptfarbe', 'Anthrazit', '#2B2F2D'), ('Akzent', 'Moos', '#5E7D32'),
                      ('Grund', 'Kalkweiß', '#F6F6F2'), ('Fläche', 'Hellmoos', '#E3E8D8'), ('Schrift', 'Fast Schwarz', '#1E211F')],
              fahrzeug='Weißes Fahrzeug, Schrift in Anthrazit, Symbol und Unterzeile in Moos',
              kleidung='Anthrazit, Logo in Kalkweiß und hellem Moos'),
    'C': dict(name='Tanne und Kupfer', p='#173F3C', a='#A65A2E', g='#F3EEE6', t='#1A2120', hi='#A65A2E',
              tint='#DCE6E2', cta='#A65A2E', lp='#F3EEE6', la='#DE9A68',
              farben=[('Hauptfarbe', 'Tanne', '#173F3C'), ('Akzent', 'Kupfer', '#A65A2E'),
                      ('Grund', 'Sand', '#F3EEE6'), ('Fläche', 'Nebelgrün', '#DCE6E2'), ('Schrift', 'Fast Schwarz', '#1A2120')],
              fahrzeug='Weißes Fahrzeug, Schrift in Tanne, Symbol und Unterzeile in Kupfer',
              kleidung='Tanne, Logo in Sand und hellem Kupfer'),
}

SCHRIFTEN = {
    '1': dict(titel='Klassisch', namen='Source Serif 4 und Source Sans 3',
              display="'Source Serif 4', Georgia, serif", body="'Source Sans 3', 'Segoe UI', sans-serif",
              fvs='normal', stretch='100%', dw='600'),
    '2': dict(titel='Natürlich und warm', namen='Fraunces und Figtree',
              display="'Fraunces', Georgia, serif", body="'Figtree', 'Segoe UI', sans-serif",
              fvs="'SOFT' 50, 'WONK' 0", stretch='100%', dw='560'),
    '3': dict(titel='Modern und reduziert', namen='Instrument Sans',
              display="'Instrument Sans', 'Segoe UI', sans-serif", body="'Instrument Sans', 'Segoe UI', sans-serif",
              fvs='normal', stretch='88%', dw='640'),
}

LABEL = "'Figtree', 'Segoe UI', sans-serif"
FONT_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Figtree:wght@400;500;600;700'
             '&amp;family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,0..100,0..1'
             '&amp;family=Instrument+Sans:wdth,wght@75..100,400..700'
             '&amp;family=Source+Sans+3:wght@400;600'
             '&amp;family=Source+Serif+4:opsz,wght@8..60,400..700&amp;display=swap">')


def fmt(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def logo_svg(n, variant, P, A, uid, max_w, max_h):
    lg = VORSCHLAEGE[int(n)](variant)
    s = min(max_w / lg['w'], max_h / lg['h'])
    w, h = lg['w'] * s, lg['h'] * s
    body = lg['body'].replace('{P}', P).replace('{A}', A).replace('{U}', uid)
    return (f'<svg viewBox="{lg["viewBox"]}" width="{fmt(w)}" height="{fmt(h)}" role="img" '
            f'aria-label="Logo Baumpflege Happe, Vorschlag {n}" style="display: block">{body}</svg>')


def page(title, body, script, props, w, h):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT_LINK}
<style>
body{{margin:0}}
a{{color:#1F3D2B}}a:hover{{color:#0F2418}}
button{{cursor:pointer}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps({**props, "$preview": {"width": w, "height": h}}, ensure_ascii=False).replace("'", "&#39;")}'>
{script}
</script>
</body>
</html>
'''


WELTEN_JS = json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('farben',)} for k, v in WELTEN.items()}, ensure_ascii=False)
SCHRIFTEN_JS = json.dumps(SCHRIFTEN, ensure_ascii=False)
STATIC_SCRIPT = 'class Component extends DCLogic {\n  renderVals() {\n    return {};\n  }\n}'


def welt_script(extra=''):
    return f'''const WELTEN = {WELTEN_JS};
class Component extends DCLogic {{
  renderVals() {{
    const welt = this.props.farbwelt ?? 'A';
    const c = WELTEN[welt] || WELTEN.A;
    return {{ c: c{extra} }};
  }}
}}'''


def card(inner, label, extra_style='background: #FFFFFF', h=None, grow=True):
    hh = f'height: {h}px; ' if h else ''
    g = 'flex-grow: 1; flex-basis: 0; ' if grow else ''
    return (f'<div style="{g}{hh}box-sizing: border-box; {extra_style}; border-radius: 10px; padding: 20px; '
            f'display: flex; flex-direction: column; gap: 12px; min-width: 0">'
            f'<div style="flex-grow: 1; display: flex; align-items: center; justify-content: center">{inner}</div>'
            f'<div style="font-family: {LABEL}; font-size: 13px; color: #5F635E">{label}</div></div>')


# ------------------------------------------------------------------ Main (Überblick)
def main_board():
    W, H = 1200, 880
    logos = ''.join(
        f'''<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 10px; padding: 24px; display: flex; flex-direction: column; gap: 16px; min-width: 0">
<div style="height: 120px; display: flex; align-items: center; justify-content: center">{logo_svg(n, 'quer', '{{c.p}}', '{{c.a}}', 'm' + n, 310, 100)}</div>
<div style="font-family: {LABEL}"><div style="font-size: 18px; font-weight: 600; color: #1A1F1B">{n} · {SCHRIFTEN[n]['titel']}</div>
<div style="font-size: 14px; color: #5F635E; margin-top: 4px">{SCHRIFTEN[n]['namen']}</div></div></div>''' for n in '123')
    welten = ''.join(
        f'''<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 10px; padding: 24px; display: flex; flex-direction: column; gap: 16px; min-width: 0">
<div style="display: flex; height: 72px; border-radius: 6px; overflow: hidden">{''.join(f'<div style="flex-grow: {3 if i == 0 else 1}; background: {hx}"></div>' for i, (_, _, hx) in enumerate(v['farben'][:4]))}</div>
<div style="font-family: {LABEL}"><div style="font-size: 18px; font-weight: 600; color: #1A1F1B">{k} · {v['name']}</div>
<div style="font-size: 14px; color: #5F635E; margin-top: 4px">{' · '.join(f[1] for f in v['farben'][:4])}</div></div></div>''' for k, v in WELTEN.items())
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 56px; background: #F2EFE8; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 28px">
<div>
<div style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5F635E">Schritt 2 von 5 · Zur Auswahl</div>
<h1 style="margin: 10px 0 0; font-size: 44px; line-height: 1.1; font-weight: 600">Logo und Farben für Baumpflege Happe</h1>
<p style="margin: 14px 0 0; font-size: 18px; line-height: 1.5; color: #3B3F3A; max-width: 880px">Drei Logo-Vorschläge und drei Farbwelten. Logo und Farbwelt lassen sich frei kombinieren, jedes Logo gibt es mit und ohne Symbol. Unten siehst du jede Kombination auf Website, Fahrzeug und Arbeitskleidung.</p>
</div>
<div style="display: flex; flex-direction: column; gap: 12px">
<h2 style="margin: 0; font-size: 20px; font-weight: 600">Logo-Vorschläge</h2>
<div style="display: flex; gap: 20px">{logos}</div>
</div>
<div style="display: flex; flex-direction: column; gap: 12px">
<h2 style="margin: 0; font-size: 20px; font-weight: 600">Farbwelten</h2>
<div style="display: flex; gap: 20px">{welten}</div>
</div>
<div style="background: #FFFFFF; border-radius: 10px; padding: 20px 24px; font-size: 17px; line-height: 1.5">Deine Auswahl, zum Beispiel: <strong>Logo 2 mit Symbol, Farbwelt A</strong>. Mischungen und Änderungswünsche sind ausdrücklich willkommen.</div>
</div>'''
    return page('Überblick Logo und Farben', body, welt_script(), {"farbwelt": {"editor": "enum", "options": ["A", "B", "C"], "default": "A"}}, W, H)


# ------------------------------------------------------------------ Logo-Boards
def logo_board(n):
    W, H = 1200, 880
    S = SCHRIFTEN[n]
    big = card(logo_svg(n, 'quer', '{{c.p}}', '{{c.a}}', f'b{n}q', 680, 140), 'Mit Symbol, quer', h=210, grow=False)
    row2 = ''.join([
        card(logo_svg(n, 'stapel', '{{c.p}}', '{{c.a}}', f'b{n}s', 300, 170), 'Mit Symbol, gestapelt'),
        card(logo_svg(n, 'wort', '{{c.p}}', '{{c.a}}', f'b{n}w', 330, 110), 'Nur Schriftzug'),
        card(logo_svg(n, 'symbol', '{{c.p}}', '{{c.a}}', f'b{n}y', 140, 150), 'Nur Symbol'),
    ])
    small = (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">'
             f'{logo_svg(n, "quer_kurz", "{{c.p}}", "{{c.a}}", f"b{n}k", 220, 34)}'
             f'<div style="display: flex; gap: 18px; align-items: end">{logo_svg(n, "symbol", "{{c.p}}", "{{c.a}}", f"b{n}f1", 48, 48)}'
             f'{logo_svg(n, "symbol", "{{c.p}}", "{{c.a}}", f"b{n}f2", 32, 32)}{logo_svg(n, "symbol", "{{c.p}}", "{{c.a}}", f"b{n}f3", 16, 16)}</div></div>')
    row3 = ''.join([
        card(logo_svg(n, 'quer', '{{c.lp}}', '{{c.la}}', f'b{n}d', 300, 86), '<span style="color: #FFFFFF">Auf dunklem Grund</span>', extra_style='background: {{c.p}}'),
        card(logo_svg(n, 'quer', '#1A1A1A', '#1A1A1A', f'b{n}e', 300, 86), 'Einfarbig (Stempel, Gravur, einfarbige Folie)'),
        card(small, 'Klein, ohne Unterzeile: Handy-Kopfzeile, App- und Browser-Symbol'),
    ])
    fonts = f'''<div style="background: #FFFFFF; border-radius: 10px; padding: 20px 24px; display: flex; flex-direction: column; gap: 8px">
<div style="font-family: {S['display']}; font-variation-settings: {S['fvs']}; font-stretch: {S['stretch']}; font-weight: {S['dw']}; font-size: 30px; line-height: 1.15; color: {{{{c.p}}}}">Baumpflege und Baumfällung in Bornheim, Köln und Bonn</div>
<div style="font-family: {S['body']}; font-size: 17px; line-height: 1.5; color: {{{{c.t}}}}">Wir schneiden, sichern und fällen Bäume fachgerecht, häckseln das Schnittgut vor Ort und hinterlassen Ihr Grundstück aufgeräumt.</div>
<div style="font-family: {LABEL}; font-size: 13px; color: #5F635E">Schriftprobe: {S['namen']}</div></div>'''
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 40px 48px; background: {{{{c.g}}}}; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 16px">
<div style="display: flex; justify-content: space-between; align-items: end">
<div><div style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5F635E">Vorschlag {n}</div>
<h1 style="margin: 4px 0 0; font-size: 34px; font-weight: 600">{S['titel']}</h1></div>
<div style="font-size: 14px; color: #5F635E">Dargestellt in Farbwelt {{{{welt}}}} · Schrift: {S['namen']}</div>
</div>
{big}
<div style="display: flex; gap: 16px; height: 220px">{row2}</div>
<div style="display: flex; gap: 16px; height: 150px">{row3}</div>
{fonts}
</div>'''
    script = f'''const WELTEN = {WELTEN_JS};
class Component extends DCLogic {{
  renderVals() {{
    const welt = this.props.farbwelt ?? 'A';
    return {{ c: WELTEN[welt] || WELTEN.A, welt: WELTEN[welt] ? welt : 'A' }};
  }}
}}'''
    return page(f'Logo-Vorschlag {n}', body, script, {"farbwelt": {"editor": "enum", "options": ["A", "B", "C"], "default": "A"}}, W, H)


# ------------------------------------------------------------------ Farbwelt-Boards
def star(color):
    return (f'<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="{color}" '
            'd="M12 2.6l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17l-5.6 3 1.1-6.3L2.9 9.3l6.3-.9z"/></svg>')


def welt_board(k):
    W, H = 1200, 880
    v = WELTEN[k]
    sw = []
    for role, name, hx in v['farben']:
        r, g, b = hex2rgb(hx)
        ral = nearest_ral(hx)
        ral_txt = f'nahe {ral[0]} {RAL_DE.get(ral[0], ral[1])}' if role != 'Schrift' else 'für Texte'
        border = 'border: 1px solid #D9D5CC; ' if hx.upper() in ('#F5F1E8', '#F6F6F2', '#F3EEE6', '#E3E8D8', '#DCE6E2', '#E4EADD') else ''
        sw.append(f'''<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; min-width: 0">
<div style="height: 130px; background: {hx}; {border}border-radius: 10px 10px 0 0"></div>
<div style="padding: 14px 16px; font-size: 14px; line-height: 1.55; color: #3B3F3A">
<div style="font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: #5F635E">{role}</div>
<div style="font-size: 18px; font-weight: 600; color: #1A1F1B">{name}</div>
<div>{hx.upper()}</div><div>RGB {r} {g} {b}</div><div>{ral_txt}</div></div></div>''')
    white = '#FFFFFF'
    checks = [
        ('Schrift auf Grund', contrast(v['t'], v['g']), 'Fließtext'),
        ('Hauptfarbe auf Grund', contrast(v['p'], v['g']), 'Überschriften, Links'),
        ('Weiße Schrift auf Button', contrast(white, v['cta']), 'Button „Anfrage mit Fotos senden“'),
        ('Akzent auf Grund', contrast(v['a'], v['g']), 'Symbole, Linien, große Schrift'),
        ('Helles Logo auf Hauptfarbe', contrast(v['la'], v['p']), 'Kleidung, dunkle Flächen'),
    ]

    def verdict(cr, use):
        if 'Akzent' in use or 'Symbole' in use:
            return 'ab 3:1 für Grafik und große Schrift: erfüllt' if cr >= 3 else 'zu schwach'
        return 'WCAG AA erfüllt' if cr >= 4.5 else ('nur große Schrift' if cr >= 3 else 'zu schwach')
    rows = ''.join(
                   f'<div style="display: flex; justify-content: space-between; gap: 12px; padding: 9px 0; border-top: 1px solid #ECE8E0"><div><div style="font-weight: 600">{n}</div><div style="color: #5F635E; font-size: 13px">{use}</div></div><div style="text-align: right; white-space: nowrap"><div style="font-weight: 600">{f"{cr:.1f}".replace(".", ",")} : 1</div><div style="color: #5F635E; font-size: 13px">{verdict(cr, use)}</div></div></div>'
                   for n, cr, use in checks)
    sample = f'''<div style="flex-grow: 1; flex-basis: 0; background: {v['g']}; border: 1px solid #E2DED5; border-radius: 10px; padding: 28px; display: flex; flex-direction: column; gap: 14px">
<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {v['a'] if contrast(v['a'], v['g']) >= 4.5 else v['p']}">Baumfällung</div>
<div style="font-family: 'Source Serif 4', Georgia, serif; font-size: 30px; font-weight: 600; line-height: 1.15; color: {v['p']}">Sicher gefällt, sauber aufgeräumt</div>
<div style="font-size: 16px; line-height: 1.55; color: {v['t']}">Wir planen jede Fällung sorgfältig, häckseln das Schnittgut vor Ort und fahren es ab.</div>
<div style="display: flex; gap: 12px; flex-wrap: wrap">
<a href="#" style="background: {v['cta']}; color: #FFFFFF; text-decoration: none; padding: 13px 20px; border-radius: 8px; font-weight: 600; font-size: 16px">Anfrage mit Fotos senden</a>
<a href="#" style="border: 2px solid {v['p']}; color: {v['p']}; text-decoration: none; padding: 11px 18px; border-radius: 8px; font-weight: 600; font-size: 16px">Anrufen</a></div>
<div style="display: flex; align-items: center; gap: 4px; margin-top: 4px">{star(v['hi']) * 5}<span style="margin-left: 8px; font-size: 14px; color: {v['t']}">[Durchschnitt] aus [Anzahl] Google-Bewertungen</span></div>
<div style="display: flex; gap: 10px; margin-top: 4px">
<div style="background: {v['tint']}; color: {v['t']}; border-radius: 6px; padding: 8px 12px; font-size: 14px">Fläche für Hinweise</div>
<div style="background: {v['p']}; color: #FFFFFF; border-radius: 6px; padding: 8px 12px; font-size: 14px">Dunkle Fläche</div></div></div>'''
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 40px 48px; background: #F2EFE8; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 18px">
<div><div style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5F635E">Farbwelt {k}</div>
<h1 style="margin: 4px 0 0; font-size: 34px; font-weight: 600">{v['name']}</h1></div>
<div style="display: flex; gap: 14px">{''.join(sw)}</div>
<div style="display: flex; gap: 18px; flex-grow: 1">
{sample}
<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 10px; padding: 20px 24px; font-size: 15px; display: flex; flex-direction: column">
<div style="font-size: 16px; font-weight: 600; margin-bottom: 6px">Kontraste</div>
{rows}
<div style="border-top: 1px solid #ECE8E0; padding-top: 10px; margin-top: auto; font-size: 14px; line-height: 1.5; color: #3B3F3A"><strong>Fahrzeug:</strong> {v['fahrzeug']}.<br><strong>Kleidung:</strong> {v['kleidung']}.<br>RAL-Angaben sind Richtwerte. Folierer und Textildrucker stimmen die Farbe mit ihrem Farbfächer ab.</div>
</div></div>
</div>'''
    return page(f'Farbwelt {k}', body, STATIC_SCRIPT, {}, W, H)


# ------------------------------------------------------------------ Interaktive Anwendungen
INTERACTIVE_PROPS = {
    "logo": {"editor": "enum", "options": ["1", "2", "3"], "default": "1", "section": "Auswahl"},
    "farbwelt": {"editor": "enum", "options": ["A", "B", "C"], "default": "A", "section": "Auswahl"},
    "symbol": {"editor": "boolean", "default": True, "section": "Auswahl"},
}

INTERACTIVE_SCRIPT = f'''const WELTEN = {WELTEN_JS};
const SCHRIFTEN = {SCHRIFTEN_JS};
class Component extends DCLogic {{
  renderVals() {{
    const s = this.state || {{}};
    const logo = s.logo ?? String(this.props.logo ?? '1');
    const welt = s.welt ?? (this.props.farbwelt ?? 'A');
    const sym = s.sym ?? (this.props.symbol ?? true);
    const c = WELTEN[welt] || WELTEN.A;
    const on = (active) => active
      ? {{ bg: c.p, fg: '#FFFFFF', bd: c.p, pressed: 'true' }}
      : {{ bg: '#FFFFFF', fg: '#1A1F1B', bd: '#CFCBC2', pressed: 'false' }};
    const pick = (patch) => () => this.setState(Object.assign({{}}, this.state || {{}}, patch));
    return {{
      c: c,
      f: SCHRIFTEN[logo] || SCHRIFTEN['1'],
      welt: welt,
      logos: ['1', '2', '3'].map((id) => Object.assign({{ label: 'Logo ' + id, pick: pick({{ logo: id }}) }}, on(id === logo))),
      welten: ['A', 'B', 'C'].map((id) => Object.assign({{ label: id + ' · ' + WELTEN[id].name, pick: pick({{ welt: id }}) }}, on(id === welt))),
      syms: [[true, 'Mit Symbol'], [false, 'Ohne Symbol']].map(([v, l]) => Object.assign({{ label: l, pick: pick({{ sym: v }}) }}, on(v === sym))),
      l1s: logo === '1' && sym, l1w: logo === '1' && !sym,
      l2s: logo === '2' && sym, l2w: logo === '2' && !sym,
      l3s: logo === '3' && sym, l3w: logo === '3' && !sym,
      l1: logo === '1', l2: logo === '2', l3: logo === '3',
    }};
  }}
}}'''


def selector():
    def group(lst, title):
        return (f'<div style="display: flex; align-items: center; gap: 8px"><span style="font-size: 14px; color: #5F635E; margin-right: 4px">{title}</span>'
                f'<sc-for list="{{{{{lst}}}}}" as="item" hint-placeholder-count="3">'
                '<button type="button" onClick="{{item.pick}}" aria-pressed="{{item.pressed}}" '
                'style="font-family: ' + LABEL + '; font-size: 15px; font-weight: 600; min-height: 44px; padding: 0 16px; border-radius: 22px; '
                'background: {{item.bg}}; color: {{item.fg}}; border: 1px solid {{item.bd}}">{{item.label}}</button></sc-for></div>')
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 20px 32px; align-items: center; background: #FFFFFF; border-radius: 12px; padding: 14px 20px">'
            f'{group("logos", "Logo")}{group("syms", "")}{group("welten", "Farbwelt")}</div>')


def logo_switch(variant_sym, variant_wort, P, A, uid, max_w, max_h, sym_only=False, wort_max=None):
    """Logo je nach Auswahl (Vorschlag 1 bis 3, mit oder ohne Symbol)."""
    out = []
    for n in '123':
        if sym_only:
            out.append(f'<sc-if value="{{{{l{n}}}}}" hint-placeholder-val="{{{{ true }}}}">{logo_svg(n, "symbol", P, A, uid + n + "y", max_w, max_h)}</sc-if>')
        else:
            out.append(f'<sc-if value="{{{{l{n}s}}}}" hint-placeholder-val="{{{{ true }}}}">{logo_svg(n, variant_sym, P, A, uid + n + "s", max_w, max_h)}</sc-if>')
            ww, wh = wort_max or (max_w, max_h)
            out.append(f'<sc-if value="{{{{l{n}w}}}}" hint-placeholder-val="{{{{ false }}}}">{logo_svg(n, variant_wort, P, A, uid + n + "w", ww, wh)}</sc-if>')
    return ''.join(out)


def website_board():
    W, H = 1440, 960
    nav = ''.join(f'<a href="#" style="color: {{{{c.t}}}}; text-decoration: none; font-size: 15px">{t}</a>' for t in ['Leistungen', 'Gewerbe', 'Einsatzgebiet', 'Referenzen', 'Über uns', 'Kontakt'])
    services = ''.join(f'''<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; gap: 8px">
<div style="height: 90px; border-radius: 6px; background: {{{{c.tint}}}}; display: flex; align-items: center; justify-content: center; font-size: 13px; color: {{{{c.t}}}}">[Foto: {foto}]</div>
<div style="font-family: {{{{f.display}}}}; font-variation-settings: {{{{f.fvs}}}}; font-stretch: {{{{f.stretch}}}}; font-weight: {{{{f.dw}}}}; font-size: 21px; color: {{{{c.p}}}}">{t}</div>
<div style="font-size: 15px; line-height: 1.5; color: {{{{c.t}}}}">{txt}</div></div>''' for t, txt, foto in [
        ('Baumpflege', 'Kronenpflege und Schnitt, damit Ihr Baum gesund und sicher bleibt.', 'Kronenschnitt'),
        ('Baumfällung', 'Sorgfältig geplant, Schnittgut wird vor Ort gehäckselt und abgefahren.', 'Fällung'),
        ('Landschaftspflege', 'Heckenschnitt und Pflege von Gehölzen, auch für kleine Gärten.', 'Heckenschnitt')])
    desktop = f'''<div style="width: 940px; flex-shrink: 0; border: 1px solid #D9D5CC; border-radius: 12px; overflow: hidden; background: {{{{c.g}}}}; font-family: {{{{f.body}}}}; color: {{{{c.t}}}}">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 18px 32px; background: #FFFFFF; border-bottom: 1px solid #ECE8E0">
<div>{logo_switch("quer_kurz", "wort_kurz", "{{c.p}}", "{{c.a}}", "wd", 250, 46)}</div>
<nav style="display: flex; gap: 20px; align-items: center">{nav}</nav></div>
<div style="display: flex; gap: 0; height: 410px">
<div style="width: 470px; box-sizing: border-box; padding: 40px 32px; display: flex; flex-direction: column; justify-content: center; gap: 18px">
<h2 style="margin: 0; font-family: {{{{f.display}}}}; font-variation-settings: {{{{f.fvs}}}}; font-stretch: {{{{f.stretch}}}}; font-weight: {{{{f.dw}}}}; font-size: 40px; line-height: 1.1; color: {{{{c.p}}}}">Baumpflege und Baumfällung in Bornheim, Köln und Bonn</h2>
<p style="margin: 0; font-size: 18px; line-height: 1.5">Ihr Baumspezialist zwischen Köln und Bonn. Kostenlose Ersteinschätzung anhand Ihrer Fotos.</p>
<div style="display: flex; gap: 12px; flex-wrap: wrap">
<a href="#" style="background: {{{{c.cta}}}}; color: #FFFFFF; text-decoration: none; padding: 14px 20px; border-radius: 8px; font-weight: 600; font-size: 16px">Anfrage mit Fotos senden</a>
<a href="#" style="border: 2px solid {{{{c.p}}}}; color: {{{{c.p}}}}; text-decoration: none; padding: 12px 18px; border-radius: 8px; font-weight: 600; font-size: 16px">Anrufen</a></div></div>
<div style="flex-grow: 1; background: {{{{c.tint}}}}; display: flex; align-items: center; justify-content: center; font-size: 15px; color: {{{{c.t}}}}; text-align: center; padding: 24px">[Großes eigenes Foto: Baumkrone bei der Arbeit]</div></div>
<div style="display: flex; gap: 16px; padding: 24px 32px">{services}</div></div>'''
    phone = f'''<div style="width: 390px; height: 800px; flex-shrink: 0; box-sizing: border-box; border: 1px solid #D9D5CC; border-radius: 28px; overflow: hidden; background: {{{{c.g}}}}; font-family: {{{{f.body}}}}; color: {{{{c.t}}}}; display: flex; flex-direction: column">
<div style="display: flex; align-items: center; justify-content: space-between; padding: 16px 18px; background: #FFFFFF; border-bottom: 1px solid #ECE8E0">
<div>{logo_switch("quer_kurz", "wort_kurz", "{{c.p}}", "{{c.a}}", "wp", 230, 40)}</div>
<button type="button" aria-label="Menü öffnen" style="width: 44px; height: 44px; border: 0; background: transparent; padding: 10px"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{{{{c.p}}}}" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div>
<div style="height: 230px; background: {{{{c.tint}}}}; display: flex; align-items: center; justify-content: center; font-size: 14px; text-align: center; padding: 16px">[Eigenes Foto]</div>
<div style="padding: 24px 20px; display: flex; flex-direction: column; gap: 14px; flex-grow: 1">
<h2 style="margin: 0; font-family: {{{{f.display}}}}; font-variation-settings: {{{{f.fvs}}}}; font-stretch: {{{{f.stretch}}}}; font-weight: {{{{f.dw}}}}; font-size: 30px; line-height: 1.12; color: {{{{c.p}}}}">Baumpflege und Baumfällung in Bornheim, Köln und Bonn</h2>
<p style="margin: 0; font-size: 17px; line-height: 1.5">Ihr Baumspezialist zwischen Köln und Bonn.</p>
<a href="#" style="background: {{{{c.cta}}}}; color: #FFFFFF; text-decoration: none; padding: 15px 18px; border-radius: 8px; font-weight: 600; font-size: 17px; text-align: center">Anfrage mit Fotos senden</a></div>
<div style="display: flex; border-top: 1px solid #ECE8E0; background: #FFFFFF">
<a href="#" style="flex-grow: 1; flex-basis: 0; display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 60px; color: {{{{c.p}}}}; text-decoration: none; font-weight: 600; font-size: 17px; border-right: 1px solid #ECE8E0"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="{{{{c.p}}}}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Anrufen</a>
<a href="#" style="flex-grow: 1; flex-basis: 0; display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 60px; color: {{{{c.p}}}}; text-decoration: none; font-weight: 600; font-size: 17px"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="{{{{c.p}}}}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21l1.6-4.7A8.5 8.5 0 1 1 7.7 19.4z"/></svg>WhatsApp</a></div></div>'''
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 32px 40px; background: #F2EFE8; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 20px">
<div style="display: flex; justify-content: space-between; align-items: end"><h1 style="margin: 0; font-size: 30px; font-weight: 600">Anwendung: Website</h1><div style="font-size: 14px; color: #5F635E">Entwurf zur Wirkung, die Startseite gestalten wir in Schritt 3</div></div>
{selector()}
<div style="display: flex; gap: 32px; align-items: start">{desktop}{phone}</div>
</div>'''
    return page('Anwendung Website', body, INTERACTIVE_SCRIPT, INTERACTIVE_PROPS, W, H)


def fahrzeug_board():
    W, H = 1200, 960
    truck = '''<svg viewBox="0 0 1040 520" width="1040" height="520" aria-hidden="true" style="position: absolute; left: 0; top: 0">
<rect x="40" y="470" width="960" height="6" rx="3" fill="#D9D5CC"/>
<rect x="70" y="392" width="890" height="34" rx="6" fill="#3A3D3B"/>
<path d="M60 400 V178 C60 150 76 128 104 124 L196 112 C214 110 228 114 240 126 L330 220 C342 232 350 246 350 262 V400 Z" fill="#FFFFFF" stroke="#BDB8AE" stroke-width="3"/>
<path d="M92 214 V160 C92 150 99 144 108 143 L196 134 C206 133 214 136 221 143 L292 214 Z" fill="#D7DEE2" stroke="#BDB8AE" stroke-width="2"/>
<path d="M232 228 V392" stroke="#BDB8AE" stroke-width="2"/>
<rect x="250" y="238" width="22" height="8" rx="4" fill="#BDB8AE"/>
<rect x="44" y="330" width="22" height="38" rx="4" fill="#E9E5DC" stroke="#BDB8AE" stroke-width="2"/>
<rect x="362" y="232" width="610" height="160" rx="6" fill="#FFFFFF" stroke="#BDB8AE" stroke-width="3"/>
<rect x="362" y="370" width="610" height="22" fill="{{c.p}}"/>
<rect x="60" y="378" width="290" height="22" fill="{{c.p}}"/>
<circle cx="210" cy="432" r="62" fill="#2B2B2B"/><circle cx="210" cy="432" r="30" fill="#BDBDBD"/><circle cx="210" cy="432" r="8" fill="#7D7D7D"/>
<circle cx="800" cy="432" r="62" fill="#2B2B2B"/><circle cx="800" cy="432" r="30" fill="#BDBDBD"/><circle cx="800" cy="432" r="8" fill="#7D7D7D"/>
</svg>'''
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 32px 40px; background: #F2EFE8; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 20px">
<div style="display: flex; justify-content: space-between; align-items: end"><h1 style="margin: 0; font-size: 30px; font-weight: 600">Anwendung: Pritschenwagen mit Kipper</h1><div style="font-size: 14px; color: #5F635E">Seitenansicht, schematisch</div></div>
{selector()}
<div style="background: #FFFFFF; border-radius: 12px; padding: 40px 40px 24px; display: flex; flex-direction: column; gap: 24px">
<div style="position: relative; width: 1040px; height: 520px">
{truck}
<div style="position: absolute; left: 238px; top: 250px; width: 108px; height: 116px; display: flex; align-items: center; justify-content: center">{logo_switch("symbol", "wort_kurz", "{{c.p}}", "{{c.a}}", "fs", 84, 100, wort_max=(100, 60))}</div>
<div style="position: absolute; left: 392px; top: 246px; width: 560px; height: 92px; display: flex; align-items: center">{logo_switch("wort", "wort", "{{c.p}}", "{{c.a}}", "fw", 560, 92)}</div>
<div style="position: absolute; left: 392px; top: 342px; width: 560px; height: 24px; display: flex; justify-content: space-between; align-items: center; font-family: {{{{f.body}}}}; font-size: 19px; font-weight: 600; color: {{{{c.p}}}}"><span>baumpflege-happe.de</span><span>Telefon [Platzhalter]</span></div>
</div>
<div style="font-size: 15px; line-height: 1.5; color: #3B3F3A">Tür: Symbol, ohne Symbol der kurze Schriftzug. Pritsche: Schriftzug mit Unterzeile, darunter Domain und Telefon, unten ein Band in der Hauptfarbe.</div>
</div>
</div>'''
    return page('Anwendung Fahrzeug', body, INTERACTIVE_SCRIPT, INTERACTIVE_PROPS, W, H)


def kleidung_board():
    W, H = 1200, 960
    shirt = 'M95 20 L60 32 L10 70 L35 120 L70 100 L70 330 L230 330 L230 100 L265 120 L290 70 L240 32 L205 20 C195 38 175 48 150 48 C125 48 105 38 95 20 Z'
    jacket = 'M92 20 L44 40 L12 320 L58 326 L82 120 L82 350 L218 350 L218 120 L242 326 L288 320 L256 40 L208 20 C194 30 174 36 150 36 C126 36 106 30 92 20 Z'

    def garment(path, fill, inner, cap, sub, stroke='none'):
        return f'''<div style="flex-grow: 1; flex-basis: 0; background: #FFFFFF; border-radius: 12px; padding: 24px; display: flex; flex-direction: column; gap: 14px; align-items: center">
<div style="position: relative; width: 300px; height: 360px">
<svg viewBox="0 0 300 360" width="300" height="360" aria-hidden="true" style="position: absolute; left: 0; top: 0"><path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="2"/></svg>
{inner}</div>
<div style="text-align: center"><div style="font-size: 17px; font-weight: 600">{cap}</div><div style="font-size: 14px; color: #5F635E; margin-top: 2px">{sub}</div></div></div>'''
    front = garment(shirt, '{{c.p}}', f'<div style="position: absolute; left: 160px; top: 76px; width: 84px; height: 40px; display: flex; align-items: center">{logo_switch("quer_kurz", "wort_kurz", "{{c.lp}}", "{{c.la}}", "kc", 84, 34)}</div>',
                    'Shirt oder Polo, vorne', 'Brustlogo ohne Unterzeile, gestickt oder gedruckt')
    back = garment(jacket, '{{c.p}}', f'<div style="position: absolute; left: 86px; top: 64px; width: 128px; height: 140px; display: flex; align-items: center; justify-content: center">{logo_switch("stapel", "wort", "{{c.lp}}", "{{c.la}}", "kb", 128, 136)}</div>',
                   'Jacke, Rücken', 'Großes Logo, gut erkennbar aus Distanz')
    light = garment(shirt, '#FFFFFF', f'<div style="position: absolute; left: 160px; top: 76px; width: 84px; height: 40px; display: flex; align-items: center">{logo_switch("quer_kurz", "wort_kurz", "{{c.p}}", "{{c.a}}", "kl", 84, 34)}</div>',
                    'Helles Shirt', 'Logo in Hauptfarbe und Akzent', stroke='#D9D5CC')
    cap = f'''<div style="display: flex; gap: 24px; align-items: center; background: #FFFFFF; border-radius: 12px; padding: 18px 24px">
<div style="position: relative; width: 150px; height: 96px; flex-shrink: 0">
<svg viewBox="0 0 150 96" width="150" height="96" aria-hidden="true" style="position: absolute; left: 0; top: 0"><path d="M20 74 C20 30 44 8 75 8 C106 8 130 30 130 74 Z" fill="{{{{c.p}}}}"/><path d="M8 74 H142 C142 84 132 90 120 90 H30 C18 90 8 84 8 74 Z" fill="{{{{c.p}}}}"/></svg>
<div style="position: absolute; left: 50px; top: 24px; width: 50px; height: 44px; display: flex; align-items: center; justify-content: center">{logo_switch("symbol", "wort_kurz", "{{c.lp}}", "{{c.la}}", "kk", 34, 38, wort_max=(40, 30))}</div></div>
<div><div style="font-size: 17px; font-weight: 600">Kappe und kleine Flächen</div><div style="font-size: 14px; color: #5F635E; margin-top: 2px">Symbol, ohne Symbol der kurze Schriftzug. Feine Linien stimmt der Sticker vorher ab.</div></div></div>'''
    body = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; padding: 32px 40px; background: #F2EFE8; font-family: {LABEL}; color: #1A1F1B; display: flex; flex-direction: column; gap: 20px">
<div style="display: flex; justify-content: space-between; align-items: end"><h1 style="margin: 0; font-size: 30px; font-weight: 600">Anwendung: Arbeitskleidung</h1><div style="font-size: 14px; color: #5F635E">Kleidung in der Hauptfarbe der Farbwelt</div></div>
{selector()}
<div style="display: flex; gap: 20px">{front}{back}{light}</div>
{cap}
</div>'''
    return page('Anwendung Arbeitskleidung', body, INTERACTIVE_SCRIPT, INTERACTIVE_PROPS, W, H)


# ------------------------------------------------------------------ Dateien und Index
boards = {}
files = {}


def main():


    def add(name, html, x, y, w, h, title, interactive=False):
        files[name] = html
        e = {'x': x, 'y': y, 'w': w, 'h': h, 'title': title}
        if interactive:
            e['is_interactive'] = True
        boards[name] = e


    add('Main.dc.html', main_board(), 0, 0, 1200, 880, 'Überblick')
    for i, n in enumerate('123'):
        add(f'Logo{n}.dc.html', logo_board(n), i * 1280, 1440, 1200, 880, f'Logo-Vorschlag {n}: {SCHRIFTEN[n]["titel"]}')
    for i, k in enumerate('ABC'):
        add(f'Farbwelt{k}.dc.html', welt_board(k), i * 1280, 2700, 1200, 880, f'Farbwelt {k}: {WELTEN[k]["name"]}')
    add('Website.dc.html', website_board(), 0, 3960, 1440, 960, 'Anwendung: Website', True)
    add('Fahrzeug.dc.html', fahrzeug_board(), 1520, 3960, 1200, 960, 'Anwendung: Fahrzeug', True)
    add('Kleidung.dc.html', kleidung_board(), 2800, 3960, 1200, 960, 'Anwendung: Arbeitskleidung', True)

    index = {
        'v': 3,
        'createdOnFiles': {'v': 1, 'at': os.environ.get('NOW', '2026-10-01T18:30:00Z')},
        'title': 'Baumpflege Happe Logo und Farben',
        'launch': {'view': 'canvas'},
        'pages': [],
        'boards': boards,
        'order': list(boards.keys()),
        'notes': {
            'logos': {'x': 0, 'y': 1180, 'text': 'Logo-Vorschläge', 'kind': 'title1', 'maxW': 3760},
            'farben': {'x': 0, 'y': 2440, 'text': 'Farbwelten', 'kind': 'title1', 'maxW': 3760},
            'anwendung': {'x': 0, 'y': 3700, 'text': 'Anwendungen: Logo und Farbwelt per Klick umschalten', 'kind': 'title1', 'maxW': 4000},
        },
        'designSystems': [],
    }
    with open(f'{ROOT}/project/canvas.json', 'w') as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    for name, html in files.items():
        with open(f'{ROOT}/project/{name}', 'w') as fh:
            fh.write(html)
    for name in files:
        print(name, os.path.getsize(f'{ROOT}/project/{name}'))


if __name__ == '__main__':
    main()
