from importlib import reload
import spacingSetter
reload(spacingSetter)

import os
from spacingSetter import *

# --------
# settings
# --------

designspacePath = '/hipertipo/fonts/Publica/_ufos/Publica.designspace'

txt = 'AVATAR voxr.'

steps = 5
s = 0.15
savePDF = True

# -----
# draw!
# -----

x, y = 40, height() * 0.8

S = SpacingSetter(designspacePath)
S.colorKerning = 0.7,
S.colorBox     = 0.85,
S.useKerning   = True
S.drawKerning  = True
S.drawWidths   = True
S.drawGlyphs   = True

for i in range(steps):
    spac = i * 1.0 / (steps-1)
    L = dict(width=0, weight=0.5, spacing=spac, contrast=0, slant=0)
    S.draw(txt, (x, y), s, L)
    y -= S.fontInfo.unitsPerEm * s * 1.2

if savePDF:
    dstFolder = '/hipertipo/tools/spacingTools/_imgs'
    pdfPath = os.path.join(dstFolder, f'spacing-axis_kerning-on.pdf')
    saveImage(pdfPath)