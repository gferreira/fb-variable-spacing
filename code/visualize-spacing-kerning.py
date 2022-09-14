from importlib import reload
import variableSpacing.spacingSetter
reload(variableSpacing.spacingSetter)

import os
from variableSpacing.spacingSetter import *

# --------
# settings
# --------

designspacePath = '/hipertipo/tools/VariableSpacing/demos/Roboto/Roboto.designspace'

txt = 'AVATAR voxr.'

steps = 5
s = 0.045
savePDF = False

# -----
# draw!
# -----

newPage('A4Landscape')
fill(1)
rect(0, 0, height(), width())

x, y = 50, height() * 0.8

S = SpacingSetter(designspacePath)
S.colorBox      = 1, 0, 1, 0.35
S.colorKerning  = 0, 1, 1, 0.35
S.colorTracking = 1, 1, 0, 0.35
S.useKerning    = True
S.drawKerning   = True
S.drawWidths    = True
S.drawGlyphs    = True
S.drawTracking  = True

for i in range(steps):
    spac = i * -100 / (steps-1)
    print(i, spac)
    L = dict(width=0, weight=400, spacing=spac, contrast=0, slant=0)
    S.draw(txt, (x, y), s, L)
    y -= S.fontInfo.unitsPerEm * s * 1.12

if savePDF:
    dstFolder = '/hipertipo/tools/spacingTools/_imgs'
    pdfPath = os.path.join(dstFolder, f'spacing-axis_kerning-on.pdf')
    saveImage(pdfPath)
