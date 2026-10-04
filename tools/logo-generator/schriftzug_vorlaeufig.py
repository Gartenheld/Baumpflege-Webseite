# Erzeugt den Schriftzug „BAUMPFLEGE / goldene Linie / HAPPE“ (dunkel und hell) aus dem gelieferten Logo
# (brand/logo/vorlaeufig/baumpflege-happe_logo_original.jpg, 2000 x 2000, weißer Grund).
# Aufruf: python schriftzug_vorlaeufig.py <logo.jpg> <zielordner>
# Ergebnis: schriftzug-dunkel-voll.png (Originalfarben: dunkle Schrift, goldene Linie) und
# schriftzug-hell-voll.png (Schrift in Creme, Linie in Gold), beide transparent und eng beschnitten.
import sys
from PIL import Image
import numpy as np

IM, ZIEL = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(IM).convert('RGB')).astype(float)

# Bereich des Schriftzugs und Zeilen der Linie (im Gesamtbild)
box = (20, 885, 1985, 1345)
linie_von, linie_bis = 1106, 1140
w = a[box[1]:box[3], box[0]:box[2]].copy()
linie = np.zeros(w.shape[:2], bool)
linie[linie_von - box[1]:linie_bis - box[1], :] = True

gold = np.array([201, 162, 78.])
creme = np.array([243, 245, 236.])

# Deckkraft: Schrift über den dunkelsten Kanal, Linie über den Blaukanal (dort ist Gold am kräftigsten)
deck_schrift = np.clip((255 - w.min(2) - 14) / (255 - 20 - 14), 0, 1)
deck_linie = np.clip((255 - w[..., 2] - 10) / (255 - gold[2] - 10), 0, 1)
cov = np.where(linie, deck_linie, deck_schrift)

alv = np.maximum(cov, 1e-3)[..., None]
dunkel_rgb = np.clip((w - 255 * (1 - alv)) / alv, 0, 255)
dunkel_rgb[linie] = gold
hell_rgb = np.where(linie[..., None], gold, creme) * np.ones_like(w)


def bild(rgb):
    return Image.fromarray(np.dstack([rgb, cov * 255]).clip(0, 255).astype('uint8'), 'RGBA')


dk, hl = bild(dunkel_rgb), bild(hell_rgb)
bb = dk.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
dk.crop(bb).save(ZIEL + '/schriftzug-dunkel-voll.png')
hl.crop(bb).save(ZIEL + '/schriftzug-hell-voll.png')
print('ok', dk.crop(bb).size)
