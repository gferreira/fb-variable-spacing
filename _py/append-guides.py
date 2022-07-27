from fontPens.marginPen import MarginPen

g = CurrentGlyph()

yBeam = [None, 40][1]

if g is None:
    f = CurrentFont()
    glyphs = f.selectedGlyphs
else:
    glyphs = [g]

for g in glyphs:
    g.prepareUndo('create spacing guides')
    g.clearGuidelines()
    if g.bounds is None:
        g.appendGuideline((0, 0), 90, name='TRAC')
        g.appendGuideline((d*2, 0), 90, name='TRAC')
    else:
        if yBeam is None:
            L, B, R, T = g.bounds
        else:
            pen = MarginPen(g.font, yBeam, isHorizontal=True)
            g.draw(pen)
            intersections = pen.getAll()
            L, R = intersections[0], intersections[-1]
        g.appendGuideline((L-d, 0), 90, name='TRAC')
        g.appendGuideline((R+d, 0), 90, name='TRAC')
    g.performUndo()
