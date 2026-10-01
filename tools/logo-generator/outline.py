"""Linien in Flächen umrechnen und Flächen verrechnen (für Plotter, Stick und Website ohne Masken)."""
import re

import skia


def parse(d):
    """Einfacher Parser für absolute Befehle M L H V C Z."""
    p = skia.Path()
    toks = re.findall(r'[MLHVCZ]|-?\d*\.?\d+(?:e-?\d+)?', d)
    i, cmd, x, y = 0, None, 0.0, 0.0

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v
    while i < len(toks):
        t = toks[i]
        if t in 'MLHVCZ':
            cmd = t
            i += 1
            if cmd == 'Z':
                p.close()
                continue
        if cmd == 'M':
            x, y = num(), num()
            p.moveTo(x, y)
            cmd = 'L'
        elif cmd == 'L':
            x, y = num(), num()
            p.lineTo(x, y)
        elif cmd == 'H':
            x = num()
            p.lineTo(x, y)
        elif cmd == 'V':
            y = num()
            p.lineTo(x, y)
        elif cmd == 'C':
            x1, y1, x2, y2, x, y = (num() for _ in range(6))
            p.cubicTo(x1, y1, x2, y2, x, y)
    return p


def stroke(d, width):
    paint = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    out = skia.Path()
    paint.getFillPath(parse(d), out)
    return out


def union(paths):
    acc = skia.Path()
    for q in paths:
        acc = skia.Op(acc, q, skia.PathOp.kUnion_PathOp)
    return acc


def diff(a, b):
    return skia.Op(a, b, skia.PathOp.kDifference_PathOp)


def circle(cx, cy, r):
    p = skia.Path()
    p.addCircle(cx, cy, r)
    return p


def _n(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def to_svg(path):
    """Pfad als SVG-Daten, mit Füllregel nonzero (AsWinding) und Kegelschnitten als Quadratiken."""
    wp = skia.AsWinding(path) if hasattr(skia, 'AsWinding') else path
    out = []
    it = skia.Path.Iter(wp, False)
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb:
            break
        if verb == skia.Path.kMove_Verb:
            out.append(f'M{_n(pts[0].x())} {_n(pts[0].y())}')
        elif verb == skia.Path.kLine_Verb:
            out.append(f'L{_n(pts[1].x())} {_n(pts[1].y())}')
        elif verb == skia.Path.kQuad_Verb:
            out.append(f'Q{_n(pts[1].x())} {_n(pts[1].y())} {_n(pts[2].x())} {_n(pts[2].y())}')
        elif verb == skia.Path.kConic_Verb:
            quads = skia.Path.ConvertConicToQuads(pts[0], pts[1], pts[2], it.conicWeight(), 2)
            for k in range(1, len(quads), 2):
                out.append(f'Q{_n(quads[k].x())} {_n(quads[k].y())} {_n(quads[k + 1].x())} {_n(quads[k + 1].y())}')
        elif verb == skia.Path.kCubic_Verb:
            out.append(f'C{_n(pts[1].x())} {_n(pts[1].y())} {_n(pts[2].x())} {_n(pts[2].y())} {_n(pts[3].x())} {_n(pts[3].y())}')
        elif verb == skia.Path.kClose_Verb:
            out.append('Z')
    return ''.join(out)
