---
title  : SpacingStates module
layout : default
order  : 2
---

A Python module to work with spacing states in UFO fonts.
{: .lead}

* Table of Contents
{:toc}


Reading
-------

##### `getSpacingStates(font)`

Get the name of all spacing states available in the font.

```python
from variableSpacing import getStatesNames
spacingStates = getStatesNames(font)
print(spacingStates)
>>> ['default', 'loose', 'tight']
```

##### `getSpacingLib(font)`

Get the spacing lib from a given font.

```python
from variableSpacing import getSpacingLib
spacingLib = getSpacingLib(font)
print(spacingLib.keys())
>>> dict_keys(['default', 'tight'])
print(spacingLib['default']['a'])
>>> {'leftMargin': 65, 'width': 524}
```

##### `getKerningLib(font)`

Get the kerning lib from a given font.

```python
from variableSpacing import getKerningLib
kerningLib = getKerningLib(font)
print(kerningLib.keys())
>>> dict_keys(['default', 'tight'])
print(kerningLib['default'][0])
>>> ['B', 'J', -20]
```

##### `getComponentsLib(font)`

Get the components lib from a given font.

```python
from variableSpacing import getComponentsLib
componentsLib = getComponentsLib(font)
print(componentsLib.keys())
>>> dict_keys(['default', 'tight'])
print(componentsLib['default']['a'])
>>> {'leftMargin': 65, 'width': 524}
```


Writing
-------

##### `saveComponentsToLib(font)`

Save relative positions between components in the font lib.

```python
from variableSpacing import saveComponentsToLib
font = CurrentFont()
saveComponentsToLib(font)
```

##### `saveSpacingToLib(font, spacingState)`

Save the font’s current spacing values (width, left margin) and component positions to the font lib.

```python
from variableSpacing import saveSpacingToLib
font = CurrentFont()
saveSpacingToLib(font, 'tight')
```

##### `saveKerningToLib(font, spacingState)`

Save the font’s current kerning values to the font lib.

```python
from variableSpacing import saveKerningToLib
font = CurrentFont()
saveKerningToLib(font, 'tight')
```


Loading
-------

##### `loadSpacingFromLib(font, spacingState)`

Load spacing data for a given state from the lib into the font.

```python
from variableSpacing import loadSpacingFromLib
font = CurrentFont()
loadSpacingFromLib(font, 'tight')
```

##### `loadKerningFromLib(font, spacingState)`

Load kerning data for a given state from the lib into the font.

```python
from variableSpacing import loadKerningFromLib
font = CurrentFont()
loadKerningFromLib(font, 'tight')
```


Deleting
--------

##### `deleteSpacingState(font, spacingState)`

Delete a given state from the spacing and kerning libs in the font.

```python
from variableSpacing import deleteSpacingState
font = CurrentFont()
deleteSpacingState(font, 'tight')
```

##### `deleteSpacingStatesLib(font)`

Delete top-level spacing states font lib from the font.

```python
from variableSpacing import deleteSpacingStatesLib
font = CurrentFont()
deleteSpacingStatesLib(font, 'tight')
```


Generating
----------

##### `buildSpacingSources(folder)`

Generate spacing states as separate UFO sources for all fonts in a given folder.


Exporting & importing
---------------------

##### `exportSpacingStates(font, jsonPath)`

Export a font’s spacing states as an external JSON file.

##### `importSpacingStates(font, jsonPath)`

Import spacing states from an external JSON file into a font.
