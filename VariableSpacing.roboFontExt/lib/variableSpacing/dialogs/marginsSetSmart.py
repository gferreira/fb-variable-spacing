from importlib import reload
# import hTools3.dialogs.glyphs.base
# reload(hTools3.dialogs.glyphs.base)
import variableSpacing 
reload(variableSpacing)

import math
from vanilla import RadioGroup, Button, CheckBox, EditText, TextBox
from mojo import drawingTools as ctx
from mojo.UI import NumberEditText
from mojo.tools import IntersectGlyphWithLine
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from variableSpacing import saveComponentsToLib, getComponentsLib


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
        componentsDict = getComponentsLib(font)

        # print info
        if self.verbose:
            print('setting margins smartly:\n')
            print(f'\tleft: {self.leftValue} ({self.left})')
            print(f'\tright: {self.rightValue} ({self.right})')
            print(f'\tbeam: {self.beamY} ({["OFF", "ON"][int(self.beam)]})')
            print(f'\tglyphs: {", ".join(glyphNames)}')
            print()

        # --------------------------
        # contours only / skip empty
        # --------------------------

        print('\tglyphs with contours only:\n')
        print('\t\t', end='')
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
            print(glyphName, end=', ')
            glyph.prepareUndo('smart set margins')
            oldLeft,  oldRight  = glyph.leftMargin, glyph.rightMargin
            beamLeft, beamRight = self.getMargins(glyph)
            if self.left:
                leftValue = self.leftValue
                if self.beam:
                    leftValue -= beamLeft - oldLeft
                glyph.leftMargin = leftValue
            if self.right:
                rightValue = self.rightValue
                if self.beam:
                    rightValue -= beamRight - oldRight
                glyph.rightMargin = rightValue
            glyph.changed()
            glyph.performUndo()
        print('\n')

        # ---------------------------
        # mixed contours & components
        # ---------------------------

        print('\tglyphs with contours and components:\n')
        print('\t\t', end='')
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
            print(glyphName, end=', ')
            glyph.prepareUndo('smart set margins')
            # set left margin
            if self.left:
                glyph.leftMargin = self.leftValue
            # no glyphparts for glyph
            if glyphName not in componentsDict:
                # set right margin with no adjustments
                if self.right:
                    glyph.rightMargin = self.rightValue
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

            # set left margin
            if self.left:
                glyph.leftMargin = self.leftValue
            # set right margin
            if self.right:
                glyph.rightMargin = self.rightValue
            glyph.changed()
            glyph.performUndo()
        print('\n')

        # ----------------
        # components only
        # ----------------
        print('\tglyphs with components only:\n')
        print('\t\t', end='')
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
            print(glyphName, end=', ')
            glyph.prepareUndo('smart set margins')

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

            if self.left:
                leftValue = self.leftValue
                if self.beam:
                    leftValue -= beamLeft - oldLeft
                glyph.leftMargin = leftValue
                glyph.changed()
            if self.right:
                rightValue = self.rightValue
                if self.beam:
                    rightValue -= beamRight - oldRight
                glyph.rightMargin = rightValue
                glyph.changed()

            glyph.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    SmartSetMarginsDialog()
