# Erzeugt den Schriftzug (dunkel und hell) aus dem Original, mit deutlicherem Eichenblatt.
import sys
from PIL import Image, ImageFilter
import numpy as np
IM, ZIEL, FAKTOR = sys.argv[1], sys.argv[2], float(sys.argv[3])
a = np.asarray(Image.open(IM).convert('RGB')).astype(float)
box = (255, 1380, 1565, 1708)
w = a[box[1]:box[3], box[0]:box[2]].copy()
Hh, Ww = w.shape[:2]
mc = w.min(2); mx = w.max(2)
cov = np.clip((255 - mc - 14) / (255 - 150 - 14), 0, 1)
cov[:110, 1150:] = 0  # Fleck rechts oben

# --- Blatt herauslösen ---
y0, y1, x0, x1 = 125, 222, 588, 710
pw = w[y0:y1, x0:x1]; pc = cov[y0:y1, x0:x1]
# Silhouette: Adern (hell) im Inneren schließen
img = Image.fromarray((pc * 255).astype('uint8'))
geschl = np.asarray(img.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))).astype(float) / 255
sil = np.maximum(pc, geschl)
L = pw @ np.array([0.2126, 0.7152, 0.0722])
satt = pw.max(2) - pw.min(2)
innen = np.asarray(Image.fromarray(((sil > 0.5) * 255).astype('uint8')).filter(ImageFilter.MinFilter(7))) > 0
ader = np.clip((L - 110) / (165 - 110), 0, 1) * (satt < 90) * innen
# Adern verstärken, damit sie auch klein sichtbar bleiben
ader = np.asarray(Image.fromarray((ader * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3))).astype(float) / 255 * innen
koerper = (sil > 0.5) & (ader < 0.3)
Lk = L[koerper]; lo, hi = np.percentile(Lk, 5), np.percentile(Lk, 95)
t = np.clip((L - lo) / max(hi - lo, 1), 0, 1)[..., None]

# helle Fassung: Gold mit Schattierung, Adern dunkel (wie ausgeschnitten)
gold_tief = np.array([184, 145, 61.]); gold_hell = np.array([236, 214, 156.]); ader_farbe = np.array([62, 74, 50.])
hell_blatt = gold_tief * (1 - t) + gold_hell * t
hell_blatt = hell_blatt * (1 - ader[..., None]) + ader_farbe * ader[..., None]
# dunkle Fassung: Originalfarben, Adern deckend weiß-grünlich
dunkel_blatt = pw.copy()

def skaliert(rgb, alpha):
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype('uint8'), 'RGBA')
    nw, nh = round(im.width * FAKTOR), round(im.height * FAKTOR)
    # vormultipliziert skalieren, damit keine hellen Ränder entstehen
    pm = np.asarray(im).astype(float); pm[..., :3] *= pm[..., 3:4] / 255
    pmi = Image.fromarray(pm.astype('uint8'), 'RGBA').resize((nw, nh), Image.LANCZOS)
    r = np.asarray(pmi).astype(float); al = np.maximum(r[..., 3:4], 1e-3)
    r[..., :3] = np.clip(r[..., :3] * 255 / al, 0, 255)
    return r

def zusammensetzen(grund_rgb, blatt_rgb):
    rgba = np.dstack([grund_rgb, cov * 255]).astype(float)
    rgba[y0:y1, x0:x1, 3] = 0  # altes Blatt entfernen
    b = skaliert(blatt_rgb, sil)
    cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    by, bx = round(cy - b.shape[0] / 2), round(cx - b.shape[1] / 2)
    ziel = rgba[by:by + b.shape[0], bx:bx + b.shape[1]]
    ab = b[..., 3:4] / 255; az = ziel[..., 3:4] / 255
    aout = ab + az * (1 - ab)
    ziel[..., :3] = (b[..., :3] * ab + ziel[..., :3] * az * (1 - ab)) / np.maximum(aout, 1e-3)
    ziel[..., 3:4] = aout * 255
    return Image.fromarray(np.clip(rgba, 0, 255).astype('uint8'), 'RGBA')

alv = np.maximum(cov, 1e-3)[..., None]
dunkel_rgb = np.clip((w - 255 * (1 - alv)) / alv, 0, 255)
creme = np.array([243, 245, 236.]) * np.ones_like(w)
dk = zusammensetzen(dunkel_rgb, dunkel_blatt)
hl = zusammensetzen(creme, hell_blatt)
bb = dk.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
dk.crop(bb).save(ZIEL + '/schriftzug-dunkel-voll.png'); hl.crop(bb).save(ZIEL + '/schriftzug-hell-voll.png')
print('ok', dk.crop(bb).size)
