from importlib import reload
import spacingLib
reload(spacingLib)

import drawBot as ctx
from spacingLib import *

# --------
# settings
# --------

ufoPath = '/hipertipo/fonts/Escrow/Escrow-Roman/_ufos/opsz12_wdth100_wght400.ufo'

f = OpenFont(ufoPath, showInterface=False)

x, y = 40, 240

parameters = {
    'text'  : 'agendsc',
    'scale' : 0.21,
    'glyphParameters' : {
        'color1'  : (0.5, 0, 1),
        'color2'  : (0, 1, 0.5),
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

S = SpacingWord(f)
S.setParameters(parameters)
S.draw((x, y))

# saveImage('acefgrstzj_2.png')
