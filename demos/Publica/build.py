import sys, os, shutil

folder = os.getcwd()

try:
    import variableSpacingLib
except:
    variableSpacingLibPath = os.path.join(os.path.dirname(os.path.dirname(folder)), 'code')
    sys.path.append(variableSpacingLibPath)
    import variableSpacingLib

import os 
from fontParts.world import OpenFont
from fontmake.font_project import FontProject
from variableSpacingLib import *

KEY = 'com.hipertipo.spacingaxis'
designspacePath = os.path.join(folder, 'Publica.designspace')
varFontPath = designspacePath.replace('.designspace', '.ttf')

# sources containing multiple spacing states to expand
spacingSources = [
    'Publica.ufo'
]

# build spacing sources
newSources = []
for src in spacingSources:
    srcPath = os.path.join(folder, src)
    srcFont = OpenFont(srcPath, showInterface=False)
    states = getStatesNames(srcFont, KEY)
    states.remove('default')
    for stateName in states:
        dstPath = srcPath.replace('.ufo', f'_{stateName}.ufo')
        # if duplicate already exists, delete it
        if os.path.exists(dstPath):
            shutil.rmtree(dstPath)
        # duplicate UFO
        shutil.copytree(srcPath, dstPath)
        # set font info in duplicate
        dstFont = OpenFont(dstPath, showInterface=False)
        dstFont.info.styleName += f' {stateName.capitalize()}'
        # load spacing state
        loadSpacingFromLib(dstFont, f'{KEY}.spacing', stateName)
        loadKerningFromLib(dstFont, f'{KEY}.kerning', stateName)
        # clear spacing states
        deleteLib(dstFont, KEY) 
        # done
        dstFont.save()
        dstFont.close()
    srcFont.close()
    newSources.append(dstPath)

# generate variable font
P = FontProject()
P.build_variable_font(designspacePath, output_path=varFontPath, verbose=True)

# clear spacing sources
for ufoPath in newSources:
    shutil.rmtree(ufoPath)
