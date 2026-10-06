# Erzeugt den Schriftzug „BAUMPFLEGE / goldene Linie / HAPPE“ (dunkel und hell) aus dem gelieferten Logo
# (brand/logo/baumpflege-happe_schriftzug_original.jpg, weißer Grund). Die goldene Linie wird automatisch gefunden.
# Aufruf: python schriftzug.py <logo.jpg> <zielordner>
# Ergebnis: schriftzug-dunkel-voll.png (dunkle Schrift mit dem feinen Schatten der Vorlage, goldene Linie) und
# schriftzug-hell-voll.png (Schrift in Creme ohne Schatten, Linie in Gold), beide transparent und eng beschnitten.
import sys
from PIL import Image
import numpy as np

IM, ZIEL = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(IM).convert('RGB')).astype(float)
gold = np.array([201, 162, 78.])
creme = np.array([243, 245, 236.])

# Goldene Linie: Zeilen mit vielen deutlich goldenen Pixeln (Rot klar über Blau)
goldig = (a[..., 0] - a[..., 2]) > 60
zeilen = np.nonzero(goldig.sum(1) > 0.3 * goldig.sum(1).max())[0]
linie = np.zeros(a.shape[:2], bool)
linie[zeilen.min() - 2:zeilen.max() + 3, :] = True
linie &= (a[..., 0] - a[..., 2]) > 8

# Deckkraft: Schrift über den dunkelsten Kanal, Linie über den Blaukanal (dort ist Gold am kräftigsten)
deck_schrift = np.clip((255 - a.min(2) - 12) / (255 - 15 - 12), 0, 1)
deck_hell = np.clip((150 - a.min(2)) / (150 - 30), 0, 1)  # ohne den hellen Schatten an der Kante
deck_linie = np.clip((255 - a[..., 2] - 10) / (255 - gold[2] - 10), 0, 1)
cov_dunkel = np.where(linie, deck_linie, deck_schrift)
cov_hell = np.where(linie, deck_linie, deck_hell)

alv = np.maximum(cov_dunkel, 1e-3)[..., None]
dunkel_rgb = np.clip((a - 255 * (1 - alv)) / alv, 0, 255)
dunkel_rgb[linie] = gold
hell_rgb = np.where(linie[..., None], gold, creme) * np.ones_like(a)


def bild(rgb, cov):
    return Image.fromarray(np.dstack([rgb, cov * 255]).clip(0, 255).astype('uint8'), 'RGBA')


dk, hl = bild(dunkel_rgb, cov_dunkel), bild(hell_rgb, cov_hell)
bb = dk.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
dk.crop(bb).save(ZIEL + '/schriftzug-dunkel-voll.png')
hl.crop(bb).save(ZIEL + '/schriftzug-hell-voll.png')
print('ok', dk.crop(bb).size, 'Linie Zeilen', zeilen.min(), zeilen.max())
