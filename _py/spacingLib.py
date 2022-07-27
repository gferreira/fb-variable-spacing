# from importlib import reload
# import hTools3.modules.primitives
# reload(hTools3.modules.primitives)

import drawBot as DB
from drawBot import BezierPath
from fontParts.world import OpenFont, RGlyph
from fontPens.marginPen import MarginPen
from progvis.modules.vector import getVector, vector
from progvis.modules.DB.tools import drawGlyph, glyph2bezier
from hTools3.modules.primitives import polygon as Polygon, rect as Rect


class SpacingGlyph:

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

        # gRight = RGlyph()
        # Polygon(gRight.getPen(), rightSide, close=True)
        # gRight = gRight % self.glyph

        # gRight = RGlyph()
        _gRight = BezierPath()
        _gRight.polygon(*rightSide, close=True)
        # _gRight.drawToPen(gRight.getPen())

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

        # gLeft = RGlyph()
        # Polygon(gLeft.getPen(), leftSide, close=True)
        # gLeft = gLeft % self.glyph

        # gLeft = RGlyph()

        _gLeft = BezierPath()
        _gLeft.polygon(*leftSide, close=True)
        # _gLeft.drawToPen(gLeft.getPen())

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
        # gBox = RGlyph()
        # Rect(gBox.getPen(), 0, self.yMin, self.glyph.width, self.yMax - self.yMin)
        # return gBox
        _gBox = BezierPath()
        _gBox.rect(0, self.yMin, self.glyph.width, self.yMax - self.yMin)
        return _gBox

    @property
    def inner(self):
        # box       = glyph2bezier(self.box)
        # leftSide  = glyph2bezier(self.leftSide)
        # rightSide = glyph2bezier(self.rightSide)
        
        # g = RGlyph()
        glyph = BezierPath()
        self.glyph.draw(glyph)
        # glyph = glyph2bezier(g)

        # gInner = RGlyph()
        _gInner = self.box.difference(self.leftSide)
        _gInner = _gInner.difference(self.rightSide)
        _gInner = _gInner.difference(glyph)
        # _gInner.drawToPen(gInner.getPen())
        
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


class SpacingWord:

    text            = 'SPACE'
    scale           = 1.0
    glyphParameters = {}
    innerDraw       = True
    outerDraw       = True
    glyphsDraw      = True

    def __init__(self, font, ctx=DB):
        self.font = font
        self.ctx = ctx

    def setParameters(self, parameters):
        for k, v in parameters.items():
            setattr(self, k, v)
            
    def draw(self, pos):
        self.ctx.translate(*pos)
        self.ctx.scale(self.scale)

        if self.innerDraw or self.outerDraw:
            with self.ctx.savedState():
                for char in self.text:
                    glyphName = char
                    g = self.font[glyphName]
                    G = SpacingGlyph(g, self.ctx)
                    G.setParameters(self.glyphParameters)
                    G.draw((0, 0), inner=self.innerDraw, outer=self.outerDraw, glyph=False)
                    self.ctx.translate(g.width, 0)

        if self.glyphsDraw:
            with self.ctx.savedState():
                for char in self.text:
                    glyphName = char
                    g = self.font[glyphName]
                    G = SpacingGlyph(g)
                    G.setParameters(self.glyphParameters)
                    G.draw((0, 0), inner=False, outer=False, glyph=True)
                    self.ctx.translate(g.width, 0)

