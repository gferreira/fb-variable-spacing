import sys, os

folder = os.getcwd()

try:
    import variableSpacing
except:
    variableSpacingPath = os.path.join(folder, 'Lib')
    sys.path.append(variableSpacingPath)
    import variableSpacing

from importlib import reload
import variableSpacing.spacingSetter
reload(variableSpacing.spacingSetter)

from variableSpacing.spacingSetter import *

colorBox      = 1, 0, 1, 0.35
colorKerning  = 0, 1, 1, 0.35
colorTracking = 1, 1, 0, 0.35

def setup():
    blendMode('multiply')
    fill(1)
    rect(0, 0, height(), width())
    fill(0)
    font('Menlo')
    fontSize(9)

def drawColorCaptions():
    captions = {
        'glyph box' : colorBox,
        'tracking'  : colorTracking,
        'kerning'   : colorKerning,
    }
    x = width() / 2
    y = height() - 30
    col = 100
    with savedState():
        for label, color in captions.items():
            fill(*color)    
            rect(x, y-4, 12, 12)
            fill(0)
            text(label, (x + 20, y))
            translate(col, 0)

# --------
# settings
# --------

designspacePath = '/hipertipo/tools/VariableSpacing/demos/Roboto/Roboto.designspace'

txt = 'AVATAR voxr.'

steps = 5
s = 0.04
savePDF = False
t = -20

L = dict(width=0, weight=400, spacing=0, contrast=0, slant=0)

# -----
# draw!
# -----

S = SpacingSetter(designspacePath)
S.colorBox      = 1, 0, 1, 0.35
S.colorKerning  = 0, 1, 1, 0.35
S.colorTracking = 1, 1, 0, 0.35
S.colorMargins  = 0,
S.useKerning    = False
S.drawKerning   = False
S.drawTracking  = True
S.drawWidths    = True
S.drawGlyphs    = True

# page 1: tracking

newPage('A4Landscape')
setup()
drawColorCaptions()

x, y = 50, height() * 0.8

text('tracking only (kerning off)', (x, height()-30))

for i in range(steps):
    tracking = i * t
    S.tracking = tracking
    S.draw(txt, (x, y), s, L)
    text(str(tracking), (x-30, y))
    y -= S.fontInfo.unitsPerEm * s * 1.25

# page 2: tracking & kerning

S.useKerning  = True
S.drawKerning = False

newPage()
setup()
drawColorCaptions()

y = height() * 0.8

text('tracking + kerning', (x, height()-30))

for i in range(steps):
    tracking = i * t
    S.tracking = tracking
    S.draw(txt, (x, y), s, L)
    text(str(tracking), (x-30, y))
    y -= S.fontInfo.unitsPerEm * s * 1.25

# page 2: tracking & kerning (visible)

S.drawKerning = True

newPage()
setup()
drawColorCaptions()

y = height() * 0.8

text('tracking + kerning (visible)', (x, height()-30))

for i in range(steps):
    tracking = i * t
    S.tracking = tracking
    S.draw(txt, (x, y), s, L)
    text(str(tracking), (x-30, y))
    y -= S.fontInfo.unitsPerEm * s * 1.25

# save document

if savePDF:
    pdfPath = os.path.join(os.path.dirname(folder), 'imgs', 'tracking.pdf')
    saveImage(pdfPath)
