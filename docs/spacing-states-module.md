---
title  : SpacingStates module
layout : default
---

<span class='badge bg-secondary'>version {{ site.version }}</span>

A Python module to work with spacing states in UFO fonts.
{: .lead}

### getSpacingStates

Get the name of all spacing states available in the font.

```python
from variableSpacing import getSpacingStates
spacingStates = getSpacingStates(font)
print(spacingStates)
>>> ['default', 'loose', 'tight']
```

### getSpacingLib

Get the spacing lib from a given font.

```python
from variableSpacing import getSpacingLib
spacingLib = getSpacingLib(font)
print(spacingLib.keys())
>>> dict_keys(['default', 'tight'])
print(spacingLib['default']['a'])
>>> {'leftMargin': 65, 'width': 524}
```

### getKerningLib

Get the kerning lib from a given font.

```python
from variableSpacing import getKerningLib
kerningLib = getKerningLib(font)
print(kerningLib.keys())
>>> dict_keys(['default', 'tight'])
print(kerningLib['default'][0])
>>> ['B', 'J', -20]
```

### saveSpacingToLib

Save the font’s current spacing values (width, left margin) to the font lib.

```python
from variableSpacing import saveSpacingToLib
font = CurrentFont()
saveSpacingToLib(font, 'tight')
```

### saveKerningToLib

Save the font’s current kerning values to the font lib.

```python
from variableSpacing import saveKerningToLib
font = CurrentFont()
saveKerningToLib(font, 'tight')
```

### collectGlyphsByType

Return the font's glyph names separated into four groups:
- contours only
- empty glyphs
- components only
- mixed contours & components

```python
from variableSpacing import collectGlyphsByType
font = CurrentFont()
contours, empty, components, mixed = collectGlyphsByType(f)
print('glyphs with contours only:', ' '.join(contours))
print('empty glyphs:', ' '.join(empty))
print('glyphs with components only:', ' '.join(components))
print('glyphs with contours and components:', ' '.join(mixed))
```

### loadSpacingFromLib

Load spacing data for a given state from the lib into the font.

```python
from variableSpacing import loadSpacingFromLib
f = CurrentFont()
loadSpacingFromLib(f, 'tight')
```

### loadKerningFromLib

Load kerning data for a given state from the lib into the font.

```python
from variableSpacing import loadKerningFromLib
f = CurrentFont()
loadKerningFromLib(f, 'tight')
```

### deleteSpacingState

Delete a given state from the spacing and kerning libs in the font.

```python
from variableSpacing import getSpacingStates, deleteSpacingState
f = CurrentFont()
print(getSpacingStates(f))
>>> ['tight', 'default']
deleteSpacingState(f, 'tight')
print(getSpacingStates(f))
>>> ['default']
```

### deleteSpacingStates

Delete top-level font libs with the given key prefix from the font.

### buildSpacingSources

Build existing spacing states as separate UFO sources for variable font generation.

```python
from variableSpacing import buildSpacingSources
folder = '/someFolder/'
newSources = buildSpacingSources(folder, prefix='_SPAC-')
# do something with the new sources, for example insert them into the designspace
print(newSources)
```

### exportSpacingStates

Export a font’s spacing states as an external JSON file.

```python
from variableSpacing import exportSpacingStates
f = CurrentFont()
jsonPath = f.path.replace('.ufo', '.json')
exportSpacingStates(f, jsonPath)
```

### importSpacingStates

Import spacing states from an external JSON file into a font.

```python
from variableSpacing import importSpacingStates
f = CurrentFont()
jsonPath = f.path.replace('.ufo', '.json')
importSpacingStates(f, jsonPath)
```

### smartSetMargins

Set left and right glyph margins while preserving their positions in components.

