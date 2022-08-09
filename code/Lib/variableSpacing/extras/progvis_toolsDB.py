from importlib import reload

import progvis.modules.vector
reload(progvis.modules.vector)
import hTools3.modules.bezier
reload(hTools3.modules.bezier)

import drawBot
from fontParts.world import RGlyph, RFont
from progvis.modules.vector import vector
from hTools3.modules.bezier import getBezierPoint

#: The name of the cap styles in strokes.
CAPSTYLES = ['round', 'butt', 'square']

#: The name of the join styles in strokes.
JOINSTYLES = ['round', 'miter', 'bevel']

def background(*color):
    drawBot.fill(*color)
    drawBot.rect(0, 0, drawBot.width(), drawBot.width())

def wrapLine(p1, p2, d, a, a2=90):
    '''
    d = 500
    d1 = d2 = 26
    a1 = 30
    x1, y1 = 200, 200
    x2, y2 = vector((x1, y1), d, a1)

    fill(None)
    strokeWidth(8)
    stroke(0, 1, 0)
    line((x1, y1), (x2, y2))

    strokeWidth(3)
    stroke(1, 0, 0)
    wrapLine((x1, y1), (x2, y2), (d1, d2), a1)

    '''
    x1, y1 = p1
    x2, y2 = p2
    d1, d2 = d
    # extend first point
    x1a, y1a = vector((x1,  y1),   d1, 180+a)
    x1b, y1b = vector((x1a, y1a), +d2, 180+a+a2)
    x1c, y1c = vector((x1a, y1a), -d2, 180+a+a2)
    # extend second point
    x2a, y2a = vector((x2,  y2),  +d1, a)
    x2b, y2b = vector((x2a, y2a), +d2, a+a2)
    x2c, y2c = vector((x2a, y2a), -d2, a+a2)
    # draw polygon around line
    drawBot.polygon((x1b, y1b), (x1c, y1c), (x2b, y2b), (x2c, y2c))

def getContours(glyph, bezier, pos=None, scale=1.0, close=True):

    if pos is None:
        x, y = 0, 0
    else:
        x, y = pos

    for contour in glyph:
        if len(contour) > 1:
            for i, s in enumerate(contour.segments):
                # moveTo
                if i == 0:
                    if len(s.points) == 1:
                        x1, y1 = s.points[0].x, s.points[0].y
                        bezier.moveTo((x + x1, y + y1))
                    else:
                        s_ = contour[-1]
                        x1, y1 = s_.points[-1].x, s_.points[-1].y
                        bezier.moveTo((x + x1, y + y1))
                        x1, y1 = s.points[0].x, s.points[0].y
                        x2, y2 = s.points[1].x, s.points[1].y
                        x3, y3 = s.points[2].x, s.points[2].y
                        bezier.curveTo((x + x1, y + y1), (x + x2, y + y2), (x + x3, y + y3))
                else:
                    # curveTo
                    if len(s.points) == 3:
                        x1, y1 = s.points[0].x, s.points[0].y
                        x2, y2 = s.points[1].x, s.points[1].y
                        x3, y3 = s.points[2].x, s.points[2].y
                        bezier.curveTo((x + x1, y + y1), (x + x2, y + y2), (x + x3, y + y3))
                    # lineTo
                    else:
                        x1, y1 = s.points[0].x, s.points[0].y
                        bezier.lineTo((x + x1, y + y1))
            # closePath
            if close or contour.points[0] == contour.points[-1]:
                bezier.closePath()

def getComponents(glyph, bezier, close=True):
    font = glyph.font
    for component in glyph.components:
        baseGlyph = component.baseGlyph
        s = component.scale
        x, y = component.offset
        getContours(font[baseGlyph], bezier, pos=(x, y), scale=s, close=True)

def glyph2bezier(glyph, close=True):
    B = drawBot.BezierPath()
    getContours(glyph, B, close=close)
    getComponents(glyph, B, close=close)
    return B

glyphToBezier = getBezier = glyph2bezier

def bezier2glyph(bezierPath, close=True):
    '''
    Convert a DrawBot ``BezierPath`` object into a glyph.

    '''
    # create an empty glyph
    glyph = RGlyph()
    pen = glyph.getPen()
    # get points from bezier
    for contour in bezierPath.contours:
        for i, segment in enumerate(contour):
            if len(segment) == 1:
                pt = segment[0]
                # moveTo
                if i == 0:
                    pen.moveTo(pt)
                    firstPt = pt
                # lineTo
                else:
                    ptX, ptY = pt
                    if pt == firstPt:
                        ptX += 0.0000000001
                    pen.lineTo((ptX, ptY))
            # curveTo
            elif len(segment) == 3:
                pt1 = segment[0]
                pt2 = segment[1]
                pt3 = segment[2]
                pen.curveTo(pt1, pt2, pt3)
            else:
                print('segment length not supported')
        # done with contour
        if close:
            pen.closePath()
        else:
            pen.endPath()
    # done
    return glyph

bezierToGlyph = bezier2glyph

def drawGlyph(glyph):
    B = drawBot.BezierPath()
    glyph.draw(B)
    drawBot.drawPath(B)

#----------------
# resample paths
#----------------

def makeStepsList(glyph, steps):

    cntrs = []

    for contour in glyph:

        d = (len(contour)-1) / float(steps-1)

        pts = []

        for step in range(steps):

            f = step * d
            i, t = str(f).split('.')
            i1 = int(i)
            t = float('0.%s' % t)

            if i1 == len(contour)-1:
                i1 -= 1
                t = 1.0

            i2 = i1 + 1

            bpt1 = contour.bPoints[i1]
            bpt2 = contour.bPoints[i2]

            pt1 = bpt1.anchor
            pt2 = pt1[0] + bpt1.bcpOut[0], pt1[1] + bpt1.bcpOut[1]
            pt4 = bpt2.anchor
            pt3 = pt4[0] + bpt2.bcpIn[0], pt4[1] + bpt2.bcpIn[1]

            x, y = getBezierPoint(t, pt1, pt2, pt3, pt4)

            pts.append((x, y))

        cntrs.append(pts)

    return cntrs

def makeStepsGlyph(glyph, steps):
    pointLists = makeStepsList(glyph, steps)
    g = RGlyph()
    pen = g.getPen()
    for pts in pointLists:
        for i, pt in enumerate(pts):
            if i == 0:
                pen.moveTo(pt)
            else:
                pen.lineTo(pt)
        pen.endPath()
    return g

if __name__ == '__main__':

    ufoPath = u"/_fonts/Calligraphica/_ufos/03.ufo"
    f = RFont(ufoPath)
    src = f['c']
    dst = makeStepsGlyph(src, 19)

    print(len(dst))
    for c in dst:
        print(c, len(c))

