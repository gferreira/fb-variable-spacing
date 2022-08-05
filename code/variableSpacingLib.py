
'''

# data format

font.lib[f'{KEY}.spacing'] = {
    'default' : {
        'space': {
            'width': 270,
        },
        'a': {
            'width': 543,
            'leftMargin': 75,
        },
    }
    'tight' : {},
    'loose' : {},
}

font.lib[f'{KEY}.kerning'] = {
    'default' : [
        ('public.kern1.A', 'public.kern2.V', -40),
        ('B', 'J', -20),
    ],
    'tight' : [],
    'loose' : [],
}

'''

KEY = 'com.hipertipo.spacingaxis'

# ---------
# functions
# ---------

# reading

def getStatesNames(font, KEY):
    '''
    Get the name of all spacing states available in the font.

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

def getSpacingLib(font, spacingKey):
    '''
    Get the spacing lib from a given font.

    '''
    if spacingKey in font.lib:
        return font.lib[spacingKey]
    else:
        return {}

def getKerningLib(font, kerningKey):
    '''
    Get the kerning lib from a given font.

    '''
    if kerningKey in font.lib:
        return font.lib[kerningKey]
    else:
        return {}

# writing

def saveSpacingToLib(font, spacingKey, name):
    '''
    Save the font’s spacing values (width, left margin) to the font lib.

    '''
    # make spacing dict
    D = {}
    for glyphName in font.glyphOrder:
        D[glyphName] = {}
        D[glyphName]['width'] = font[glyphName].width
        if font[glyphName].leftMargin is not None:
            D[glyphName]['leftMargin'] = font[glyphName].leftMargin

    # store spacing in lib
    if spacingKey not in font.lib:
        font.lib[spacingKey] = {}

    font.lib[spacingKey][name] = D

def saveKerningToLib(font, kerningKey, name):
    '''
    Save the font’s kerning values to the font lib.

    '''
    # make list of kerning pairs
    L = []
    for pair, value in font.kerning.items():
        g1, g2 = pair
        L.append((g1, g2, value))

    # store kerning in lib
    if kerningKey not in font.lib:
        font.lib[kerningKey] = {}

    font.lib[kerningKey][name] = L

# loading

def loadSpacingFromLib(font, spacingKey, name):
    '''
    Load spacing data for a given state from the lib into the font.

    '''
    if not spacingKey in font.lib:
        return

    if not name in font.lib[spacingKey]:
        return

    changedGlyphs = {}
    for glyphName in font.lib[spacingKey][name].keys():
        glyph = font[glyphName]
        if 'leftMargin' in font.lib[spacingKey][name][glyphName]:
            changedGlyphs[glyphName] = glyph.leftMargin
            glyph.leftMargin = font.lib[spacingKey][name][glyphName]['leftMargin']
        glyph.width = font.lib[spacingKey][name][glyphName]['width']

    # fix component positions
    for glyphName in font.glyphOrder:
        glyph = font[glyphName]
        if not len(glyph.components):
            continue
        for comp in glyph.components:
            baseGlyph = font[comp.baseGlyph]
            if comp.baseGlyph not in changedGlyphs:
                continue
            deltaX = changedGlyphs[glyphName] - font.lib[spacingKey][name][glyphName]['leftMargin']
            comp.moveBy((deltaX, 0))

def loadKerningFromLib(font, kerningKey, name):
    '''
    Load kerning data for a given state from the lib into the font.

    '''
    if not kerningKey in font.lib:
        return

    if not name in font.lib[kerningKey]:
        return

    font.kerning.clear()

    kerningDict = {(g1, g2): value for g1, g2, value in font.lib[kerningKey][name]}

    font.kerning.update(kerningDict)

# deleting

def deleteSpacingState(font, KEY, stateName):
    '''
    Delete a given state from the spacing and kerning libs in the font.

    '''
    # delete state from spacing lib
    spacingKey = f'{KEY}.spacing'
    if spacingKey in font.lib:
        if stateName in font.lib[spacingKey]:
            del font.lib[spacingKey][stateName]

    # delete state from kerning lib
    kerningKey = f'{KEY}.kerning'
    if kerningKey in font.lib:
        if stateName in font.lib[kerningKey]:
            del font.lib[kerningKey][stateName]

def deleteLib(font, key):
    '''
    Delete top-level font lib with the given key from the font.

    '''
    if key in font.lib:
        del font.lib[key]