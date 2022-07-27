from importlib import reload
import spacingSetter
reload(spacingSetter)

import os
from spacingSetter import *

designspacePath = '/hipertipo/fonts/Publica/_ufos/Publica.designspace'

S = SpacingSetter(designspacePath)
S.previewKerning = True

steps = 5
s = 0.15
savePDF = True

for j in range(2):
    newPage()
    x, y = 40, height() * 0.8
    S.drawKerning = False if j == 0 else True
    for i in range(steps):
        spac = i * 1.0 / (steps-1)
        L = dict(width=0, weight=0.5, spacing=spac, contrast=0, slant=0)
        S.draw('AVATAR voxr.', (x, y), s, L)
        y -= S.fontInfo.unitsPerEm * s * 1.2

if savePDF:
    dstFolder = '/Users/gferreira/Desktop/spacing'
    pdfPath = os.path.join(dstFolder, f'spacing-axis-preview.pdf')
    saveImage(pdfPath)
