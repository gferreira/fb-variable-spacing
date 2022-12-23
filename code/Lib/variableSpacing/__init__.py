import os, glob, shutil, json
from fontParts.world import OpenFont

__version__ = "0.1.4"

'''
SPACING STATES DATA FORMAT
--------------------------

1. SPACING LIB

font.lib[KEY_SPACING] = {
    'default' : {
        'space': {
            'width': 270,
        },
        'a': {
            'width': 543,
            'leftMargin': 75,
        },
        'ntilde' : {
            'width': 620,
            'leftMargin': 96,
            'components' : {
                'n' : (0, 0),
                'tilde' : (110, 57),
            },
        },
    },
    'tight' : {},
    'loose' : {},
}

2. KERNING LIB

font.lib[KEY_KERNING] = {
    'default' : [
        ('public.kern1.A', 'public.kern2.V', -40),
        ('B', 'J', -20),
    ],
    'tight' : [],
    'loose' : [],
}
'''

KEY = 'com.hipertipo.spacingaxis'
KEY_SPACING = f'{KEY}.spacing'
KEY_KERNING = f'{KEY}.kerning'

# -------
# reading
# -------

def getSpacingStates(font, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING):
    '''
    Get the name of all spacing states available in the font.

    ::
        
        from variableSpacing import getSpacingStates
        spacingStates = getSpacingStates(font)
        print(spacingStates)
        >>> ['default', 'loose', 'tight']

    '''
    spacingLib = []
    if spacingKey in font.lib:
        if len(font.lib[spacingKey]):
            spacingLib += list(font.lib[spacingKey].keys())

    kerningLib = []
    if kerningKey in font.lib:
        if len(font.lib[kerningKey]):
            kerningLib += list(font.lib[kerningKey].keys())

    return list(set(spacingLib + kerningLib))

def getSpacingLib(font, spacingKey=KEY_SPACING):
    '''
    Get the spacing lib from a given font.

    ::

        from variableSpacing import getSpacingLib
        spacingLib = getSpacingLib(font)
        print(spacingLib.keys())
        >>> dict_keys(['default', 'tight'])
        print(spacingLib['default']['a'])
        >>> {'leftMargin': 65, 'width': 524}

    '''
    if spacingKey in font.lib:
        return font.lib[spacingKey]
    else:
        return {}

def getKerningLib(font, kerningKey=KEY_KERNING):
    '''
    Get the kerning lib from a given font.

    ::
    
        from variableSpacing import getKerningLib
        kerningLib = getKerningLib(font)
        print(kerningLib.keys())
        >>> dict_keys(['default', 'tight'])
        print(kerningLib['default'][0])
        >>> ['B', 'J', -20]

    '''
    if kerningKey in font.lib:
        return font.lib[kerningKey]
    else:
        return {}

# -------
# writing
# -------

def saveSpacingToLib(font, spacingState, spacingKey=KEY_SPACING, verbose=False):
    '''
    Save the font’s current spacing values (width, left margin) to the font lib.

    ::

        from variableSpacing import saveSpacingToLib
        font = CurrentFont()
        saveSpacingToLib(font, 'tight')

    '''
    # make spacing dict
    D = {}
    for glyphName in font.glyphOrder:
        if verbose:
            print(f'saving spacing data for {glyphName}...')
        glyph = font[glyphName]
        D[glyphName] = {}
        # store the advance widths of all glyphs
        D[glyphName]['width'] = glyph.width
        if verbose:
            print(f'\twidth: {glyph.width}')
        # store left margin of non-empty glyphs
        if glyph.leftMargin is not None:
            D[glyphName]['leftMargin'] = glyph.leftMargin
            if verbose:
                print(f'\tleft margin: {glyph.leftMargin}')
        if verbose:
            print()
    # store spacing dict in lib
    if spacingKey not in font.lib:
        font.lib[spacingKey] = {}
    font.lib[spacingKey][spacingState] = D

def saveKerningToLib(font, spacingState, kerningKey=KEY_KERNING):
    '''
    Save the font’s current kerning values to the font lib.

    ::

        from variableSpacing import saveKerningToLib
        font = CurrentFont()
        saveKerningToLib(font, 'tight')

    '''
    # make list of kerning pairs
    L = []
    for pair, value in font.kerning.items():
        g1, g2 = pair
        L.append((g1, g2, value))

    # store kerning in lib
    if kerningKey not in font.lib:
        font.lib[kerningKey] = {}

    font.lib[kerningKey][spacingState] = L

# -------
# loading
# -------

def collectGlyphsByType(font):
    '''
    Return the font's glyph names separated into four groups:

    - contours only
    - empty glyphs
    - components only
    - mixed contours & components

    ::

        from variableSpacing import collectGlyphsByType
        font = CurrentFont()
        contours, empty, components, mixed = collectGlyphsByType(f)
        print('glyphs with contours only:\n', ' '.join(contours), '\n')
        print('empty glyphs:\n', ' '.join(empty), '\n')
        print('glyphs with components only:\n', ' '.join(components), '\n')
        print('glyphs with contours and components:\n', ' '.join(mixed), '\n')

    '''
    glyphsContours = [
        glyphName for glyphName in font.glyphOrder
        if glyphName in font
        and not len(font[glyphName].components)
        and len(font[glyphName])
    ]
    glyphsEmpty = [
        glyphName for glyphName in font.glyphOrder
        if glyphName in font
        and not len(font[glyphName].components)
        and not len(font[glyphName])
    ]
    glyphsComponents = [
        glyphName for glyphName in font.glyphOrder
        if glyphName in font
        if len(font[glyphName].components)
        and not len(font[glyphName])
    ]
    glyphsMixed = [
        glyphName for glyphName in font.glyphOrder
        if glyphName in font
        if len(font[glyphName].components)
        and len(font[glyphName])
    ]
    return glyphsContours, glyphsEmpty, glyphsComponents, glyphsMixed
    
def loadSpacingFromLib(font, spacingState, spacingKey=KEY_SPACING, verbose=True):
    '''
    Load spacing data for a given state from the lib into the font.

    ::

        from variableSpacing import loadSpacingFromLib
        f = CurrentFont()
        loadSpacingFromLib(f, 'tight')

    '''
    print('loading spacing states...')

    if not spacingKey in font.lib:
        return

    if not spacingState in font.lib[spacingKey]:
        return

    spacingDict = font.lib[spacingKey][spacingState]

    # collect glyphs by type
    glyphsContours, glyphsEmpty, glyphsComponents, glyphsMixed = collectGlyphsByType(font)

    # ------------------
    # load glyph metrics
    # ------------------

    # empty glyphs
    for glyphName in glyphsEmpty:
        if glyphName not in spacingDict:
            continue
        # set glyph width
        font[glyphName].width = spacingDict[glyphName]['width']

    # glyphs with contours only
    for glyphName in glyphsContours:
        if glyphName not in spacingDict:
            continue
        # set left margin
        glyph = font[glyphName]
        leftValue = spacingDict[glyphName].get('leftMargin')
        if leftValue is not None:
            oldLeft  = glyph.leftMargin
            glyph.leftMargin = leftValue
            diff = oldLeft - leftValue
            # shift all components back
            for gName in glyphsComponents + glyphsMixed:
                for c in font[gName].components:
                    if c.baseGlyph == glyphName:
                        cx, cy = c.offset
                        c.offset = cx + diff, cy
        # set glyph width (right margin)
        glyph.width = spacingDict[glyphName]['width']

    # glyphs with components
    for glyphName in glyphsComponents + glyphsMixed:
        if glyphName not in spacingDict:
            continue
        # set left margin
        glyph = font[glyphName]
        leftValue = spacingDict[glyphName].get('leftMargin')
        if leftValue is not None:
            oldLeft  = glyph.leftMargin
            glyph.leftMargin = leftValue
            diff = oldLeft - leftValue
            # shift all components back
            for gName in glyphsComponents + glyphsMixed:
                for c in font[gName].components:
                    if c.baseGlyph == glyphName:
                        cx, cy = c.offset
                        c.offset = cx + diff, cy
        # set glyph width (right margin)
        glyph.width = spacingDict[glyphName]['width']

def loadKerningFromLib(font, spacingState, kerningKey=KEY_KERNING):
    '''
    Load kerning data for a given state from the lib into the font.

    ::

        from variableSpacing import loadKerningFromLib
        f = CurrentFont()
        loadKerningFromLib(f, 'tight')

    '''
    if not kerningKey in font.lib:
        return

    if not spacingState in font.lib[kerningKey]:
        return

    font.kerning.clear()

    # convert kerning format from tuple (json) into dict (font lib)
    kerningDict = {(g1, g2): value for g1, g2, value in font.lib[kerningKey][spacingState]}

    font.kerning.update(kerningDict)

# --------
# deleting
# --------

def deleteSpacingState(font, spacingState, KEY=KEY):
    '''
    Delete a given state from the spacing and kerning libs in the font.

    ::

        from variableSpacing import getSpacingStates, deleteSpacingState
        f = CurrentFont()
        print(getSpacingStates(f))
        >>> ['tight', 'default']
        deleteSpacingState(f, 'tight')
        print(getSpacingStates(f))
        >>> ['default']

    '''
    spacingKey = f'{KEY}.spacing'
    if spacingKey in font.lib:
        if spacingState in font.lib[spacingKey]:
            del font.lib[spacingKey][spacingState]

    kerningKey = f'{KEY}.kerning'
    if kerningKey in font.lib:
        if spacingState in font.lib[kerningKey]:
            del font.lib[kerningKey][spacingState]

def deleteSpacingStates(font, key=KEY):
    '''
    Delete top-level font libs with the given key prefix from the font.

    '''
    for k in font.lib.keys():
        if k.startswith(key):
            del font.lib[k]

# ----------
# generating
# ----------

def buildSpacingSources(folder, prefix='_', verbose=True):
    '''
    Build existing spacing states as separate UFO sources for variable font generation.

    ::

        from variableSpacing import buildSpacingSources
        folder = '/someFolder/'
        newSources = buildSpacingSources(folder, prefix='_SPAC-')
        # do something with the new sources, for example insert them into the designspace
        print(newSources)

    '''
    # get all ufo sources in folder
    sources = [ufo for ufo in glob.glob(f'{folder}/*.ufo') if prefix not in os.path.split(ufo)[-1]]

    # keep a list of all new sources
    newSources = []

    if verbose:
        print(f'building spacing sources in {folder}...')

    for src in sources:
        srcPath = os.path.join(folder, src)
        srcFont = OpenFont(srcPath, showInterface=False)

        states = getSpacingStates(srcFont)
        if 'default' in states:
            states.remove('default')

        if not len(states):
            continue

        ### we assume that the 'default' state is loaded
        # loadSpacingFromLib(srcFont, f'{KEY}.spacing', 'default')
        # loadKerningFromLib(srcFont, f'{KEY}.kerning', 'default')
        # srcFont.save()

        for stateName in states:
            dstPath = srcPath.replace('.ufo', f'{prefix}{stateName}.ufo')
            # if duplicate already exists, delete it
            if os.path.exists(dstPath):
                shutil.rmtree(dstPath)
            # duplicate UFO source
            if verbose:
                print(f"\tsaving spacing state '{stateName}' as {dstPath}...")
            shutil.copytree(srcPath, dstPath)

            # set font info in duplicate
            dstFont = OpenFont(dstPath, showInterface=False)
            dstFont.info.styleName += f' {stateName.capitalize()}'

            # load spacing state
            loadSpacingFromLib(dstFont, stateName)
            loadKerningFromLib(dstFont, stateName)

            # clear spacing states from lib
            deleteSpacingStates(dstFont) 

            # done!
            dstFont.save()
            dstFont.close()
            newSources.append(dstPath)

        srcFont.close()

    if verbose:
        print('...done.\n')

    return newSources

# -------------
# export/import
# -------------

def exportSpacingStates(font, jsonPath, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING):
    '''
    Export a font’s spacing states as an external JSON file.
    
    ::
    
        from variableSpacing import exportSpacingStates
        
        f = CurrentFont()
        jsonPath = f.path.replace('.ufo', '.json')
        exportSpacingStates(f, jsonPath)

    '''
    spacingLib = getSpacingLib(font, spacingKey=spacingKey)
    kerningLib = getKerningLib(font, kerningKey=kerningKey)

    spacingStates = {
        spacingKey : spacingLib,
        kerningKey : kerningLib,
    }

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(spacingStates, f, indent=2)

def importSpacingStates(font, jsonPath, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING):
    '''
    Import spacing states from an external JSON file into a font.

    ::
    
        from variableSpacing import importSpacingStates
        
        f = CurrentFont()
        jsonPath = f.path.replace('.ufo', '.json')
        importSpacingStates(f, jsonPath)

    '''
    with open(jsonPath, 'r', encoding='utf-8') as f:
        spacingStates = json.load(f)

    spacingLib = spacingStates.get(spacingKey)
    kerningLib = spacingStates.get(kerningKey)

    if spacingLib:
        font.lib[spacingKey] = spacingLib

    if kerningLib:
        font.lib[kerningKey] = kerningLib

# ------------
# transforming
# ------------

from fontParts.world import RGlyph
from fontPens.marginPen import MarginPen
from defcon.pens.transformPointPen import TransformPointPen
from defcon.objects.component import _defaultTransformation

class DecomposePointPen:
    '''
    A pen to decompose glyphs with components in Nonelab.

    Copied from ufoProcessor. Added support for `*args` and `**kwargs`.

    ::

        srcGlyph = CurrentGlyph()
        dstGlyph = RGlyph()
        pen = dstGlyph.getPointPen()
        decomposePen = DecomposePointPen(srcGlyph.font, pen)
        srcGlyph.drawPoints(decomposePen)
        dstGlyph.width = srcGlyph.width

    '''

    def __init__(self, glyphSet, outPointPen):
        self._glyphSet = glyphSet
        self._outPointPen = outPointPen
        self.beginPath = outPointPen.beginPath
        self.endPath = outPointPen.endPath
        self.addPoint = outPointPen.addPoint

    def addComponent(self, baseGlyphName, transformation, *args, **kwargs):
        if baseGlyphName in self._glyphSet:
            baseGlyph = self._glyphSet[baseGlyphName]
            if transformation == _defaultTransformation:
                baseGlyph.drawPoints(self)
            else:
                transformPointPen = TransformPointPen(self, transformation)
                baseGlyph.drawPoints(transformPointPen)

def getMargins(glyph, useBeam=False, beamY=400):
    if useBeam:
        # decompose glyph
        g = RGlyph()
        g.width = glyph.width
        pen = g.getPointPen()
        decomposePen = DecomposePointPen(glyph.font, pen)
        glyph.drawPoints(decomposePen)
        # get margins from flat copy
        pen = MarginPen({}, beamY, isHorizontal=True)
        g.draw(pen)
        intersections = pen.getAll()
        if not len(intersections):
            return
        leftMargin  = intersections[0]
        rightMargin = g.width - intersections[-1]
        return leftMargin, rightMargin
    else:
        return glyph.leftMargin, glyph.rightMargin

def setLeftMargin(glyph, leftMargin, leftMode, useBeam, beamLeft=None):
    if leftMargin is None:
        return
    oldLeft = glyph.leftMargin
    # mode 1: add / subtract
    if leftMode == 1: 
        leftValue = oldLeft + leftMargin
    # mode 2: percentage
    elif leftMode == 2: 
        leftValue = oldLeft * leftMargin / 100
    # mode 0: set equal to
    else: 
        leftValue = leftMargin
    # use beam to measure
    if useBeam and beamLeft:
        leftValue -= beamLeft - oldLeft
    # set left margin
    glyph.leftMargin = leftValue
    # return the difference
    return oldLeft - glyph.leftMargin

def setRightMargin(glyph, rightMargin, rightMode, useBeam, beamRight=None):
    if rightMargin is None:
        return 
    oldRight = glyph.rightMargin
    # add / subtract
    if rightMode == 1:
        rightValue = oldRight + rightMargin
    # percentage
    elif rightMode == 2: 
        rightValue = oldRight * rightMargin / 100
    # set equal to
    else: 
        rightValue = rightMargin
    # use beam to measure
    if useBeam and beamRight:
        rightValue -= beamRight - oldRight
    # set right margin
    glyph.rightMargin = rightValue
    # return the difference
    return oldRight - glyph.rightMargin

def smartSetMargins(font, glyphNames, leftMargin=None, rightMargin=None, leftMode=0, rightMode=0, useBeam=False, beamY=400, setUndo=True):
    '''
    Set left and right glyph margins while preserving their positions in components.

    ADD SPECIAL HANDLING FOR NEGATIVE MARGINS
    TO PREVENT NEGATIVE GLYPH WIDTHS AS RESULT

    '''
    glyphsContours, glyphsEmpty, glyphsComponents, glyphsMixed = collectGlyphsByType(font)

    # empty glyphs: do nothing

    # glyphs with contours only
    for glyphName in glyphsContours:
        glyph = font[glyphName]
        if useBeam:
            beamLeft, beamRight = getMargins(glyph, useBeam=useBeam, beamY=beamY)
        else:
            beamLeft = beamRight = None
        # set left margin
        if setUndo:
            glyph.prepareUndo('transform margins')
        diff = setLeftMargin(glyph, leftMargin, leftMode, useBeam, beamLeft)
        # shift all components back into position
        for gName in glyphsComponents + glyphsMixed:
            for c in font[gName].components:
                if c.baseGlyph == glyphName:
                    cx, cy = c.offset
                    c.offset = cx + diff, cy
        # set right margin
        setRightMargin(glyph, rightMargin, rightMode, useBeam, beamRight)
        if setUndo:
            glyph.performUndo()

    # glyphs with components
    for glyphName in glyphsComponents + glyphsMixed:
        glyph = font[glyphName]
        if useBeam:
            beamLeft, beamRight = getMargins(glyph, useBeam=useBeam, beamY=beamY)
        else:
            beamLeft = beamRight = None
        # set left margin
        if setUndo:
            glyph.prepareUndo('transform margins')
        diff = setLeftMargin(glyph, leftMargin, leftMode, useBeam, beamLeft)
        # shift all components back into position
        for gName in glyphsComponents + glyphsMixed:
            for c in font[gName].components:
                if c.baseGlyph == glyphName:
                    cx, cy = c.offset
                    c.offset = cx + diff, cy
        # set right margin
        setRightMargin(glyph, rightMargin, rightMode, useBeam, beamRight)
        if setUndo:
            glyph.performUndo()
