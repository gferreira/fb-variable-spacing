# visualize negative space in a typeface

# --------
# settings
# --------

txt = 'HARLEY'
fn = ['SourceSerifRoman-Bold', 'Georgia'][1] # fontname
fs = 180 # fontsize
x, y = 34, 156

c0 = 0,
c1 = 1,
c2 = 1, 0, 1
c3 = 0, 1, 1


# -----
# draw!
# -----

size('A4Landscape')
fill(*c0)
rect(0, 0, width(), height())
font(fn)
fontSize(fs)
lineHeight(fs)

_xMin = []
_xMax = []
_yMin = []
_yMax = []

_x, _y = x, y
_W, _H = textSize(txt)

for i, char in enumerate(txt):

    # get glyph contour
    B1 = BezierPath()
    B1.text(char, (_x, _y), fontSize=fs, font=fn)

    # get glyph box
    xMin, yMin, xMax, yMax = B1.bounds()
    _xMin.append(xMin)
    _yMin.append(yMin)
    _xMax.append(xMax)
    _yMax.append(yMax)

    if i == 0:
        x0 = xMin - _x
    if i == len(txt)-1:
        xz = _W - xMax

for i, char in enumerate(txt):
    w, h = textSize(char)

    # get glyph contour
    B1 = BezierPath()
    B1.text(char, (_x, _y), fontSize=fs, font=fn)

    # make glyph areas
    xMin, yMin, xMax, yMax = B1.bounds()
    B2 = BezierPath()
    B2.rect(xMin, yMin, xMax-xMin, yMax-yMin)
    B3 = B2.difference(B1)

    # draw glyph areas
    stroke(None)
    for c in B3.contours:
        B = BezierPath()
        c.drawToPen(B)
        # check if shape is on the edge
        fill(*c2)
        drawPath(B)

    # draw glyph contour
    stroke(None)
    fill(*c1)
    drawPath(B1)

    # done with glyph
    _x += w

# draw word box

_xMin = min(_xMin)
_xMax = max(_xMax)
_yMin = max(_yMin)
_yMax = min(_yMax)

W = _xMax - _xMin # - x0 # - xz
H = _yMax - _yMin # - y

fill(None)
stroke(1, 0, 0)
strokeWidth(1)
rect(x+x0, y, W, H)
