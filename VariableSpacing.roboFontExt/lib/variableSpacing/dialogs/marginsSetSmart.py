from importlib import reload
# import hTools3.dialogs.glyphs.base
# reload(hTools3.dialogs.glyphs.base)
import variableSpacing 
reload(variableSpacing)

import math
from vanilla import RadioGroup, Button, CheckBox, EditText, TextBox
from mojo import drawingTools as ctx
from mojo.UI import NumberEditText
# from mojo.tools import IntersectGlyphWithLine
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from variableSpacing import saveComponentsToLib, getComponentsLib, smartSetMargins


class SmartSetMarginsDialog(GlyphsDialogBase):

    title = 'margins'
    key   = f'{GlyphsDialogBase.key}.marginsSmart'
    settings = {
        'left'       : True,
        'leftValue'  : 10,
        'right'      : True,
        'rightValue' : 10,
        'beamValue'  : 400,
    }

    def __init__(self):
        self.height = self.textHeight * 6
        self.height += self.padding * 7
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        self.w.leftLabel = TextBox(
                (x, y, col, self.textHeight),
                'left',
                sizeStyle=self.sizeStyle)

        self.w.leftValue = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['leftValue'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.rightLabel = TextBox(
                (x, y, col, self.textHeight),
                'right',
                sizeStyle=self.sizeStyle)

        self.w.rightValue = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['rightValue'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p - 1
        self.w.beam = CheckBox(
                (x, y, -p, self.textHeight),
                "use beam",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.beamLabel = TextBox(
                (x, y, col, self.textHeight),
                'beam',
                sizeStyle=self.sizeStyle)

        self.w.beamValue = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['beamValue'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.leftCheckbox = CheckBox(
                (x, y, self.width * 0.5 - p, self.textHeight),
                "left",
                value=self.settings['left'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        x += self.width * 0.5 - p
        self.w.rightCheckbox = CheckBox(
                (x, y, self.width * 0.5 - p, self.textHeight),
                "right",
                value=self.settings['right'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        x = p
        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "apply",
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        # y += self.textHeight + p
        # self.w.preview = CheckBox(
        #         (x, y, -p, self.textHeight),
        #         "show preview",
        #         value=True,
        #         callback=self.updatePreviewCallback,
        #         sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def left(self):
        return bool(self.w.leftCheckbox.get())

    @property
    def leftValue(self):
        return self.w.leftValue.get()

    @property
    def right(self):
        return bool(self.w.rightCheckbox.get())

    @property
    def rightValue(self):
        return self.w.rightValue.get()

    @property
    def beam(self):
        return bool(self.w.beam.get())

    @property
    def beamY(self):
        return self.w.beamValue.get()

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        pass

    # -------
    # methods
    # -------

    def assertGlyph(self, glyph):
        margins = self.getMargins(glyph)
        if margins is None:
            return False
        else:
            return True

    def getIntersections(self, glyph):
        intersections = sorted(IntersectGlyphWithLine(glyph, ((-10000, self.beamY), (10000, self.beamY)), canHaveComponent=True, addSideBearings=False))
        return intersections[0][0], intersections[-1][0]

    def getMargins(self, glyph):
        # use assertMargins(glyph) before calling this method to make sure it will not return `None`
        if self.beam:
            intersections = sorted(IntersectGlyphWithLine(glyph, ((-10000, self.beamY), (10000, self.beamY)), canHaveComponent=True, addSideBearings=False))
            if not len(intersections):
                return
            leftMargin  = intersections[0][0]
            rightMargin = glyph.width - intersections[-1][0]
            return leftMargin, rightMargin
        else:
            return glyph.leftMargin, glyph.rightMargin

    def apply(self):

        # assert conditions
        font = self.getCurrentFont()
        if not font:
            return
        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return
        if not (self.left or self.right):
            return

        # create components lib if it doesn't exist yet?
        saveComponentsToLib(font)

        # print info
        if self.verbose:
            print('setting margins smartly:\n')
            print(f'\tleft: {self.leftValue} ({self.left})')
            print(f'\tright: {self.rightValue} ({self.right})')
            print(f'\tbeam: {self.beamY} ({["OFF", "ON"][int(self.beam)]})')
            print(f'\tglyphs: {", ".join(glyphNames)}')
            print()

        leftMargin  = self.leftValue  if self.left  else None
        rightMargin = self.rightValue if self.right else None

        smartSetMargins(font, glyphNames, leftMargin=leftMargin, rightMargin=rightMargin, useBeam=self.beam, beamY=self.beamY, verbose=self.verbose)

        if self.verbose:
            print('...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    SmartSetMarginsDialog()
