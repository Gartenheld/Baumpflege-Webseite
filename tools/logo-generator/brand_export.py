import json, os
from logos import v1, svg_doc, F1_SERIF
R = '/home/user/Baumpflege-Webseite/brand/logo'
FARBEN = {
    'farbig': ('#173F3C', '#A65A2E'),
    'tanne': ('#173F3C', '#173F3C'),
    'schwarz': ('#000000', '#000000'),
    'weiss': ('#FFFFFF', '#FFFFFF'),
    'negativ': ('#F3EEE6', '#DE9A68'),
}
VAR = ['quer', 'quer_kurz', 'stapel', 'stapel_kurz', 'wort', 'wort_kurz', 'symbol', 'symbol_klein']
jobs = []
for v in VAR:
    lg = v1(v)
    for f, (P, A) in FARBEN.items():
        name = f'baumpflege-happe_{v.replace("_", "-")}_{f}'
        svg = svg_doc(lg, P, A, uid=name)
        open(f'{R}/svg/{name}.svg', 'w').write(svg + '\n')
        if v in ('quer', 'stapel', 'symbol') and f in ('farbig', 'negativ', 'weiss'):
            jobs.append({'kind': 'png', 'name': name, 'w': lg['w'], 'h': lg['h']})
        if v in ('quer', 'stapel', 'symbol') and f in ('farbig', 'schwarz', 'weiss'):
            jobs.append({'kind': 'pdf', 'name': name, 'w': lg['w'], 'h': lg['h']})
json.dump(jobs, open('brand_jobs.json', 'w'))
# Kennzahlen für die Richtlinie
q = v1('quer'); qk = v1('quer_kurz')
cap = F1_SERIF.cap * 64 / F1_SERIF.upem
print(json.dumps({'quer': [q['w'], q['h']], 'quer_kurz': [qk['w'], qk['h']], 'cap_H': cap}))
