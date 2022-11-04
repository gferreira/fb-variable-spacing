import sys

# ufoProcessor is not embedded in DrawBot
try:
    import ufoProcessor
except:
    # http://github.com/LettError/ufoProcessor
    ufoProcessorPath = '/_code/ufoProcessor/Lib'
    sys.path.append(ufoProcessorPath)
    import ufoProcessor

import drawBot
from defcon.pens.transformPointPen import TransformPointPen
from defcon.objects.component import _defaultTransformation
from ufoProcessor import DesignSpaceProcessor, Location
from fontTools.agl import UV2AGL
from fontParts.world import RGlyph


def drawGlyph(g):
    bez = drawBot.BezierPath()
    g.draw(bez)
    drawBot.drawPath(bez)


class DecomposePointPen(object):

    # copied from ufoProcessor
    # added support for *args and **kwargs

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


class SpacingSetter:

    '''
    An object to visualize horizontal glyph metrics in a string of text.
    The object takes a UFO designspace as input.
    It can output an image showing glyphs, widths and kerning.

    '''

    fontInfo      = {}
    kerning       = {}
    glyphs        = {}
    glyphNames    = []

    useKerning    = True
    drawGlyphs    = True
    drawKerning   = True
    drawWidths    = True
    drawTracking  = False
    drawBoxes     = True

    tracking      = 0          # as a percentage % of em

    colorKerning  = 0.5,
    colorBox      = 0.8,
    colorMargins  = 1, 0, 0
    colorGlyphs   = 0,
    colorTracking = 1, 1, 0

    captionSize   = 120

    def __init__(self, designspacePath, ctx=drawBot):
        self.designspacePath = designspacePath
        self.ctx = ctx

    def draw(self, text, pos, scale, locationDict):
        '''
        Set a given string of text  at a given position and scale,
        in the designspace instance defined by the given location.
        
        '''
        x, y = pos

        doc = DesignSpaceProcessor()
        doc.read(self.designspacePath)
        doc.loadFonts()

        location = Location(**locationDict)

        # convert unicode to psnames
        self.glyphNames = [UV2AGL.get(ord(char)) for char in text] 

        # interpolate font info
        fontInfoMutator = doc.getInfoMutator()
        self.fontInfo = fontInfoMutator.makeInstance(location)

        tracking = self.fontInfo.unitsPerEm / 1000 * self.tracking

        # interpolate kerning
        if self.useKerning:
            pairs = []
            for i, glyphName in enumerate(self.glyphNames):
                if i == 0:
                    continue
                pairs.append((self.glyphNames[i-1], glyphName))
            kerningMutator = doc.getKerningMutator(pairs)
            self.kerning = kerningMutator.makeInstance(location)

        # interpolate glyphs
        self.glyphs = {}
        for glyphName in self.glyphNames:
            if glyphName in self.glyphs:
                continue
            glyphMutator = doc.getGlyphMutator(glyphName)
            instanceGlyph = glyphMutator.makeInstance(location)
            for comp in instanceGlyph.components:
                compName = comp['baseGlyph']
                if compName not in self.glyphs:
                    compGlyphMutator = doc.getGlyphMutator(compName)
                    compGlyph = compGlyphMutator.makeInstance(location)
                    self.glyphs[compName] = compGlyph
            g = RGlyph()
            pointPen = g.getPointPen()
            decomposePen = DecomposePointPen(self.glyphs, pointPen)
            instanceGlyph.drawPoints(decomposePen)
            g.width = instanceGlyph.width
            self.glyphs[glyphName] = g

        # -----
        # draw!
        # -----

        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(scale)

        # draw glyph boxes
        if self.drawBoxes or self.drawTracking:
            self.ctx.save()
            for i, glyphName in enumerate(self.glyphNames):
                g = self.glyphs[glyphName]
                if self.useKerning and i > 0:
                    pair = self.glyphNames[i-1], glyphName
                    kernValue = self.kerning.get(pair)
                    if kernValue:
                        self.ctx.translate(kernValue, 0)
                if self.drawBoxes:
                    self.ctx.fill(*self.colorBox)
                    self.ctx.rect(0, self.fontInfo.descender, g.width, self.fontInfo.unitsPerEm)
                self.ctx.translate(g.width + tracking, 0)
                if self.drawTracking:
                    self.ctx.fill(*self.colorTracking)
                    self.ctx.rect(0, self.fontInfo.descender, -tracking, self.fontInfo.unitsPerEm)

            self.ctx.restore()

        # draw kerns
        if self.drawKerning:

            self.ctx.save()
            self.ctx.fontSize(self.captionSize)
            self.ctx.font('Menlo-Bold')
            for i, glyphName in enumerate(self.glyphNames):
                g = self.glyphs[glyphName]
                if self.useKerning and i > 0:
                    pair = self.glyphNames[i-1], glyphName
                    kernValue = self.kerning.get(pair)
                    if kernValue:
                        self.ctx.fill(*self.colorKerning)
                        self.ctx.rect(0, self.fontInfo.descender, kernValue, self.fontInfo.unitsPerEm)
                        self.ctx.fill(0)
                        # self.ctx.text(str(g.width), (g.width/2, self.fontInfo.descender +20), align='center')
                        # if g.bounds:
                        #     self.ctx.text(str(g.leftMargin), (20, self.fontInfo.descender +20), align='left')
                        #     self.ctx.text(str(g.rightMargin), (g.width-20, self.fontInfo.descender +20), align='right')
                        self.ctx.text(str(kernValue), (kernValue/2, self.fontInfo.descender -self.captionSize-20), align='center')
                        self.ctx.translate(kernValue, 0)

                self.ctx.translate(g.width + tracking, 0)
            self.ctx.restore()

        # draw margins
        if self.drawWidths:
            for i, glyphName in enumerate(self.glyphNames):
                g = self.glyphs[glyphName]
                yMin = self.fontInfo.descender
                yMax = self.fontInfo.unitsPerEm - abs(self.fontInfo.descender)
                if self.useKerning and i > 0:
                    pair = self.glyphNames[i-1], glyphName
                    kernValue = self.kerning.get(pair)
                    if kernValue:
                        self.ctx.translate(kernValue, 0)
                self.ctx.stroke(*self.colorMargins)
                self.ctx.strokeWidth(5)
                self.ctx.line((0, yMin), (0, yMax))
                self.ctx.translate(g.width + tracking, 0)
                if i == len(text)-1:
                    self.ctx.line((0, yMin), (0, yMax))
        
        self.ctx.restore()

        # draw glyphs
        if self.drawGlyphs:
            self.ctx.save()
            self.ctx.translate(x, y)
            self.ctx.scale(scale)
            for i, glyphName in enumerate(self.glyphNames):
                g = self.glyphs[glyphName]
                if self.useKerning and i > 0:
                    pair = self.glyphNames[i-1], glyphName
                    kernValue = self.kerning.get(pair)
                    if kernValue:
                        self.ctx.translate(kernValue, 0)
                self.ctx.fill(*self.colorGlyphs)
                drawGlyph(g)
                if i == len(text)-1:
                    continue
                self.ctx.translate(g.width + tracking, 0)
            self.ctx.restore()
