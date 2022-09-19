---
title  : Spacing States format
layout : default
order  : 1
---

A format to store various sets of glyph metrics and kerning values inside the same font.
{: .lead}

* Table of Contents
{:toc}


Spacing State definition
------------------------

A *spacing state* is a description of all whitespace values in a font.

A single font can contain several spacing states, for example: *standard*, *tight* and *loose*.

Each spacing state is described by:

- the *advance width* and *left margin* of all glyphs
- all *kerning values* in the font

{% comment %}
- the *positional relationship* between components
{% endcomment %}

### Libs overview

Data to enable spacing states is stored in 3 custom font-level libs under the prefix `com.hipertipo.spacingaxis`:

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
  <tr>
    <td><a href='#components-lib'>components lib</a></td>
    <td><code>com.hipertipo.spacingaxis.components</code></td>
  </tr>
</table>


Spacing lib
-----------

The spacing lib contains a record of the **advance width** and **left margin** of all glyphs in a font, for each spacing state.

Empty glyphs have no margins and are described only by their advance width.

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

Each kerning pair is stored as a tuple of *first glyph*, *second glyph*, and *kern value*.

Glyphs in kerning pairs are defined as *glyph names* or *kerning groups*.

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


Components lib
--------------

The components lib contains a record of all **component positions** in a font, expressed in relation to the glyph bounds.

This data is used to preserve the relative positions between components when switching spacing states.

All and only glyphs containing components are included.

- Components are defined by their *base glyph name* and *relative offset*.
- Contours are defined by their *position* and *unique identifiers*.

##### Python example 

```python
font.lib['com.hipertipo.spacingaxis.components'] = {
    'aacute' : [
        ('a', (65.0, -10.0)),
        ('acutecmb', (212.0, 581.0)),
    ]
    'dollar' : [
        ('S', (62.0, -10.0)),         # component
        ((225, 588), 'VyKpf7rL3q'),   # contour
        ((225, -115), 'ZpTeU9Jwwi'),
    ],
    # etc.
}
```

##### XML example

```xml
<key>com.hipertipo.spacingaxis.components</key>
<dict>
  <key>aacute</key>
  <array>
    <array>
      <string>a</string>
      <array>
        <real>65.0</real>
        <real>-10.0</real>
      </array>
    </array>
    <array>
      <string>acutecmb</string>
      <array>
        <real>212.0</real>
        <real>581.0</real>
      </array>
    </array>
  </array>
  <key>dollar</key>
  <array>
    <array>
      <string>S</string>
      <array>
        <real>62.0</real>
        <real>-10.0</real>
      </array>
    </array>
    <array>
      <array>
        <real>225</real>
        <real>588</real>
      </array>
      <string>VyKpf7rL3q</string>
    </array>
    <array>
      <array>
        <real>225</real>
        <real>-115</real>
      </array>
      <string>ZpTeU9Jwwi</string>
    </array>
  </array>
</dict>
```


{% comment %}
### Old format (deprecated)

##### XML example

```xml
<key>com.hipertipo.spacingaxis.components</key>
<dict>
  <key>aacute</key>
  <dict>
    <key>a</key>
    <array>
      <real>65.0</real>
      <real>-10.0</real>
    </array>
    <key>acutecmb</key>
    <array>
      <real>212.0</real>
      <real>581.0</real>
    </array>
  </dict>
  <key>dollar</key>
  <dict>
    <key>S</key>
    <array>
      <real>62.0</real>
      <real>-10.0</real>
    </array>
    <key>VyKpf7rL3q</key>
    <array>
      <integer>225</integer>
      <integer>588</integer>
    </array>
    <key>ZpTeU9Jwwi</key>
    <array>
      <integer>225</integer>
      <integer>-115</integer>
    </array>
  </dict>
  <!-- etc. -->
</dict>
```

##### Python example 

```python
font.lib['com.hipertipo.spacingaxis.components'] = {
    'aacute' : {
        'a' : (65.0, -10.0),
        'acutecmb' : (212.0, 581.0),
    },
    'dollar' : {
        'S' : (62.0, -10.0),
        'VyKpf7rL3q' : (225, 588),
        'ZpTeU9Jwwi' : (225, -115)
    },
    # etc.
}
```
{% endcomment %}
