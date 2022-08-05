from random import uniform
from grapefruit import Color
from fontParts.world import OpenFont, RGlyph
from hTools3.modules.primitives import rect as Rect
# from progvis.modules.DB.tools import drawGlyph

# --------
# settings
# --------

ufoPath = '/hipertipo/fonts/Escrow/Escrow-Roman/_ufos/opsz12_wdth100_wght400.ufo'

txt = 'acefgrstzj'

closedStart = [
    'J', 'S', 'T', 'Z',
    'a', 's', 'z', # 'j'
]
closedEnd   = [
    'C', 'E', 'F', 'G', 'L', 'S', 'T', 'Z',
    'c', 'e', 'r', 's', 't', 'z', 'g', 'f' 
]

x, y = 50, 200
s = 0.17
d = 0.2

c0 = 1,
c1 = Color.from_rgb(0.5, 0, 1) # Color.from_hsl(5, 1, 0.5)
c2 = Color.from_rgb(0, 1, 0.5) # c2.complementary_color()
c3 = 0,

minArea = 10000

# -----
# setup
# -----

f = OpenFont(ufoPath, showInterface=False)

glyphs = []
glyphBoxes = []
wordLength = 0

for i, char in enumerate(txt):
    glyphName = char # TODO: convert from unicode to PS name
    glyph = f[glyphName]
    glyphs.append(glyph)
    glyphBoxes.append(glyph.bounds)
    wordLength += glyph.width
    if i == 0:
        xStart = glyph.leftMargin
    if i == len(txt)-1:
        xEnd = glyph.rightMargin


yMin = 0 # max([b[1] for b in glyphBoxes])
yMax = f.info.xHeight # min([b[3] for b in glyphBoxes])

W = wordLength - xStart - xEnd
H = yMax - yMin

# -----
# draw!
# -----

size('A4Landscape')
fill(*c0)
rect(0, 0, width(), height())

translate(x, y)
scale(s)

fill(0)
save()
for i, glyph in enumerate(glyphs):
    _xMin, _yMin, _xMax, _yMax = glyphBoxes[i]
    with savedState():
        gWidth = RGlyph()
        Rect(gWidth.getPen(), 0, yMin, glyph.width, yMax-yMin)
        stroke(*c1)
        fill(*c1)
        drawGlyph(gWidth)
        gBox = RGlyph()
        Rect(gBox.getPen(), _xMin, yMin, _xMax-_xMin, yMax-yMin)
        gAlt = gBox % glyph
        for contour in gAlt:
            drawContour = True
            for p in contour.bPoints:
                if glyph.name not in closedStart and p.anchor[0] <= _xMin:
                    drawContour = False
                if glyph.name not in closedEnd and p.anchor[0] >= _xMax:
                    drawContour = False
            if drawContour:
                if contour.area > minArea:
                    # fill(*c2.darker(uniform(-d, d)).rgb)
                    fill(*c2.rgb)
                    drawGlyph(contour)
    translate(glyph.width, 0)
restore()

# draw glyph shapes
for i, glyph in enumerate(glyphs):
    fill(*c3)
    drawGlyph(glyph)
    translate(glyph.width, 0)

# saveImage('acefgrstzj_1.png')

