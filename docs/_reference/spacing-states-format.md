---
title  : Spacing States format
layout : default
order  : 1
---

A format to store various sets of glyph metrics and kerning values inside the same font.
{: .lead}


Spacing State definition
------------------------

The **spacing state** of a font is defined as the sum of:

- glyph width and left margin of all glyphs
- all kerning values

Multiple spacing states share the same set of glyph contours.


Spacing State libs
------------------

Spacing states are stored under two separate custom font-level libs: one for the actual spacing (glyph metrics), and the other one for the kerning.

The prefix `com.hipertipo.spacingaxis` is used to identify both libs:

<table class='table'>
  <tr>
    <th>lib</th>
    <th>key</th>
  </tr>
  <tr>
    <td>spacing</td>
    <td><code>com.hipertipo.spacingaxis.spacing</code></td>
  </tr>
  <tr>
    <td>kerning</td>
    <td><code>com.hipertipo.spacingaxis.kerning</code></td>
  </tr>
</table>

We recommend `default`, `tight` and `loose` as standard primary names for spacing states.

<div class="alert alert-warning" role="alert" markdown='1'>
Note: The key can be changed to `com.fontbureau.spacingaxis` if this is to become an official FontBureau project.
{: .card-text }
</div>

### Spacing lib

The spacing lib contains data for one or more spacing states.

A **spacing state** is a snapshot of the font’s glyph width and left margin values at a given state.

Empty glyphs are described only by their width, as without contours there are also no left or right margins.

```xml
<key>com.hipertipo.spacingaxis.spacing</key>
<dict>
  <key>default</key>
  <dict>
    <key>a</key>
    <dict>
      <key>leftMargin</key>
      <real>74.98881178188978</real>
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
</dict>
```

### Kerning lib

The kerning lib contains data for one or more kerning states.

A **kerning state** is a snapshot of the font’s kerning pair values at a given state.

The value for each kerning pair is stored as an array of first glyph, second glyph, and kerning value.

The glyphs in each pair can be defined by glyph name or kerning group.

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
</dict>
```
