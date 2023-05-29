from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo import drawingTools as ctx
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView, NumberEditText
from mojo.roboFont import RGlyph

from variableSpacing.spacingAreas import *
from variableSpacing.extras.hTools3_dialogs import *
from variableSpacing.extras.hTools3_spinnerSlider import SpinnerSlider
from variableSpacing.extras.hTools3_color import rgb2nscolor, nscolor2rgb

# ----------------
# global variables
# ----------------

KEY = 'previewSpacingAreas'

# ------------------------
# representation factories
# ------------------------

def factorySpacing(glyph, color1=(0.5, 0, 1, 0.5), color2=(0, 1, 0.5, 0.5), yMin=None, yMax=None, ySteps=40, dMax=None, xFactor=0.3):
    glyphParameters = {
        'color1'  : color1,
        'color2'  : color2,
        'ySteps'  : ySteps,
        'yMin'    : yMin,
        'yMax'    : yMax,
        'xFactor' : xFactor,
        'dMax'    : dMax,
    }
    G = SpacingAreasGlyph(glyph, ctx=ctx)
    G.setParameters(glyphParameters)
    return G

# -------
# objects
# -------

class PreviewSpacing(hDialog, BaseWindowController):

    key   = KEY
    title = 'spacing'

    glyphParameters = {
        'color1'  : (0.5, 0, 1, 0.5),
        'color2'  : (0, 1, 0.5, 0.5),
        'ySteps'  : 30,
        'yMax'    : None,
        'yMin'    : 0,
        'xFactor' : 0.3,
        'dMax'    : 150, 
    }

    yMinOptions = ['baseline', 'descender', 'box']
    yMaxOptions = ['xHeight', 'capHeight', 'ascender', 'box']

    def __init__(self):

        self.width  = 150
        self.height = self.textHeight*7
        self.height += self.padding*9

        self.w = self.window(
            (self.width, self.height),
            title=self.title,
        )

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        self.w.yMinLabel = TextBox(
                (x, y, col, self.textHeight),
                'y min',
                sizeStyle=self.sizeStyle)
        # y += self.textHeight
        self.w.yMin = PopUpButton(
                (col, y, -p, self.textHeight),
                self.yMinOptions,
                callback=self.updateViewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.yMaxLabel = TextBox(
                (x, y, col, self.textHeight),
                'y max',
                sizeStyle=self.sizeStyle)
        # y += self.textHeight
        self.w.yMax = PopUpButton(
                (col, y, -p, self.textHeight),
                self.yMaxOptions,
                callback=self.updateViewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p*1.5
        self.w.innerColorLabel = TextBox(
                (x, y, col, self.textHeight),
                'inner',
                sizeStyle=self.sizeStyle)
        self.w.innerColor = ColorWell(
                (col, y, -p, self.textHeight),
                color=rgb2nscolor(self.glyphParameters['color1']),
                # callback=self.savePreviewFillColorCallback
            )

        y += self.textHeight + p
        self.w.outerColorLabel = TextBox(
                (x, y, col, self.textHeight),
                'outer',
                sizeStyle=self.sizeStyle)
        self.w.outerColor = ColorWell(
                (col, y, -p, self.textHeight),
                color=rgb2nscolor(self.glyphParameters['color2']),
                # callback=self.savePreviewFillColorCallback
            )

        y += self.textHeight + p*1.5
        self.w.yStepsLabel = TextBox(
                (x, y, col, self.textHeight),
                'steps',
                sizeStyle=self.sizeStyle)
        self.w.ySteps = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.glyphParameters['ySteps'],
                callback=self.updateViewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.dmaxLabel = TextBox(
                (x, y, col, self.textHeight),
                'depth',
                sizeStyle=self.sizeStyle)
        self.w.dmax = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.glyphParameters['dMax'],
                callback=self.updateViewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                'show preview',
                value=True,
                callback=self.updateViewCallback,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()

        addObserver(self, "drawBackgroundObserver", "drawBackground")
        # addObserver(self, "drawPreviewObserver",    "drawPreview")
        addObserver(self, "updatePreviewObserver",  "viewDidChangeGlyph")
        addObserver(self, "drawSpaceCenterPreview", "spaceCenterDraw")

        registerRepresentationFactory(Glyph, f"{self.key}", factorySpacing)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def ySteps(self):
        return int(self.w.ySteps.get())

    @property
    def yMin(self):
        g = CurrentGlyph()
        if g is None:
            return
        i = self.w.yMin.get()
        yMinLabel = self.w.yMin.getItems()[i]
        yMinDict = {
            'baseline'  : 0,
            'descender' : g.font.info.ascender,
            'box'       : g.bounds[1],
        }
        return yMinDict[yMinLabel]

    @property
    def yMax(self):
        g = CurrentGlyph()
        if g is None:
            return
        i = self.w.yMax.get()
        yMaxLabel = self.w.yMax.getItems()[i]
        yMaxDict = {
            'xHeight'   : g.font.info.xHeight,
            'capHeight' : g.font.info.capHeight,
            'ascender'  : g.font.info.ascender,
            'box'       : g.bounds[3],
        }
        return yMaxDict[yMaxLabel]

    @property
    def dmax(self):
        return int(self.w.dmax.get())

    @property
    def innerColor(self):
        return nscolor2rgb(self.w.innerColor.get())

    @property
    def outerColor(self):
        return nscolor2rgb(self.w.outerColor.get())

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        removeObserver(self, "drawBackground")
        # removeObserver(self, "drawPreview")
        removeObserver(self, "viewDidChangeGlyph")
        removeObserver(self, "spaceCenterDraw")
        super().windowCloseCallback(sender)
        unregisterRepresentationFactory(Glyph, f"{self.key}")
        UpdateCurrentGlyphView()

    def updateViewCallback(self, sender):
        UpdateCurrentGlyphView()

    # ---------
    # observers
    # ---------

    def drawBackgroundObserver(self, notification):
        if not self.w.preview.get():
            return
        g = notification['glyph']
        s = notification['scale']
        if not len(g):
            return

        yMax = g.font.info.capHeight

        G = g.getRepresentation(f'{self.key}',
                yMin=self.yMin,
                yMax=self.yMax,
                ySteps=self.ySteps,
                dMax=self.dmax,
                xFactor=self.glyphParameters['xFactor'])

        ctx.fill(*self.outerColor)
        ctx.drawGlyph(G.leftSideGlyph)
        ctx.drawGlyph(G.rightSideGlyph)

        ctx.fill(*self.innerColor)
        ctx.drawGlyph(G.innerGlyph)

    def drawSpaceCenterPreview(self, notification):

        glyph = notification['glyph']

        font = glyph.font
        if font is None:
            return

        G = glyph.getRepresentation(f'{self.key}',
                yMin=self.yMin,
                yMax=self.yMax,
                ySteps=self.ySteps,
                dMax=self.dmax,
                xFactor=self.glyphParameters['xFactor'])

        ctx.fill(*self.outerColor)
        ctx.drawGlyph(G.leftSideGlyph)
        ctx.drawGlyph(G.rightSideGlyph)

        ctx.fill(*self.innerColor)
        ctx.drawGlyph(G.innerGlyph)

    def updatePreviewObserver(self, notification):
        glyph = notification['glyph']
        if glyph is None:
            return
        glyph.naked().dirty = True
        self.updatePreview()

    # -------
    # methods
    # -------

    def updatePreview(self):
        UpdateCurrentGlyphView()

# -------
# testing
# -------

if __name__ == '__main__':

    OpenWindow(PreviewSpacing)
