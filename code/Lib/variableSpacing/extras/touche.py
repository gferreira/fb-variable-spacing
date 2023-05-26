'''
Touché by Nina Stössinger & Frederik Berlaen
# add link to public repository on github

with some changes by Gustavo Ferreira (2023)

'''
from fontTools.pens.basePen import BasePen
from fontTools.misc.arrayTools import pointInRect, offsetRect, sectRect
try:
    # check if these are available somewhere else
    from lib.tools.bezierTools import intersectCubicCubic, intersectCubicLine, intersectLineLine
except:
    # print('not in RF')
    pass

def pointBoundTouche(point, bounds):
    found = pointInRect(point, bounds)
    if not found:
        # lazy check x values only
        minX, minY, maxX, maxY = bounds
        found = minX <= point[0] <= maxX
    return found
    
class FindPossibleOverlappingSegmentsPen(BasePen):
    
    def __init__(self, glyphSet, bounds, moveSegment=(0, 0)):
        BasePen.__init__(self, glyphSet)

        self.allSegments = set()
        self.segments = set()
        self.bounds = bounds
        self.moveSegment = moveSegment
    
    def addSegment(self, segment):
        mx, my = self.moveSegment
        segment = tuple((x+mx, y+my) for x, y in segment)
        self.segments.add(segment)
    
    def _moveTo(self, pt):
        self.previousPoint = pt
        self.firstPoint = pt
    
    def _lineTo(self, pt):
        if pointBoundTouche(pt, self.bounds):
            self.addSegment((self.previousPoint, pt))
        self.previousPoint = pt
    
    def _curveToOne(self, pt1, pt2, pt3):
        found = False
        if pointBoundTouche(pt1, self.bounds):
            found = True
        elif pointBoundTouche(pt2, self.bounds):
            found = True
        elif pointBoundTouche(pt3, self.bounds):
            found = True
        if found:
            self.addSegment((self.previousPoint, pt1, pt2, pt3))
        self.previousPoint = pt3
        
    def closePath(self):
        if self.firstPoint != self.previousPoint:
            self.lineTo(self.firstPoint)
            
class Touche(object):
    """
    Checks a font for touching glyphs.

        font = CurrentFont()
        a, b = font['a'], font['b']
        touche = Touche(font)
        touche.checkPair(a, b)
        touche.findTouchingPairs([a, b])

    """

    def __init__(self, font):
        self.font = font
        self.flatKerning = font.naked().flatKerning

    def __del__(self):
        self.font = None
        self.flatKerning = None

    def lookupSidebearings(self, glyphs=None):
        if glyphs is None:
            glyphs = [self.font[gName] for gName in self.font.glyphOrder]
        # lookup all sidebearings
        lsb, rsb = ({} for i in range(2))
        for g in glyphs:
            lsb[g], rsb[g] = g.leftMargin, g.rightMargin
        self.lsb, self.rsb = lsb, rsb

    def findTouchingPairs(self, glyphs):
        """
        Finds all touching pairs in a list of glyphs.

        Returns a list of tuples containing the names of overlapping glyphs

        """
        self.lookupSidebearings(glyphs)
        pairs = [(g1, g2) for g1 in glyphs for g2 in glyphs]
        return [(g1.name, g2.name) for (g1, g2) in pairs if self.checkPair(g1, g2)]

    def getKerning(self, g1, g2):
        return self.flatKerning.get((g1.name, g2.name), 0)

    def checkPair(self, g1, g2):
        """
        New checking method contributed by Frederik

        Returns a Boolean if overlapping.

        """
        kern = self.getKerning(g1, g2)

        # Check sidebearings first (PvB's idea)
        if self.rsb.get(g1) is not None and self.lsb.get(g2) is not None: # watch out for empty glyphs
            if self.rsb[g1] + self.lsb[g2] + kern > 0:
                return False

        # get the bounds and check them
        bounds1 = g1.bounds
        if bounds1 is None:
            return False
        bounds2 = g2.bounds
        if bounds2 is None:
            return False

        # shift bounds2
        bounds2 = offsetRect(bounds2, g1.width+kern, 0)
        # check for intersection bounds
        intersectingBounds, _ = sectRect(bounds1, bounds2)
        if not intersectingBounds:
            return False
        # move bounds1 back, moving bounds is faster then moving all coordinates in a glyph
        bounds1 = offsetRect(bounds1, -g2.width-kern, 0)

        # create a pen for g1 with a shifted rect, draw the glyph into the pen
        f1 = g1.font
        pen1 = FindPossibleOverlappingSegmentsPen(f1, bounds2)
        g1.draw(pen1)

        # create a pen for g2 with a shifted rect and move each found segment with the width and kerning
        f2 = g1.font
        pen2 = FindPossibleOverlappingSegmentsPen(f2, bounds1, (g1.width+kern, 0))
        # draw the glyph into the pen
        g2.draw(pen2)

        for segment1 in pen1.segments:
            for segment2 in pen2.segments:
                if len(segment1) == 4 and len(segment2) == 4:
                    a1, a2, a3, a4 = segment1
                    b1, b2, b3, b4 = segment2
                    result = intersectCubicCubic(a1, a2, a3, a4, b1, b2, b3, b4)
                elif len(segment1) == 4:
                    p1, p2, p3, p4 = segment1
                    a1, a2 = segment2
                    result = intersectCubicLine(p1, p2, p3, p4, a1, a2)
                elif len(segment2) == 4:
                    p1, p2, p3, p4 = segment2
                    a1, a2 = segment1
                    result = intersectCubicLine(p1, p2, p3, p4, a1, a2)
                else:
                    a1, a2 = segment1
                    b1, b2 = segment2
                    result = intersectLineLine(a1, a2, b1, b2)
                if result.status == "Intersection":
                    return True

        return False
