# Erzeugt den Schriftzug „BAUMPFLEGE / Linie / HAPPE“ (dunkel und hell) aus dem gelieferten Logo
# (brand/logo/vorlaeufig/baumpflege-happe_logo_original.jpg, 2000 x 2000, weißer Grund).
# Aufruf: python schriftzug_vorlaeufig.py <logo.jpg> <zielordner>
# Ergebnis: schriftzug-dunkel-voll.png (Originalfarben) und schriftzug-hell-voll.png (Creme, Linie in Gold),
# beide mit transparentem Hintergrund und eng beschnitten.
import sys
from PIL import Image
import numpy as np

IM, ZIEL = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(IM).convert('RGB')).astype(float)

# Bereich des Schriftzugs unterhalb des Emblems
box = (185, 1600, 1815, 1985)
w = a[box[1]:box[3], box[0]:box[2]].copy()

# Deckkraft aus dem dunkelsten Farbkanal, leichtes Rauschen des weißen Grundes entfernen
mc = w.min(2)
cov = np.clip((255 - mc - 14) / (255 - 20 - 14), 0, 1)

# Zeilen der Linie (im Gesamtbild etwa 1797 bis 1806)
linie = np.zeros(cov.shape, bool)
linie[1790 - box[1]:1814 - box[1], :] = True

alv = np.maximum(cov, 1e-3)[..., None]
dunkel_rgb = np.clip((w - 255 * (1 - alv)) / alv, 0, 255)

creme = np.array([243, 245, 236.])
gold = np.array([201, 162, 78.])
hell_rgb = np.where(linie[..., None], gold, creme) * np.ones_like(w)


def bild(rgb):
    return Image.fromarray(np.dstack([rgb, cov * 255]).clip(0, 255).astype('uint8'), 'RGBA')


dk, hl = bild(dunkel_rgb), bild(hell_rgb)
bb = dk.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
dk.crop(bb).save(ZIEL + '/schriftzug-dunkel-voll.png')
hl.crop(bb).save(ZIEL + '/schriftzug-hell-voll.png')
print('ok', dk.crop(bb).size)
