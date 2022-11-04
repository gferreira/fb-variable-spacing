# menuTitle: Spacing States tool

from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, shutil
from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView, PutFile, GetFile
from mojo import drawingTools as ctx

from variableSpacing import *
from variableSpacing.extras.hTools3_dialogs import *

# -------
# objects
# -------

class VariableSpacingTool(hDialog, BaseWindowController):
    '''
    A tool to enable multiple spacing states for the same set of glyph contours.

    '''
    spacingKey = KEY_SPACING
    kerningKey = KEY_KERNING
    font       = None
    verbose    = True

    def __init__(self):
        self.height  = self.textHeight*12
        self.height += self.padding*10
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
        self.w.newState = Button(
            (x, y, -p, self.textHeight),
            'create',
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
        self.w.exportStates = Button(
            (x, y, -p, self.textHeight),
            'export',
            callback=self.exportStatesCallback,
            sizeStyle='small')
        
        y += self.textHeight + p
        self.w.importStates = Button(
            (x, y, -p, self.textHeight),
            'import',
            callback=self.importStatesCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.generateState = Button(
            (x, y, -p, self.textHeight),
            'generate',
            callback=self.generateStateCallback,
            sizeStyle='small')

        y += self.textHeight + p
        self.w.preview = CheckBox(
            (x,  y, -p, self.textHeight),
            "show preview",
            value=True,
            sizeStyle='small',
            callback=self.updatePreviewCallback)

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
            print(f"creating new spacing state '{newStateName}'...")

        # add new state to font libs
        saveComponentsToLib(self.font)
        saveSpacingToLib(self.font, newStateName)
        saveKerningToLib(self.font, newStateName)

        # update list UI
        self.w.statesList.append(newStateName)

    def loadStateCallback(self, sender):
        '''
        Load the selected state from the lib into the font.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"loading spacing state '{self.currentState}' from the lib...")

        loadSpacingFromLib(self.font, self.currentState)
        loadKerningFromLib(self.font, self.currentState)

        UpdateCurrentGlyphView()

    def saveStateCallback(self, sender):
        '''
        Save the selected state to the font lib.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"saving spacing state '{self.currentState}' to the lib...")

        saveComponentsToLib(self.font)
        saveSpacingToLib(self.font, self.currentState)
        saveKerningToLib(self.font, self.currentState)

    def deleteStateCallback(self, sender):
        '''
        Delete the selected state from the font lib.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"deleting spacing state '{self.currentState}'...")

        deleteSpacingState(self.font, self.currentState)

        self.loadFontStates()

    def exportStatesCallback(self, sender):
        '''
        Export spacing states as an external JSON file.

        '''
        if self.font is None:
            return

        if self.verbose:
            print("exporting spacing states...")

        jsonFileName = 'spacingStates.json'
        jsonPath = PutFile(message='Save spacing states into JSON file:', fileName=jsonFileName)

        if jsonPath is None:
            if self.verbose:
                print('[cancelled]\n')
            return

        if os.path.exists(jsonPath):
            os.remove(jsonPath)

        if self.verbose:
            print(f'\tsaving {jsonPath}...')

        exportSpacingStates(self.font, jsonPath)

        if self.verbose:
            print('...done.\n')

    def importStatesCallback(self, sender):
        '''
        Import spacing states from external JSON file.

        '''
        if self.font is None:
            return

        if self.verbose:
            print("importing spacing states...")

        jsonPath = GetFile(message='Select JSON file with spacing states:')

        if self.verbose:
            print(f'\timporting data from {jsonPath}...')

        importSpacingStates(self.font, jsonPath)
        self.loadFontStates()

        if self.verbose:
            print('...done.\n')

    def generateStateCallback(self, sender):
        '''
        Generate the selected state as a separate font.

        '''
        if self.font is None:
            return

        if self.verbose:
            print(f"generating spacing state '{self.currentState}' as a separate UFO...")

        ufoPathSrc = self.font.path
        ufoPathDst = ufoPathSrc.replace('.ufo', f'_{self.currentState}.ufo')

        # if duplicate already exists, delete it
        if os.path.exists(ufoPathDst):
            shutil.rmtree(ufoPathDst)

        # duplicate UFO
        shutil.copytree(ufoPathSrc, ufoPathDst)
        if self.verbose:
            print(f"\tgenerating {ufoPathDst}...")

        # set font info in duplicate
        dstFont = OpenFont(ufoPathDst, showInterface=False)
        dstFont.info.styleName += f' {self.currentState.capitalize()}'

        # load spacing state
        loadSpacingFromLib(dstFont, self.currentState)
        loadKerningFromLib(dstFont, self.currentState)

        # clear spacing states
        deleteSpacingStatesLib(dstFont)

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
            xLeft = 0

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
        self.w.statesList.set(sorted(getSpacingStates(self.font)))

# -------
# testing
# -------

if __name__ == '__main__':

    OpenWindow(VariableSpacingTool)
