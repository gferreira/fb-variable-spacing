import os, glob, shutil
from fontParts.world import OpenFont

__version__ = "0.1.2"

KEY = 'com.hipertipo.spacingaxis'

'''
SPACING STATES DATA FORMAT

1. SPACING LIB

font.lib[f'{KEY}.spacing'] = {
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

font.lib[f'{KEY}.kerning'] = {
    'default' : [
        ('public.kern1.A', 'public.kern2.V', -40),
        ('B', 'J', -20),
    ],
    'tight' : [],
    'loose' : [],
}

3. COMPONENTS LIB

font.lib[f'{KEY}.components'] = {
    'aacute' : [
        ('a', (65.0, -10.0)),
        ('acutecmb', (212.0, 581.0)),
    ]
    'dollar' : [
        ('S', (62.0, -10.0)),         # component
        ((225, 588), 'VyKpf7rL3q'),   # contour
        ((225, -115), 'ZpTeU9Jwwi'),
    ],
}

### OLD FORMAT (DEPRECATED)

font.lib[f'{KEY}.components'] = {
    'Aacute' : {
        'A' : (35.0, 0.0),           # component
        'acutecmb' : (281.0, 726.0), # component
    }
    'dollar' : {
        'S' : (62.0, -10.0),         # component
        'VyKpf7rL3q' : (225, 588),   # contour
        'ZpTeU9Jwwi' : (225, -115)   # contour
    },
}
'''

KEY_SPACING    = f'{KEY}.spacing'
KEY_KERNING    = f'{KEY}.kerning'
KEY_COMPONENTS = f'{KEY}.components'

# -------
# reading
# -------

def getSpacingStates(font, KEY=KEY):
    '''
    Get the name of all spacing states available in the font.

    ::
        
        >>> from variableSpacing import getStatesNames
        >>> spacingStates = getStatesNames(font)
        >>> print(spacingStates)
        ['default', 'loose', 'tight']

    '''
    spacingKey = f'{KEY}.spacing'
    kerningKey = f'{KEY}.kerning'

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

def getComponentsLib(font, spacingKey=KEY_COMPONENTS):
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
    if spacingKey in font.lib:
        return font.lib[spacingKey]
    else:
        return {}

# -------
# writing
# -------

def saveSpacingToLib(font, spacingState, spacingKey=KEY_SPACING, componentsKey=KEY_COMPONENTS, verbose=False):
    '''
    Save the font’s current spacing values (width, left margin) to the font lib.

    ::

        from variableSpacing import saveSpacingToLib
        font = CurrentFont()
        saveSpacingToLib(font, 'tight')

    '''
    # ------------
    # spacing dict
    # ------------

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

    # ---------------
    # components dict
    # ---------------
    
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

    # store component dict in lib (same for all states)
    if componentsKey not in font.lib:
        font.lib[componentsKey] = {}
    font.lib[componentsKey] = D

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
    if key in font.lib:
        del font.lib[key]

# ----------
# generating
# ----------

def buildSpacingSources(folder, prefix='_'):

    # get all ufo sources in folder
    sources = [ufo for ufo in glob.glob(f'{folder}/*.ufo') if prefix not in ufo]

    # keep a list of all new sources
    newSources = []

    for src in sources:
        srcPath = os.path.join(folder, src)
        srcFont = OpenFont(srcPath, showInterface=False)

        states = getStatesNames(srcFont, KEY)
        if 'default' in states:
            states.remove('default')

        if not len(states):
            continue

        ### make sure default state is loaded in primary source
        # loadSpacingFromLib(srcFont, f'{KEY}.spacing', 'default')
        # loadKerningFromLib(srcFont, f'{KEY}.kerning', 'default')
        # srcFont.save()

        for stateName in states:
            dstPath = srcPath.replace('.ufo', f'{prefix}{stateName}.ufo')
            # if duplicate already exists, delete it
            if os.path.exists(dstPath):
                shutil.rmtree(dstPath)
            # duplicate UFO source
            shutil.copytree(srcPath, dstPath)

            # set font info in duplicate
            dstFont = OpenFont(dstPath, showInterface=False)
            dstFont.info.styleName += f' {stateName.capitalize()}'

            # load spacing state
            loadSpacingFromLib(dstFont, stateName)
            loadKerningFromLib(dstFont, stateName)

            # clear spacing states from lib
            deleteLib(dstFont, KEY) 

            # done!
            dstFont.save()
            dstFont.close()
            newSources.append(dstPath)

        srcFont.close()

    return newSources

# ----------
# DEPRECATED
# ----------

def saveSpacingToLib_old(font, spacingState, spacingKey=KEY_SPACING, componentsKey=KEY_COMPONENTS, verbose=False):
    '''
    Save the font’s current spacing values (width, left margin) to the font lib.

    ::

        from variableSpacing import saveSpacingToLib
        font = CurrentFont()
        saveSpacingToLib(font, 'tight')

    '''
    # ------------
    # spacing dict
    # ------------

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

    # ---------------
    # components dict
    # ---------------
    
    D = {}
    for glyphName in font.glyphOrder:
        glyph = font[glyphName]
        if not len(glyph.components):
            continue

        # store offsets to shape origin (bounds)
        
        if verbose:
            print(f'saving component data for {glyphName} ...')

        glyphParts = {}

        for component in glyph.components:
            cx, cy = component.offset
            if font[component.baseGlyph].bounds is None:
                print(f'### empty component for {component.baseGlyph}')
                continue
            xMin, yMin, _, _ = font[component.baseGlyph].bounds
            dx = cx + xMin
            dy = cy + yMin
            compID = component.baseGlyph # component.getIdentifier()
            glyphParts[compID] = dx, dy

        for contour in glyph.contours:
            xMin, yMin, _, _ = contour.bounds
            contourID = contour.getIdentifier()
            glyphParts[contourID] = xMin, yMin

        if verbose:
            for k, v in glyphParts.items():
                print(f'\t{k} : {v}')

        D[glyphName] = glyphParts

        if verbose:
            print()

    # store component dict in lib (same for all states)
    if componentsKey not in font.lib:
        font.lib[componentsKey] = {}
    font.lib[componentsKey] = D

def loadSpacingFromLib_old(font, spacingState, spacingKey=KEY_SPACING, componentsKey=KEY_COMPONENTS, verbose=True):
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

        glyphParts = componentsDict[glyphName]

        # adjust component positions
        for comp in glyph.components:
            compID = comp.baseGlyph
            if compID not in glyphParts:
                continue
            else:
                cx, cy = comp.offset
                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds
                dx = xMin + cx
                dy = yMin + cy

                sx, sy = glyphParts[compID]
                diffx = sx - dx
                diffy = sy - dy

                comp.moveBy((diffx, diffy))

        # adjust contour positions
        for contour in glyph.contours:
            contourID = contour.getIdentifier()
            if contourID not in glyphParts:
                continue
            else:
                dx, dy, _, _ = contour.bounds
                sx, sy = glyphParts[contourID]
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
            
        glyphParts = componentsDict[glyphName] if glyphName in componentsDict else {}

        glyph.leftMargin = 0
        glyph.changed()

        for comp in glyph.components:
            compID = comp.baseGlyph # comp.getIdentifier()
            if compID not in glyphParts:
                continue
            else:
                cx, cy = comp.offset
                if comp.baseGlyph not in font:
                    continue
                baseGlyph = font[comp.baseGlyph]
                xMin, yMin, _, _ = baseGlyph.bounds
                # current position
                dx = xMin + cx
                dy = yMin + cy
                # saved position
                sx, sy = glyphParts[compID]
                
                diffx = sx - dx
                diffy = sy - dy

                if diffx == 0 and diffy == 0:
                    continue

                comp.moveBy((diffx, diffy))
                glyph.changed()
            
        if glyph.name not in spacingDict:
            continue

        leftMargin = spacingDict[glyph.name].get('leftMargin')
        if leftMargin is not None:
            glyph.leftMargin = leftMargin
            glyph.changed()

        glyphWidth = spacingDict[glyph.name].get('width')
        glyph.width = glyphWidth
        glyph.changed()

getStatesNames = getSpacingStates
deleteLib = deleteSpacingStatesLib
