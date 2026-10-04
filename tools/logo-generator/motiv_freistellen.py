# Stellt das Bildmotiv (Eiche mit Baumkletterer) vom weißen Hintergrund frei.
# Aufruf: python motiv_freistellen.py <motiv.jpg> <ziel.png>
# Klare Farbflächen bleiben deckend, weißer Hintergrund wird durchsichtig. An den Kanten wird die Farbe
# aus dem Inneren übernommen und die Deckkraft aus der Mischung mit Weiß berechnet, so entsteht kein heller Saum.
import sys
import numpy as np
from PIL import Image

QUELLE, ZIEL = sys.argv[1], sys.argv[2]
c = np.asarray(Image.open(QUELLE).convert('RGB')).astype(np.float32)
weiss = np.float32(255)
d = (weiss - c).max(2)            # Abstand zu Weiß
# Heller, fast farbloser Saum um die Formen (stammt aus der gelieferten Datei) zählt nicht zum Motiv
saum = (c.min(2) > 165) & ((c.max(2) - c.min(2)) < 30)
kern = (d >= 60) & ~saum          # eindeutig Motiv
grund = d < 12                    # eindeutig Hintergrund
rand = ~kern & ~grund


def nachbarmittel(werte, maske):
    """Mittelwert der Nachbarn (3 x 3), die in der Maske liegen."""
    summe = np.zeros_like(werte); anzahl = np.zeros(maske.shape, np.float32)
    p = np.pad(werte * maske[..., None], ((1, 1), (1, 1), (0, 0)))
    pm = np.pad(maske.astype(np.float32), 1)
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            summe += p[dy:dy + maske.shape[0], dx:dx + maske.shape[1]]
            anzahl += pm[dy:dy + maske.shape[0], dx:dx + maske.shape[1]]
    return summe, anzahl


# Farbe des Motivs von innen nach außen in den Randbereich übertragen
farbe = c.copy(); bekannt = kern.copy()
for _ in range(10):
    summe, anzahl = nachbarmittel(farbe, bekannt)
    neu = ~bekannt & (anzahl > 0)
    farbe[neu] = summe[neu] / anzahl[neu][:, None]
    bekannt |= neu

# Deckkraft am Rand: Anteil der Motivfarbe in der Mischung mit Weiß
f_w = farbe - weiss; c_w = c - weiss
nenner = np.maximum((f_w * f_w).sum(2), 1)
deck = np.clip((c_w * f_w).sum(2) / nenner, 0, 1)
alpha = np.where(kern, 1.0, np.where(grund, 0.0, np.where(bekannt, deck, 0.0)))
rgb = np.where(kern[..., None], c, farbe)

bild = Image.fromarray(np.dstack([rgb, alpha * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
bb = bild.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
bild = bild.crop(bb)
bild.save(ZIEL, optimize=True)
print('ok', bild.size, 'Randpixel', int(rand.sum()))
