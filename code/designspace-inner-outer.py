from importlib import reload
import variableSpacing.spacingAreas
reload(variableSpacing.spacingAreas)

from variableSpacing.spacingAreas import *

# --------
# settings
# --------

size('A4Landscape')
W, H = width(), height()
newDrawing()

designspacePath = '/hipertipo/tools/VariableSpacing/demos/Roboto/Roboto.designspace'

txt = 'AVATAR'

steps = 5
s     = 0.04
t     = -50
lh    = 1.25
upm   = 2048

x, y = 50, 0.8 * H

# L = dict(width=0, weight=400, spacing=0, contrast=0, slant=0)

parameters = {
    'scale'    : s,
    # 'location' : L,
    'glyphParameters' : {
        'color1'  : (0, 1, 0), # inner
        'color2'  : (1, 0, 0), # outer
        'color3'  : (1,),      # glyph
        'ySteps'  : 50,
        'yMin'    : 0,
        'yMax'    : 'capHeight',
        'xFactor' : 0.3,
        'dMax'    : 200, 
    }
}

# -----
# draw!
# -----

S = SpacingAreasLine(designspacePath)
S.setParameters(parameters)

newPage(W, H)
fill(1)
rect(0, 0, width(), height())

_y = y
for i in range(steps):
    spac = (i-2) * t * 4 / (steps-1)
    L = dict(weight=400, spacing=spac)
    S.location = L
    S.draw(txt, (x, _y))
    text(str(int(spac)), (x-30, _y))
    _y -= upm * s * lh



# saveImage('acefgrstzj_2.png')
