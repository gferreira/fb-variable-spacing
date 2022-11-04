from fontParts.world import OpenFont
from progvis.modules.DB.tools import drawGlyph
# from grapefruit import Color

ufoPath = '/hipertipo/tools/VariableSpacing/demos/Publica/Publica-55.ufo'

f = OpenFont(ufoPath, showInterface=False)
g = f['a']

s = 1.5
m = 0.6

colors = [
    (0.45,),
    (0.30,),
    (0.15,),
    (0.00,),
]

steps = 4

savePNG = False
saveSVG = False

# -----
# draw!
# -----

L, B, R, T = g.bounds
W = R-L
H = T-B

w, h = width(), height()

x0, y0 = w/2, h/2

c1 = 0, 0.8, 1 # , 1
c2 = 1, 1, 0.5
c3 = 1, 0.15, 0

print(c1[0]*255, c1[1]*255, c1[2]*255)

# linearGradient(
#     (0, 0), (w, 0),
#     [c1, c2, c1],
#     (0, 0.5, 1)
# )
fill(*c2)
rect(0, 0, w, h)

# color stripes
# with savedState():
#     for i in range(steps):
#         factor = (m + (steps-i-1)*(1.0-m)/(steps-1))
#         save()
#         translate((w - w*factor)/2, 0)
#         c = colors[i%steps]
#         fill(*c)
#         rect(0, 0, w*factor, h)
#         restore()

with savedState():
    translate(x0, (h -f.info.xHeight*s) / 2)
    scale(s)
    fill(0)
    translate(-W*0.51 -L, 0)
    drawGlyph(g)

D = 40
dx, dy = 90, 85

fill(*c3)
# rect(0, 0, D, h)
# rect(w-D, 0, D, h)
polygon((D, h/2), (D+dx, h/2 + dy), (D+dx, h/2 - dy))
polygon((w-D, h/2), (w-D-dx, h/2 + dy), (w-D-dx, h/2 - dy))

if savePNG:
    saveImage('VariableSpacingIcon.png', imageResolution=36)

if saveSVG:
    saveImage('VariableSpacingIcon.svg')
