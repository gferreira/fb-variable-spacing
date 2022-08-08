from hTools3.objects.hproject import hProject
p = hProject('/hipertipo/fonts/Publica')

for fontName, ufoPath in p.fonts.items():
    if not fontName[-1] == 'A':
        continue
    f = OpenFont(ufoPath, showInterface=False)
    for g in f:
        if not len(g.guidelines):
            continue
        for guide in g.guidelines:
            if guide.name == 'SPAC':
                guide.name = 'TRAC'
    f.save()
    f.close()

    