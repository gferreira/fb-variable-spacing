import sys

# ufoProcessor is not embedded in DrawBot
try:
    import ufoProcessor
except:
    # http://github.com/LettError/ufoProcessor
    ufoProcessorPath = '/_code/ufoProcessor/Lib'
    sys.path.append(ufoProcessorPath)
    import ufoProcessor

import drawBot as DB
from drawBot import BezierPath
from ufoProcessor import DesignSpaceProcessor, Location
from fontTools.agl import UV2AGL
from fontParts.world import OpenFont, RGlyph
from fontPens.marginPen import MarginPen

from variableSpacing.extras.progvis_vector import getVector, vector
from variableSpacing.extras.progvis_toolsDB import drawGlyph, glyph2bezier
from variableSpacing.extras.hTools3_primitives import polygon as Polygon, rect as Rect

def drawGlyph(g):
    bez = DB.BezierPath()
    g.draw(bez)
    DB.drawPath(bez)


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




class SpacingAreasGlyph:
    '''
    An object to visualize the inside and outside of a glyph using color areas.

    *This version works only inside the RoboFont DrawBot Extension.*

    TODO:
    - rewrite glyph boolean operations with BezierPath
    - make it work with designspace files?

    '''
    ySteps  = 10
    color2  = 1, 0, 1
    color1  = 0, 1, 1
    color3  = 0,
    xFactor = 0.3

    _dMax = None
    _yMin = None
    _yMax = None

    def __init__(self, glyph, ctx=DB):
        self.glyph = glyph
        self.ctx = ctx

    @property
    def yStep(self):
        return (self.yMax - self.yMin) // self.ySteps

    @property
    def yMin(self):
        return self.glyph.bounds[1] if self._yMin is None else self._yMin

    @yMin.setter
    def yMin(self, value):
        self._yMin = value

    @property
    def yMax(self):
        return self.glyph.bounds[3] if self._yMax is None else self._yMax
    
    @yMax.setter
    def yMax(self, value):
        # if type(value) is str:
        #     value = getattr(self.glyph.font.info, value)
        self._yMax = value
    
    @property
    def dMax(self):
        return self.glyph.width * self.xFactor if self._dMax is None else  self._dMax

    @dMax.setter
    def dMax(self, value):
        self._dMax = value

    @property
    def rightSide(self):
        _rightSide = []
        for y in range(self.yMin, self.yMax, self.yStep):
            pen = MarginPen(dict(), y, isHorizontal=True)
            self.glyph.draw(pen)
            intersections = pen.getAll()
            if not intersections:
                _rightSide.append((self.glyph.width/2, y))
            else:
                _rightSide.append((intersections[-1], y))

        rightSide = []
        for i, pt in enumerate(_rightSide):
            x, y = pt
            if x < self.glyph.width - self.dMax:
                x = self.glyph.width - self.dMax
            if x > self.glyph.width:
                x = self.glyph.width
            rightSide.append((x, y))
        rightSide.append((x, self.yMax))
        rightSide.append((self.glyph.width, self.yMax))
        rightSide.append((self.glyph.width, self.yMin))

        _gRight = BezierPath()
        _gRight.polygon(*rightSide, close=True)

        return _gRight

    @property
    def rightSideGlyph(self):
        g = RGlyph()
        self.rightSide.drawToPen(g.getPen())
        return g

    @property
    def leftSide(self):
        _leftSide  = []
        for y in range(self.yMin, self.yMax, self.yStep):
            pen = MarginPen(dict(), y, isHorizontal=True)
            self.glyph.draw(pen)
            intersections = pen.getAll()
            if not intersections:
                _leftSide.append((self.glyph.width/2, y))
            else:
                _leftSide.append((intersections[0], y))

        leftSide = []
        for i, pt in enumerate(_leftSide):
            x, y = pt
            if x > self.dMax or x < 0:
                x = self.dMax
            leftSide.append((x, y))
        leftSide.append((x, self.yMax))
        leftSide.append((0, self.yMax))
        leftSide.append((0, self.yMin))

        _gLeft = BezierPath()
        _gLeft.polygon(*leftSide, close=True)

        return _gLeft

    @property
    def leftSideGlyph(self):
        g = RGlyph()
        self.leftSide.drawToPen(g.getPen())
        return g

    @property
    def innerGlyph(self):
        g = RGlyph()
        self.inner.drawToPen(g.getPen())
        return g

    @property
    def box(self):
        _gBox = BezierPath()
        _gBox.rect(0, self.yMin, self.glyph.width, self.yMax - self.yMin)
        return _gBox

    @property
    def inner(self):
        glyph = BezierPath()
        self.glyph.draw(glyph)

        _gInner = self.box.difference(self.leftSide)
        _gInner = _gInner.difference(self.rightSide)
        _gInner = _gInner.difference(glyph)
        
        return _gInner

    def setParameters(self, parameters):
        for k, v in parameters.items():
            setattr(self, k, v)

    def draw(self, pos, outer=True, inner=True, glyph=False):
        x, y = pos
        self.ctx.translate(x, y)
        if outer:
            self.ctx.fill(*self.color1)
            self.ctx.drawPath(self.leftSide)
            self.ctx.drawPath(self.rightSide)
        if inner:
            self.ctx.fill(*self.color2)
            self.ctx.drawPath(self.inner)
        if glyph:
            self.ctx.fill(*self.color3)
            drawGlyph(self.glyph)


class SpacingAreasLine:
    '''
    An object to visualize the inside and outside of all glyphs in a string of text.

    '''

    fontInfo        = {}
    kerning         = {}
    glyphs          = {}
    glyphNames      = []

    scale           = 1.0
    location        = {}
    glyphParameters = {}

    tracking        = 0          # as a percentage % of em
    useKerning      = True

    innerDraw       = True
    outerDraw       = True
    glyphsDraw      = True

    def __init__(self, designspacePath, ctx=DB):
        self.designspacePath = designspacePath
        self.ctx = ctx

    def setParameters(self, parameters):
        for k, v in parameters.items():
            setattr(self, k, v)
            
    def draw(self, text, pos):

        # ------------------
        # instantiate glyphs
        # ------------------

        doc = DesignSpaceProcessor()
        doc.read(self.designspacePath)
        doc.loadFonts()

        location = Location(**self.location)

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
        self.ctx.translate(*pos)
        self.ctx.scale(self.scale)

        if self.innerDraw or self.outerDraw:
            with self.ctx.savedState():
                for i, glyphName in enumerate(self.glyphNames):
                    g = self.glyphs[glyphName]
                    G = SpacingAreasGlyph(g, self.ctx)
                    G.setParameters(self.glyphParameters)
                    if type(G.yMax) is str:
                        G.yMax = getattr(self.fontInfo, G.yMax)

                    G.draw((0, 0), inner=self.innerDraw, outer=self.outerDraw, glyph=False)
                    self.ctx.translate(g.width, 0)

        if self.glyphsDraw:
            with self.ctx.savedState():
                for i, glyphName in enumerate(self.glyphNames):
                    g = self.glyphs[glyphName]
                    G = SpacingAreasGlyph(g)
                    G.setParameters(self.glyphParameters)
                    G.draw((0, 0), inner=False, outer=False, glyph=True)
                    self.ctx.translate(g.width, 0)

        self.ctx.restore()
