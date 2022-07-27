import drawBot
from defcon.objects.component import _defaultTransformation
from ufoProcessor import DesignSpaceProcessor, Location #, DecomposePointPen
from fontTools.agl import UV2AGL
from fontParts.world import RGlyph


def drawGlyph(g):
    bez = drawBot.BezierPath()
    g.draw(bez)
    drawBot.drawPath(bez)


class DecomposePointPen(object):

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

    fontInfo   = {}
    kerning    = {}
    glyphs     = {}
    glyphNames = []

    previewKerning = True
    drawKerning    = True

    def __init__(self, designspacePath, ctx=drawBot):
        self.designspacePath = designspacePath
        self.ctx = ctx

    def draw(self, text, pos, scale, locationDict):
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

        # interpolate kerning
        if self.previewKerning:
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

        # draw background
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(scale)

        for i, glyphName in enumerate(self.glyphNames):
            g = self.glyphs[glyphName]

            self.ctx.fill(0.8)
            self.ctx.rect(0, self.fontInfo.descender, g.width, self.fontInfo.unitsPerEm)

            if self.previewKerning and i > 0:
                pair = self.glyphNames[i-1], glyphName
                kernValue = self.kerning.get(pair)
                if kernValue:
                    if self.drawKerning:
                        self.ctx.fill(1, 0, 0)
                        self.ctx.rect(0, self.fontInfo.descender, kernValue, self.fontInfo.unitsPerEm)
                    self.ctx.translate(kernValue, 0)

            if i == len(text)-1:
                continue

            self.ctx.translate(g.width, 0)

        self.ctx.restore()

        # draw glyphs
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(scale)

        for i, glyphName in enumerate(self.glyphNames):
            g = self.glyphs[glyphName]

            if self.previewKerning and i > 0:
                pair = self.glyphNames[i-1], glyphName
                kernValue = self.kerning.get(pair)
                if kernValue:
                    self.ctx.translate(kernValue, 0)

            self.ctx.fill(0)
            drawGlyph(g)

            if i == len(text)-1:
                continue

            self.ctx.translate(g.width, 0)

        self.ctx.restore()

