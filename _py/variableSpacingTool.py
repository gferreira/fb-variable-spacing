import os, shutil
from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from mojo import drawingTools as ctx
from hTools3.dialogs import *

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

    for glyphName in font.lib[spacingKey][name].keys():
        glyph = font[glyphName]

        if 'leftMargin' in font.lib[spacingKey][name][glyphName]:
            glyph.leftMargin = font.lib[spacingKey][name][glyphName]['leftMargin']

        glyph.width = font.lib[spacingKey][name][glyphName]['width']

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

# -------
# objects
# -------

class VariableSpacingTool(hDialog, BaseWindowController):
    '''
    A tool to enable multiple spacing states for the same set of glyph contours.

    '''
    spacingKey = f'{KEY}.spacing'
    kerningKey = f'{KEY}.kerning'
    font       = None
    verbose    = True

    def __init__(self):
        self.height  = self.textHeight*10
        self.height += self.padding*8
        self.w = FloatingWindow((self.width, self.height), "spacing")

        x = y = p = self.padding
        self.w.statesLabel = TextBox(
            (x,  y, -p, self.textHeight),
            "states",
            sizeStyle='small')

        y += self.textHeight
        self.w.statesList = List(
            (x, y, -p, self.textHeight*3),
            [],
            allowsEmptySelection=False,
            allowsMultipleSelection=False,
            enableDelete=True,
            drawFocusRing=False,
            selectionCallback=self.updatePreviewCallback)

        y += self.textHeight*3 + p
        self.w.preview = CheckBox(
            (x,  y, -p, self.textHeight),
            "preview",
            value=True,
            sizeStyle='small',
            callback=self.updatePreviewCallback)

        y += self.textHeight + p
        self.w.newState = Button(
            (x, y, -p, self.textHeight),
            'new',
            callback=self.newStateCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.loadState = Button(
            (x, y, -p, self.textHeight),
            'load',
            callback=self.loadStateCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.saveState = Button(
            (x, y, -p, self.textHeight),
            'save',
            callback=self.saveStateCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.deleteState = Button(
            (x, y, -p, self.textHeight),
            'delete',
            callback=self.deleteStateCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.exportState = Button(
            (x, y, -p, self.textHeight),
            'export',
            callback=self.exportStateCallback,
            sizeStyle='small')

        self.setUpBaseWindowBehavior()

        addObserver(self, "fontBecameCurrentCallback", "fontBecameCurrent")
        addObserver(self, "fontDidCloseCallback",      "fontDidClose")
        addObserver(self, "drawPreviewCallback",       "drawBackground")

        self.font = CurrentFont()
        self.loadFontStates()

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def currentState(self):
        '''
        Return the name of the spacing state which is currently selected in the UI.

        '''
        selection = self.w.statesList.getSelection()
        if not selection:
            return
        selection = selection[0]
        items = self.w.statesList.get()
        if not len(items):
            return
        return items[selection]

    # ---------
    # callbacks
    # ---------

    def newStateCallback(self, sender):
        '''
        Create a new spacing & kerning state in the current font.

        '''
        if self.font is None:
            return

        statesList = self.w.statesList.get()

        if len(statesList) == 0:
            newStateName = 'default'
        elif 'default' in statesList and 'tight' not in statesList:
            newStateName = 'tight'
        elif 'default' in statesList and 'tight' in statesList:
            newStateName = 'loose'
        else:
            newStateName = 'new state'

        if self.verbose:
            print(f"creating new spacing state '{newStateName}'...", end=' ')

        # add new empty state to font libs
        saveSpacingToLib(self.font, self.spacingKey, newStateName)
        saveKerningToLib(self.font, self.kerningKey, newStateName)

        # update list UI
        self.w.statesList.append(newStateName)

        if self.verbose:
            print('done.\n')

    def loadStateCallback(self, sender):
        '''
        Load the selected state from the lib into the font.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"loading spacing state '{self.currentState}' from the lib...", end=' ')

        loadSpacingFromLib(self.font, self.spacingKey, self.currentState)
        loadKerningFromLib(self.font, self.kerningKey, self.currentState)

        if self.verbose:
            print('done.\n')

        UpdateCurrentGlyphView()

    def saveStateCallback(self, sender):
        '''
        Save the selected state to the font lib.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"saving spacing state '{self.currentState}'' to the lib...", end=' ')

        saveSpacingToLib(self.font, self.spacingKey, self.currentState)
        saveKerningToLib(self.font, self.kerningKey, self.currentState)

        if self.verbose:
            print('done.\n')

    def deleteStateCallback(self, sender):
        '''
        Delete the selected state from the font lib.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"deleting spacing state '{self.currentState}'...", end='')

        deleteSpacingState(self.font, KEY, self.currentState)

        self.loadFontStates()

        if self.verbose:
            print('done.\n')

    def exportStateCallback(self, sender):
        '''
        Export the selected state as a separate font.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"exporting spacing state '{self.currentState}' as a separate UFO...")

        ufoPathSrc = self.font.path
        ufoPathDst = ufoPathSrc.replace('.ufo', f'_{self.currentState}.ufo')

        # if duplicate already exists, delete it
        if os.path.exists(ufoPathDst):
            shutil.rmtree(ufoPathDst)

        # duplicate UFO
        shutil.copytree(ufoPathSrc, ufoPathDst)
        if self.verbose:
            print(f"\tsaving '{ufoPathDst}'...")

        # set font info in duplicate
        dstFont = OpenFont(ufoPathDst, showInterface=False)
        dstFont.info.styleName += f' {self.currentState.capitalize()}'

        # load spacing state
        loadSpacingFromLib(dstFont, self.spacingKey, self.currentState)
        loadKerningFromLib(dstFont, self.kerningKey, self.currentState)

        # clear spacing states
        deleteLib(dstFont, KEY) 

        # done!
        dstFont.openInterface()
        if self.verbose:
            print('...done.\n')

    def windowCloseCallback(self, sender):
        '''
        Clear all observers when closing the tool.

        '''
        removeObserver(self, "drawBackground")
        removeObserver(self, 'fontBecameCurrent')
        removeObserver(self, 'fontDidClose')
        super().windowCloseCallback(sender)
        UpdateCurrentGlyphView()

    def updatePreviewCallback(self, sender):
        UpdateCurrentGlyphView()

    # ---------
    # observers
    # ---------

    def fontBecameCurrentCallback(self, notification):
        font = notification['font']
        self.font = font
        self.loadFontStates()

    def fontDidCloseCallback(self, notitication):
        self.font = CurrentFont()
        self.loadFontStates()

    def drawPreviewCallback(self, notification):

        if not self.w.preview.get():
            return

        # get glyph
        glyph = notification["glyph"]
        if glyph is None:
            return

        # get font
        font = glyph.font
        if font is None:
            return

        if not self.spacingKey in font.lib:
            return

        if not self.currentState in font.lib[self.spacingKey]:
            return
        
        if not glyph.name in font.lib[self.spacingKey][self.currentState]:
            return

        scale      = notification['scale']
        glyphWidth = font.lib[self.spacingKey][self.currentState][glyph.name]['width']
        yBottom    = -abs(font.info.descender)
        yTop       = font.info.ascender

        if 'leftMargin' in font.lib[self.spacingKey][self.currentState][glyph.name]:
            xMin, yMin, xMax, yMax = glyph.bounds
            glyphLeft = font.lib[self.spacingKey][self.currentState][glyph.name]['leftMargin']
            xLeft = xMin - glyphLeft
        else:
            xLeft = 0 # (glyph.width - glyphWidth) / 2

        xRight = xLeft + glyphWidth
        
        ctx.save()
        ctx.lineDash(3*scale, 3*scale)
        ctx.strokeWidth(2*scale)
        ctx.stroke(1, 0, 0)
        ctx.line((xLeft,  yBottom), (xLeft,  yTop))
        ctx.line((xRight, yBottom), (xRight, yTop))
        ctx.restore()

    # -------
    # methods
    # -------

    def loadFontStates(self):
        '''
        Load the names of the font spacing states from the lib into the UI.

        '''
        # no font open
        if self.font is None:
            self.w.statesList.set([])
            return
        # get states names from font lib
        self.w.statesList.set(sorted(getStatesNames(self.font, KEY)))

# -------
# testing
# -------

if __name__ == '__main__':

    OpenWindow(VariableSpacingTool)
