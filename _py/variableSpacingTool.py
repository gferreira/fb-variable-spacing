import os, shutil
from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from mojo import drawingTools as ctx
from hTools3.dialogs import *

'''

# ------------
# SPACING DICT
# ------------

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
}

# ------------
# KERNING DICT
# ------------

font.lib[f'{KEY}.kerning'] = {
    'default' : [
        ('public.kern1.A', 'public.kern2.V', -40),
        ('B', 'J', -20),
    ],
    'tight' : [],
}

'''

# -------
# globals
# -------

KEY = 'com.hipertipo.spacingaxis'

# ---------
# functions
# ---------

def deleteLib(font, key):
    '''
    Delete top-level lib with the given key from the font.

    '''
    if key in font.lib:
        del font.lib[key]

# saving

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
    # make kerning dict
    L = []
    for pair, value in font.kerning.items():
        g1, g2 = pair
        # pairKey = f'%{g1}%{g2}'
        L.append((g1, g2, value))
    # store kerning in lib
    if kerningKey not in font.lib:
        font.lib[kerningKey] = {}
    font.lib[kerningKey][name] = L

# loading

def loadSpacingFromLib(font, spacingKey, name):
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
    if not kerningKey in font.lib:
        return
    if not name in font.lib[kerningKey]:
        return
    font.kerning.clear()
    kerningDict = {(g1, g2): value for g1, g2, value in font.lib[kerningKey][name]}
    font.kerning.update(kerningDict)

# reading

def getSpacingLib(font, spacingKey):
    '''
    Return the spacing lib from a given font.

    '''
    if spacingKey in font.lib:
        return font.lib[spacingKey]
    else:
        return {}

def getKerningLib(font, kerningKey):
    '''
    Return the kerning lib from a given font.

    '''
    if kerningKey in font.lib:
        return font.lib[kerningKey]
    else:
        return {}

def getLibNames(font, KEY):
    spacingKey = f'{KEY}.spacing'
    kerningKey = f'{KEY}.kerning'
    spacingLib = []
    kerningLib = []
    if spacingKey in font.lib:
        if len(font.lib[spacingKey]):
            spacingLib += list(font.lib[spacingKey].keys())
    if kerningKey in font.lib:
        if len(font.lib[kerningKey]):
            kerningLib += list(font.lib[kerningKey].keys())
    return list(set(spacingLib + kerningLib))

def deleteSpacingState(font, KEY, stateName):
    '''
    Delete a given state from the spacing and kerning libs in a font.

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

# -------
# objects
# -------

class VariableSpacingTool(hDialog, BaseWindowController):

    spacingKey = f'{KEY}.spacing'
    kerningKey = f'{KEY}.kerning'
    spacingLib = {}
    kerningLib = {}
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
            # editCallback=self.editStateNameCallback,
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
        self.w.generateState = Button(
            (x, y, -p, self.textHeight),
            'generate',
            callback=self.generateStateCallback,
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
        selection = self.w.statesList.getSelection()
        if not selection:
            return
        selection = selection[0]
        items = self.w.statesList.get()
        if not len(items):
            return
        return items[selection]

    @property
    def synchronize(self):
        pass

    # ---------
    # callbacks
    # ---------

    def newStateCallback(self, sender):
        if self.font is None:
            return
        if self.verbose:
            print('creating new spacing state...', end=' ')

        statesList = self.w.statesList.get()

        if len(statesList) == 0:
            newStateName = 'default'
        elif 'default' in statesList and 'tight' not in statesList:
            newStateName = 'tight'
        elif 'default' in statesList and 'tight' in statesList:
            newStateName = 'loose'
        else:
            newStateName = 'new state'

        # update UI
        self.w.statesList.append(newStateName)

        # update internal dicts
        saveSpacingToLib(self.font, self.spacingKey, newStateName)
        saveKerningToLib(self.font, self.kerningKey, newStateName)
        if self.verbose:
            print('done.\n')

    def loadStateCallback(self, sender):
        print(f'loading spacing state {self.currentState}...', end=' ')
        loadSpacingFromLib(self.font, self.spacingKey, self.currentState)
        loadKerningFromLib(self.font, self.kerningKey, self.currentState)
        print('done.\n')

    def saveStateCallback(self, sender):
        if self.font is None:
            return
        if self.verbose:
            print(f'saving spacing state {self.currentState} in the lib...', end=' ')
        saveSpacingToLib(self.font, self.spacingKey, self.currentState)
        saveKerningToLib(self.font, self.kerningKey, self.currentState)
        if self.verbose:
            print('done.\n')

    # def editStateNameCallback(self, sender):
    #     itemsBefore  = set(self.spacingLib.keys())
    #     itemsAfter   = set(self.w.statesList.get())
    #     oldName = list(itemsBefore.difference(itemsAfter))
    #     if not len(oldName):
    #         return
    #     oldName = oldName[0]
    #     newName = self.currentState
    #     if newName is None:
    #         return
    #     if oldName == newName:
    #         return
    #     if newName in self.spacingLib:
    #         print('ERROR: please use unique names for spacing states\n')
    #         return 
    #     if self.verbose:
    #         print("renaming spacing state '{oldName}' to '{newName}...", end=' ')
    #     self.spacingLib[newName] = self.spacingLib[oldName]
    #     del self.spacingLib[oldName]
    #     # print(self.font.lib.keys())
    #     # self.font.lib[self.spacingKey][newName] = self.font.lib[self.spacingKey][oldName]
    #     # del self.font.lib[self.spacingKey][oldName]
    #     # print(self.font.lib.keys())

    def deleteStateCallback(self, sender):
        if self.font is None:
            return
        if self.verbose:
            print(f"deleting spacing state '{self.currentState}'...", end='')
        deleteSpacingState(self.font, KEY, self.currentState)
        if self.currentState in self.spacingLib:
            del self.spacingLib[self.currentState]
        if self.currentState in self.kerningLib:
            del self.kerningLib[self.currentState]
        self.loadFontStates()
        if self.verbose:
            print('done.\n')

    def generateStateCallback(self, sender):
        if self.font is None:
            return
        if self.verbose:
            print(f"generate source with spacing state '{self.currentState}'...")
        ufoPathSrc = self.font.path
        ufoPathDst = ufoPathSrc.replace('.ufo', f'_{self.currentState}.ufo')
        if os.path.exists(ufoPathDst):
            shutil.rmtree(ufoPathDst)
        shutil.copytree(ufoPathSrc, ufoPathDst)
        
        dstFont = OpenFont(ufoPathDst, showInterface=False)
        loadSpacingFromLib(dstFont, self.spacingKey, self.currentState)
        loadKerningFromLib(dstFont, self.kerningKey, self.currentState)
        dstFont.openInterface()

    def windowCloseCallback(self, sender):
        removeObserver(self, "drawBackground")
        # removeObserver(self, "drawPreview")
        # removeObserver(self, "viewDidChangeGlyph")
        # removeObserver(self, "spaceCenterDraw")
        removeObserver(self, 'fontBecameCurrent')
        removeObserver(self, 'fontDidClose')
        super().windowCloseCallback(sender)
        # unregisterRepresentationFactory(Glyph, f"{self.key}")
        # UpdateCurrentGlyphView()

    def updatePreviewCallback(self, sender):
        UpdateCurrentGlyphView()

    # ---------
    # observers
    # ---------

    def fontBecameCurrentCallback(self, notification):
        font = notification['font']
        self.font = font
        self.loadFontStates()
        # print(self.spacingLib.keys())
        # print(self.kerningLib.keys())

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

        scale = notification['scale']

        if not self.spacingKey in font.lib:
            return

        if not self.currentState in font.lib[self.spacingKey]:
            return
        
        if not glyph.name in font.lib[self.spacingKey][self.currentState]:
            return

        xMin, yMin, xMax, yMax = glyph.bounds
        glyphWidth = font.lib[self.spacingKey][self.currentState][glyph.name]['width']
        glyphLeft  = font.lib[self.spacingKey][self.currentState][glyph.name]['leftMargin']

        xLeft   = xMin - glyphLeft
        xRight  = xLeft + glyphWidth
        yBottom = -abs(font.info.descender)
        yTop    = font.info.ascender
        
        ctx.save()
        ctx.strokeWidth(3*scale)
        ctx.stroke(1, 0, 0)
        ctx.line((xLeft,  yBottom), (xLeft,  yTop))
        ctx.line((xRight, yBottom), (xRight, yTop))
        ctx.restore()

    # -------
    # methods
    # -------

    def loadFontStates(self):
        '''
        Load the font spacing states from the lib into the object dicts and UI.

        '''
        # no font open
        if self.font is None:
            self.w.statesList.set([])
            return
        # load spacing states from font lib
        self.w.statesList.set(sorted(getLibNames(self.font, KEY)))
        self.spacingLib = getSpacingLib(self.font, self.spacingKey)
        self.kerningLib = getKerningLib(self.font, self.kerningKey)

# -------
# testing
# -------

if __name__ == '__main__':

    OpenWindow(VariableSpacingTool)
    # f = CurrentFont()
    # deleteLib(f, f'{KEY}.spacing')
    # deleteLib(f, f'{KEY}.kerning')
    # saveSpacingToLib(f, KEY, 'default')
    # saveKerningToLib(f, KEY, 'default')
    # print(f.lib.keys())
    # print(f.lib[f'{KEY}.spacing'])
    # print()
    # print(f.lib[f'{KEY}.kerning'])
