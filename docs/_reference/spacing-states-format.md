---
title  : Spacing States format
layout : default
order  : 1
---

<span class='badge bg-secondary'>version {{ site.version }}</span>

A format to store various sets of glyph metrics and kerning values inside the same font.
{: .lead}

* Table of Contents
{:toc}


Spacing State definition
------------------------

A *spacing state* is a description of all spacing values in a font.

A single set of glyph contours can contain multiple spacing states, for example: *standard*, *tight* and *loose*.

A spacing state is defined by:

- the *left margin* and *advance width* of all glyphs
- all *kerning values* in the font

### Libs overview

The data to enable spacing states in UFO sources is stored in 2 custom font-level libs under the prefix `com.hipertipo.spacingaxis`:

<table class='table'>
  <tr>
    <th>lib</th>
    <th>key</th>
  </tr>
  <tr>
    <td><a href='#spacing-lib'>spacing lib</a></td>
    <td><code>com.hipertipo.spacingaxis.spacing</code></td>
  </tr>
  <tr>
    <td><a href='#kerning-lib'>kerning lib</a></td>
    <td><code>com.hipertipo.spacingaxis.kerning</code></td>
  </tr>
</table>


Spacing lib
-----------

The spacing lib contains a record of the **left margin** and **advance width** of all glyphs in a font, for each spacing state.

Empty glyphs have no margins, and are described only by their advance width.

##### Python example 

```python
font.lib[f'com.hipertipo.spacingaxis.spacing'] = {
    'default' : {
        'a': {'width': 543, 'leftMargin': 75},
        'space': {'width': 270},
    }
    'tight' : {
        'a': {
            # etc.
        },
    },
    'loose' : {
        'a': {
            # etc.
        },
    },
}
```

##### XML example

```xml
<key>com.hipertipo.spacingaxis.spacing</key>
<dict>
  <key>default</key>
  <dict>
    <key>a</key>
    <dict>
      <key>leftMargin</key>
      <real>75</real>
      <key>width</key>
      <integer>543</integer>
    </dict>
    <key>space</key>
    <dict>
      <key>width</key>
      <integer>270</integer>
    </dict>
  </dict>
  <key>tight</key>
  <dict>
    <key>a</key>
    <dict>
      <!-- etc. -->
    </dict>
  </dict>
  <key>loose</key>
  <dict>
    <key>a</key>
    <dict>
      <!-- etc. -->
    </dict>
  </dict>
</dict>
```


Kerning lib
-----------

The kerning lib contains a record of all **kerning values** in a font, for each spacing state.

Each kerning pair is stored as a tuple of *first glyph or group*, *second glyph or group*, and the *kern value*.

##### Python example 

```python
font.lib['com.hipertipo.spacingaxis.kerning'] = {
    'default' : [
        ('public.kern1.A', 'public.kern2.V', -40),
        ('B', 'J', -20),
    ],
    'tight' : [
        # etc.
    ],
    'loose' : [
        # etc.
    ],
}
```

##### XML example

```xml
<key>com.hipertipo.spacingaxis.kerning</key>
<dict>
  <key>default</key>
  <array>
    <array>
      <string>public.kern1.A</string>
      <string>public.kern2.V</string>
      <integer>-40</integer>
    </array>
    <array>
      <string>B</string>
      <string>J</string>
      <integer>-20</integer>
    </array>
  </array>
  <key>tight</key>
  <array>
    <!-- etc. -->
  </array>
  <key>loose</key>
  <array>
    <!-- etc. -->
  </array>
</dict>
```
