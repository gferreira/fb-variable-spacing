from importlib import reload
import variableSpacing.spacingAreas
reload(variableSpacing.spacingAreas)

from variableSpacing.spacingAreas import *

# --------
# settings
# --------

designspacePath = '/hipertipo/tools/VariableSpacing/demos/Roboto/Roboto.designspace'

L = dict(width=0, weight=400, spacing=0, contrast=0, slant=0)

x, y = 30, 440
s = 0.05
lh = 1.1
upm = 2048

txt = '''\
nhnmnuninjnln
noncnbndnpnqn
nanengnsnrnfntn
nvnwnknynxnzn
'''

parameters = {
    'scale'    : s,
    'location' : L,
    'glyphParameters' : {
        'color1'  : (1, 0.5, 0), # inner
        'color2'  : (0, 0.5, 1), # outer
        'color3'  : (0,),        # glyph
        'ySteps'  : 50,
        'yMin'    : 0,
        'yMax'    : 'xHeight',
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

for txtLine in txt.split('\n'):
    S = SpacingAreasLine(designspacePath)
    S.setParameters(parameters)
    S.draw(txtLine, (x, y))
    translate(0, -upm*s*lh)

# saveImage('acefgrstzj_2.png')
