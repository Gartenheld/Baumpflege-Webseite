from outline import stroke, union, diff, circle, parse, to_svg
TRUNK = 'M54.6 101.5 H65.4 L66.6 127 C66.9 130.6 68.8 132.4 73 133 H47 C51.2 132.4 53.1 130.6 53.4 127 Z'
BR = [('M60 97 V70', 8), ('M60 78 C52 72 44 66 34 62', 6), ('M60 72 C68 64 76 58 86 54', 6),
      ('M60 70 C58 58 56 48 50 36', 5.5), ('M56 52 C60 46 64 40 68 30', 4.5),
      ('M44 66 C40 58 38 52 37 44', 4), ('M78 58 C80 50 82 44 82 38', 4)]
# Für kleine Größen (16 bis 48 px): weniger, kräftigere Äste
BR_KLEIN = [('M60 96 V68', 12), ('M60 80 C52 73 44 67 34 61', 10), ('M60 72 C68 64 75 58 85 52', 10),
            ('M60 68 C59 56 57 46 52 34', 9)]

def krone(branches):
    crown = diff(circle(60, 54, 50), union([stroke(d, w) for d, w in branches]))
    return to_svg(union([crown, parse(TRUNK)]))

if __name__ == '__main__':
    d1, d2 = krone(BR), krone(BR_KLEIN)
    print(len(d1), len(d2), d1[:160])
    P='#173F3C'
    cells=''
    for name,d in (('fein',d1),('klein',d2)):
        svg=f'<svg viewBox="0 0 120 136" xmlns="http://www.w3.org/2000/svg"><path d="{d}" fill="{P}"/></svg>'
        cells+=f'<div class="c"><b>{name}</b>{svg.replace("<svg","<svg width=200")}<div class="s">{svg.replace("<svg","<svg width=48")}{svg.replace("<svg","<svg width=32")}{svg.replace("<svg","<svg width=24")}{svg.replace("<svg","<svg width=16")}</div></div>'
    open('final_symbol.html','w').write(f'<!doctype html><meta charset=utf-8><style>body{{margin:0;padding:20px;background:#F3EEE6;display:flex;gap:20px;font-family:sans-serif}}.c{{background:#fff;padding:16px}}.s{{display:flex;gap:14px;align-items:end;margin-top:10px}}</style>{cells}')
