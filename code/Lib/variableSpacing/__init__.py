import os, glob, shutil, json
from fontParts.world import OpenFont

__version__ = "0.1.3"

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

3. COMPONENTS LIB

font.lib[KEY_COMPONENTS] = {
    'aacute' : [
        ('a', (65.0, -10.0)),          # component
        ('acutecmb', (212.0, 581.0)),  # component
    ]
    'dollar' : [
        ('S', (62.0, -10.0)),          # component
        ((225, 588), 'VyKpf7rL3q'),    # contour
        ((225, -115), 'ZpTeU9Jwwi'),   # contour
    ],
}
'''

KEY = 'com.hipertipo.spacingaxis'
KEY_SPACING    = f'{KEY}.spacing'
KEY_KERNING    = f'{KEY}.kerning'
KEY_COMPONENTS = f'{KEY}.components'

# -------
# reading
# -------

def getSpacingStates(font, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING):
    '''
    Get the name of all spacing states available in the font.

    ::
        
        >>> from variableSpacing import getSpacingStates
        >>> spacingStates = getSpacingStates(font)
        >>> print(spacingStates)
        ['default', 'loose', 'tight']

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

        >>> from variableSpacing import getSpacingLib
        >>> spacingLib = getSpacingLib(font)
        >>> print(spacingLib.keys())
        dict_keys(['default', 'tight'])
        >>> print(spacingLib['default']['a'])
        {'leftMargin': 65, 'width': 524}

    '''
    if spacingKey in font.lib:
        return font.lib[spacingKey]
    else:
        return {}

def getKerningLib(font, kerningKey=KEY_KERNING):
    '''
    Get the kerning lib from a given font.

    ::
    
        >>> from variableSpacing import getKerningLib
        >>> kerningLib = getKerningLib(font)
        >>> print(kerningLib.keys())
        dict_keys(['default', 'tight'])
        >>> print(kerningLib['default'][0])
        ['B', 'J', -20]

    '''
    if kerningKey in font.lib:
        return font.lib[kerningKey]
    else:
        return {}

def getComponentsLib(font, componentsKey=KEY_COMPONENTS):
    '''
    Get the components lib from a given font.

    ::

        >>> from variableSpacing import getComponentsLib
        >>> componentsLib = getComponentsLib(font)


        >>> print(componentsLib.keys())
        dict_keys(['default', 'tight'])
        >>> print(componentsLib['default']['a'])
        {'leftMargin': 65, 'width': 524}

    '''
    if componentsKey in font.lib:
        return font.lib[componentsKey]
    else:
        return {}

# -------
# writing
# -------

def saveComponentsToLib(font, componentsKey=KEY_COMPONENTS, verbose=False):
    '''
    Save relative positions between components in the font lib.

    ::

        from variableSpacing import saveComponentsToLib
        font = CurrentFont()
        saveComponentsToLib(font)

    '''
    # make components dict
    D = {}
    for glyphName in font.glyphOrder:
        glyph = font[glyphName]
        if not len(glyph.components):
            continue

        # store offsets to shape origin (bounds)
        if verbose:
            print(f'saving component data for {glyphName} ...')

        glyphParts = []
        for component in glyph.components:
            cx, cy = component.offset
            if font[component.baseGlyph].bounds is None:
                print(f'### empty component for {component.baseGlyph}')
                continue
            xMin, yMin, _, _ = font[component.baseGlyph].bounds
            dx = cx + xMin
            dy = cy + yMin
            # compID = component.getIdentifier() 
            # this doesn’t work because accented glyphs are often
            # re-composed, and this resets the component IDs
            # we need to identify components by base glyph instead
            compID = component.baseGlyph 
            glyphParts.append((compID, (dx, dy)))

        for contour in glyph.contours:
            xMin, yMin, _, _ = contour.bounds
            contourID = contour.getIdentifier()
            glyphParts.append(((xMin, yMin), contourID))

        if verbose:
            for entry in glyphParts:
                print(f"\t{parts.join(' ')}")

        D[glyphName] = glyphParts

        if verbose:
            print()

    # store component dict in lib (independent of any states)
    if componentsKey not in font.lib:
        font.lib[componentsKey] = {}
    font.lib[componentsKey] = D

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

def loadSpacingFromLib(font, spacingState, spacingKey=KEY_SPACING, componentsKey=KEY_COMPONENTS, verbose=True):
    '''
    Load spacing data for a given state from the lib into the font.

    '''
    if not spacingKey in font.lib:
        return

    if not spacingState in font.lib[spacingKey]:
        return

    spacingDict    = font.lib[spacingKey][spacingState]
    componentsDict = font.lib[componentsKey] if componentsKey in font.lib else {}

    # ----------------------------
    # contours only / empty glyphs
    # ----------------------------

    for glyphName in font.glyphOrder:
        if glyphName not in font:
            continue
        glyph = font[glyphName]
        if len(glyph.components):
            continue
        if glyphName not in spacingDict:
            continue
        if 'leftMargin' in spacingDict[glyphName]:
            glyph.leftMargin = spacingDict[glyphName]['leftMargin']
        glyph.width = spacingDict[glyphName]['width']
        glyph.changed()

    # ---------------------------
    # mixed contours & components
    # ---------------------------

    for glyphName in font.glyphOrder:
        if glyphName not in font:
            continue
        glyph = font[glyphName]
        # skip glyphs without components
        if not len(glyph.components):
            continue
        # skip empty glyphs
        if not glyph.bounds:
            continue
        # skip glyphs with no contours
        if not len(glyph.contours):
            continue

        if glyphName not in componentsDict:
            continue
        glyphParts = componentsDict[glyphName]
        assert type(glyphParts) is list

        # adjust component positions

        componentsUsed = []
        for comp in glyph.components:
            # find data for component
            for i, item in enumerate(glyphParts):
                # if the item does not start with a string, it’s not a component (but a contour)
                if type(item[0]) is not str:
                    continue
                # match item to component
                if comp.baseGlyph != item[0]:
                    continue
                # it’s possible to have multiple components of the same base glyph
                # each instance has its own entry
                # this makes sure that we only use each item once
                if i in componentsUsed:
                    continue

                cx, cy = comp.offset
                if comp.baseGlyph not in font:
                    continue
                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds
                dx = xMin + cx
                dy = yMin + cy

                sx, sy = item[1]
                diffx = sx - dx
                diffy = sy - dy

                componentsUsed.append(i)

                if diffx == 0 and diffy == 0:
                    continue

                comp.moveBy((diffx, diffy))
                break

        # adjust contour positions
        for contour in glyph.contours:
            contourID = contour.getIdentifier()

            for i, item in enumerate(glyphParts):
                # if the item does not start with a tuple, it’s not a contour (but a component)
                if type(item[0]) is not tuple:
                    continue

                # match item to contour
                if contourID != item[1]:
                    continue

                dx, dy, _, _ = contour.bounds
                sx, sy = item[0]
                diffx = sx - dx
                diffy = sy - dy
                contour.moveBy((diffx, diffy))
        
        glyph.changed()

        leftMargin = spacingDict[glyph.name].get('leftMargin')
        if leftMargin is not None:
            glyph.leftMargin = leftMargin
            glyph.changed()

        glyphWidth = spacingDict[glyph.name].get('width')
        glyph.width = glyphWidth
        glyph.changed()

    # ---------------
    # components only
    # ---------------

    for glyphName in font.glyphOrder:
        if glyphName not in font:
            continue
        glyph = font[glyphName]
        # skip glyphs without components
        if not len(glyph.components):
            continue
        # skip empty glyphs
        if not glyph.bounds:
            continue
        # skip glyphs with contours
        if len(glyph.contours):
            continue
            
        glyphParts = componentsDict[glyphName] if glyphName in componentsDict else []
        assert type(glyphParts) is list

        glyph.leftMargin = 0
        glyph.changed()

        componentsUsed = []
        for comp in glyph.components:
            # find data for component
            for i, item in enumerate(glyphParts):
                # if the item does not start with a string, it’s not a component (but a contour)
                if type(item[0]) is not str:
                    continue
                # match item to component
                if comp.baseGlyph != item[0]:
                    continue
                # it’s possible to have multiple components of the same base glyph
                # each instance has its own entry
                # this makes sure that we only use each item once
                if i in componentsUsed:
                    continue

                cx, cy = comp.offset
                if comp.baseGlyph not in font:
                    continue

                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds
                # current position
                dx = xMin + cx
                dy = yMin + cy
                # saved position
                sx, sy = item[1]
                
                diffx = sx - dx
                diffy = sy - dy

                componentsUsed.append(i)

                if diffx == 0 and diffy == 0:
                    continue

                comp.moveBy((diffx, diffy))
                glyph.changed()
                break
            
        if glyph.name not in spacingDict:
            continue

        leftMargin = spacingDict[glyph.name].get('leftMargin')
        if leftMargin is not None:
            glyph.leftMargin = leftMargin
            glyph.changed()

        glyphWidth = spacingDict[glyph.name].get('width')
        glyph.width = glyphWidth
        glyph.changed()

def loadKerningFromLib(font, spacingState, kerningKey=KEY_KERNING):
    '''
    Load kerning data for a given state from the lib into the font.

    '''
    if not kerningKey in font.lib:
        return

    if not spacingState in font.lib[kerningKey]:
        return

    font.kerning.clear()

    kerningDict = {(g1, g2): value for g1, g2, value in font.lib[kerningKey][spacingState]}

    font.kerning.update(kerningDict)

# --------
# deleting
# --------

def deleteSpacingState(font, spacingState, KEY=KEY):
    '''
    Delete a given state from the spacing and kerning libs in the font.

    '''
    # delete state from spacing lib
    spacingKey = f'{KEY}.spacing'
    if spacingKey in font.lib:
        if spacingState in font.lib[spacingKey]:
            del font.lib[spacingKey][spacingState]

    # delete state from kerning lib
    kerningKey = f'{KEY}.kerning'
    if kerningKey in font.lib:
        if spacingState in font.lib[kerningKey]:
            del font.lib[kerningKey][spacingState]

def deleteSpacingStatesLib(font, key=KEY):
    '''
    Delete top-level font lib with the given key from the font.

    '''
    for k in font.lib.keys():
        if k.startswith(key):
            del font.lib[k]

deleteSpacingStates = deleteSpacingStatesLib

# ----------
# generating
# ----------

def buildSpacingSources(folder, prefix='_', verbose=True):

    ### TO-DO: add support for subfolders

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

        ### make sure the default state is loaded in the primary source
        ### WELL… let’s simply assume it is :)
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

def exportSpacingStates(font, jsonPath, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING, componentsKey=KEY_COMPONENTS):
    '''
    Export a font’s spacing states as an external JSON file.
    
    '''
    spacingLib    = getSpacingLib(font, spacingKey=spacingKey)
    kerningLib    = getKerningLib(font, kerningKey=kerningKey)
    componentsLib = getComponentsLib(font, componentsKey=componentsKey)

    spacingStates = {
        spacingKey    : spacingLib,
        kerningKey    : kerningLib,
        componentsKey : componentsLib,
    }

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(spacingStates, f, indent=2)

def importSpacingStates(font, jsonPath, spacingKey=KEY_SPACING, kerningKey=KEY_KERNING, componentsKey=KEY_COMPONENTS):
    '''
    Import spacing states from an external JSON file into a font.
    
    '''
    with open(jsonPath, 'r', encoding='utf-8') as f:
        spacingStates = json.load(f)

    spacingLib    = spacingStates.get(spacingKey)
    kerningLib    = spacingStates.get(kerningKey)
    componentsLib = spacingStates.get(componentsKey)

    if spacingLib:
        font.lib[spacingKey] = spacingLib

    if kerningLib:
        font.lib[kerningKey] = kerningLib

    if componentsLib:
        font.lib[componentsKey] = componentsLib

# ------------
# transforming
# ------------

from fontPens.marginPen import MarginPen
from fontParts.world import RGlyph
from hTools3.modules.pens import DecomposePointPen

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

def smartSetMargins(font, glyphNames, leftMargin=None, rightMargin=None, useBeam=False, beamY=400, verbose=True, setUndo=True):

    # TO-DO: plain margins and margins with beam must be set in one go!

    componentsDict = getComponentsLib(font)

    # --------------------------
    # contours only / skip empty
    # --------------------------

    if verbose:
        print('glyphs with contours only:\n')

    for glyphName in glyphNames:
        glyph = font[glyphName]

        # skip glyphs with components
        if len(glyph.components):
            continue
        # skip empty glyphs
        if not glyph.bounds:
            continue
        # skip zero-width glyphs
        if glyph.width == 0:
            continue

        if verbose:
            print(glyphName, end=', ')

        if setUndo:
            glyph.prepareUndo('smart set margins')
        oldLeft,  oldRight  = glyph.leftMargin, glyph.rightMargin
        beamLeft, beamRight = getMargins(glyph, useBeam=useBeam, beamY=beamY)

        # set left margin
        if leftMargin is not None:
            leftValue = leftMargin
            if useBeam:
                leftValue -= beamLeft - oldLeft
            glyph.leftMargin = leftValue

        # set right margin
        if rightMargin is not None:
            rightValue = rightMargin
            if useBeam:
                rightValue -= beamRight - oldRight
            glyph.rightMargin = rightValue

        glyph.changed()
        if setUndo:
            glyph.performUndo()

    if verbose:
        print('\n')

    # ---------------------------
    # mixed contours & components
    # ---------------------------

    if verbose:
        print('glyphs with contours and components:\n')

    for glyphName in glyphNames:
        glyph = font[glyphName]

        # skip glyphs with no components
        if not len(glyph.components):
            continue

        # skip empty glyphs
        if not glyph.bounds:
            continue

        # skip zero-width glyphs
        if glyph.width == 0:
            continue

        # skip glyphs with no contours
        if not len(glyph.contours):
            continue

        if verbose:
            print(glyphName, end=', ')

        if setUndo:
            glyph.prepareUndo('smart set margins')
        oldLeft,  oldRight  = glyph.leftMargin, glyph.rightMargin
        beamLeft, beamRight = getMargins(glyph, useBeam=useBeam, beamY=beamY)

        # set left margin
        if leftMargin is not None:
            leftValue = leftMargin
            if useBeam:
                leftValue -= beamLeft - oldLeft
            glyph.leftMargin = leftValue

        # no glyphparts entry for glyph
        if glyphName not in componentsDict:
            # set right margin without any adjustment
            if rightMargin is not None:
                glyph.rightMargin = rightMargin
            # move on to the next glyph
            continue

        # adjust component positions
        glyphParts = componentsDict[glyphName]
        assert type(glyphParts) is list

        componentsUsed = []
        for comp in glyph.components:
            # find data for component
            for i, item in enumerate(glyphParts):
                # if the item does not start with a string, it’s not a component but a contour
                if type(item[0]) is not str:
                    continue

                # match item to component
                if comp.baseGlyph != item[0]:
                    continue

                # it’s possible to have multiple components of the same base glyph
                # each instance has its own entry; this makes sure that we only use each item once
                if i in componentsUsed:
                    continue

                cx, cy = comp.offset
                if comp.baseGlyph not in font:
                    continue

                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds
                dx = xMin + cx
                dy = yMin + cy
                sx, sy = item[1]
                diffx = sx - dx
                diffy = sy - dy
                componentsUsed.append(i)
                if diffx == 0 and diffy == 0:
                    continue
                comp.moveBy((diffx, diffy))
                break

        # adjust contour positions
        for contour in glyph.contours:
            contourID = contour.getIdentifier()
            for i, item in enumerate(glyphParts):
                # if the item does not start with a tuple, it’s not a contour (but a component)
                if type(item[0]) is not tuple:
                    continue

                # match item to contour
                if contourID != item[1]:
                    continue

                dx, dy, _, _ = contour.bounds
                sx, sy = item[0]
                diffx = sx - dx
                diffy = sy - dy
                contour.moveBy((diffx, diffy))

        glyph.changed()

        # set left margin
        if leftMargin is not None:
            glyph.leftMargin = leftValue

        # set right margin
        if rightMargin is not None:
            rightValue = rightMargin
            if useBeam:
                rightValue -= beamRight - oldRight
            glyph.rightMargin = rightValue

        glyph.changed()
        if setUndo:
            glyph.performUndo()

    if verbose:
        print('\n')

    # ----------------
    # components only
    # ----------------
    if verbose:
        print('glyphs with components only:\n')

    for glyphName in glyphNames:
        glyph = font[glyphName]

        # skip glyphs without components
        if not len(glyph.components):
            continue

        # skip empty glyphs
        if not glyph.bounds:
            continue

        # skip zero-width glyphs
        if glyph.width == 0:
            continue

        # skip glyphs with contours
        if len(glyph.contours):
            continue

        if verbose:
            print(glyphName, end=', ')
        if setUndo:
            glyph.prepareUndo('smart set margins')
        oldLeft,  oldRight  = glyph.leftMargin, glyph.rightMargin
        beamLeft, beamRight = getMargins(glyph, useBeam=useBeam, beamY=beamY)

        glyphParts = componentsDict[glyphName] if glyphName in componentsDict else []
        assert type(glyphParts) is list

        glyph.leftMargin = 0
        glyph.changed()

        componentsUsed = []
        for comp in glyph.components:
            # find data for component
            for i, item in enumerate(glyphParts):

                # if the item does not start with a string, it’s not a component (but a contour)
                if type(item[0]) is not str:
                    continue

                # match item to component
                if comp.baseGlyph != item[0]:
                    continue

                # it’s possible to have multiple components of the same base glyph
                # each instance has its own entry
                # this makes sure that we only use each item once
                if i in componentsUsed:
                    continue
                cx, cy = comp.offset
                if comp.baseGlyph not in font:
                    continue

                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds

                # current position
                dx = xMin + cx
                dy = yMin + cy

                # saved position
                sx, sy = item[1]
                diffx = sx - dx
                diffy = sy - dy
                componentsUsed.append(i)
                if diffx == 0 and diffy == 0:
                    continue

                # update component position
                comp.moveBy((diffx, diffy))
                glyph.changed()
                break

        if leftMargin is not None:
            leftValue = leftMargin
            if useBeam:
                leftValue -= beamLeft - oldLeft
            glyph.leftMargin = leftValue
            glyph.changed()

        if rightMargin:
            rightValue = rightMargin
            if useBeam:
                rightValue -= beamRight - oldRight
            glyph.rightMargin = rightValue
            glyph.changed()

        if setUndo:
            glyph.performUndo()

    # done
    font.changed()
