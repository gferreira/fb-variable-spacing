from importlib import reload
import spacingAreasLib
reload(spacingAreasLib)

from spacingAreasLib import *

# --------
# settings
# --------

ufoPath = '/hipertipo/fonts/Escrow/Escrow-Roman/_ufos/opsz12_wdth100_wght400.ufo'

f = OpenFont(ufoPath, showInterface=False)

x, y = 40, 440
s = 0.1
lh = 1

txt = '''\
nhnmnuninjnln
noncnbndnpnqn
nanengnsnrnfntn
nvnwnknynxnzn
'''

parameters = {
    'scale' : s,
    'glyphParameters' : {
        'color1'  : (1, 0.5, 0), # inner
        'color2'  : (0, 0.5, 1), # outer
        'color3'  : (1,),        # glyph
        'ySteps'  : 50,
        'yMin'    : 0,
        'yMax'    : f.info.xHeight,
        'xFactor' : 0.3,
        'dMax'    : 150, 
    }
}

# -----
# draw!
# -----

size('A4Landscape')
fill(1)
rect(0, 0, width(), height())

for L in txt.split('\n'):
    S = SpacingAreasLine(f)
    S.setParameters(parameters)
    S.text = L
    S.draw((x, y))
    translate(0, -f.info.unitsPerEm*s*lh)

# saveImage('acefgrstzj_2.png')
