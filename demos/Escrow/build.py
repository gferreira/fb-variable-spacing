import sys, os

folder = os.getcwd()

try:
    import variableSpacing
except:
    variableSpacingPath = os.path.join(os.path.dirname(os.path.dirname(folder)), 'code')
    sys.path.append(variableSpacingPath)
    import variableSpacing

import os 
from fontmake.font_project import FontProject
from variableSpacing import *

# build spacing sources
newSources = buildSpacingSources(folder)

# generate variable font
designspacePath = os.path.join(folder, 'Escrow.designspace')
varFontPath = designspacePath.replace('.designspace', '.ttf')
P = FontProject()
P.build_variable_font(designspacePath, output_path=varFontPath, verbose=True)

# clear spacing sources
for ufoPath in newSources:
    shutil.rmtree(ufoPath)
