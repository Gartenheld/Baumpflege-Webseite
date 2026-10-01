"""Text in SVG-Pfade umwandeln (mit Kerning über HarfBuzz)."""
import io
from functools import lru_cache

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = 'node_modules/@fontsource-variable/'


def _num(v):
    s = f'{v:.1f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


@lru_cache(maxsize=None)
def load(path, axes_items):
    f = TTFont(FONTS + path)
    axes = dict(axes_items)
    if 'fvar' in f:
        fvar_axes = {a.axisTag for a in f['fvar'].axes}
        f = instancer.instantiateVariableFont(f, {k: v for k, v in axes.items() if k in fvar_axes})
    f.flavor = None
    buf = io.BytesIO()
    f.save(buf)
    data = buf.getvalue()
    f = TTFont(io.BytesIO(data))
    return f, data


class Font:
    def __init__(self, path, **axes):
        self.tt, self.data = load(path, tuple(sorted(axes.items())))
        self.face = hb.Face(self.data)
        self.hbfont = hb.Font(self.face)
        self.upem = self.face.upem
        os2 = self.tt['OS/2']
        self.cap = getattr(os2, 'sCapHeight', 0) or 700
        self.xh = getattr(os2, 'sxHeight', 0) or 500
        self.order = self.tt.getGlyphOrder()
        self.gs = self.tt.getGlyphSet()

    def shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, features or {'kern': True, 'liga': True})
        return buf.glyph_infos, buf.glyph_positions

    def path(self, text, size, x=0, y=0, tracking=0.0, features=None):
        """Gibt (d, breite, (xmin, ymin, xmax, ymax)) zurück. y = Grundlinie."""
        infos, poss = self.shape(text, features)
        s = size / self.upem
        track = tracking * self.upem
        pen = SVGPathPen(self.gs, ntos=_num)
        bpen = BoundsPen(self.gs)
        cursor = 0
        for i, (info, pos) in enumerate(zip(infos, poss)):
            name = self.order[info.codepoint]
            ox = x + (cursor + pos.x_offset) * s
            oy = y - pos.y_offset * s
            t = (s, 0, 0, -s, ox, oy)
            self.gs[name].draw(TransformPen(pen, t))
            self.gs[name].draw(TransformPen(bpen, t))
            cursor += pos.x_advance + (track if i < len(infos) - 1 else 0)
        return pen.getCommands(), cursor * s, bpen.bounds

    def width(self, text, size, tracking=0.0, features=None):
        return self.path(text, size, tracking=tracking, features=features)[1]
