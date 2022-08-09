---
title  : Overview of Variable Spacing
layout : default
order  : 1
---

A method to add a spacing axis to variable fonts.
{: .lead }

* Table of Contents
{:toc}

### The spacing axis

Variable fonts make it possible to create a variation axis to change the spacing or ‘tracking’ of a font. This designer-made tracking included in the fonts is superior to the automatic tracking provided by applications or CSS.

Given a ‘pure’ spacing axis with no variation in the opaque shapes (contours), and ignoring obvious differences in font info values (style name), the difference between two spacing sources is restricted to:

- different side-bearings (or rather: left margin, glyph width)
- different kerning values (but same pairs and kerning groups)

**The contours are exactly the same in the two spacing sources.**

### Implementing the spacing axis

In the design stage, when the glyph shapes are still changing, it is important to have an easy way to keep contours synchronized between the two spacing sources.

### Streamlined implementation process

**This proposal aims to reduce data duplication and streamline the process of creating and editing the spacing axis.**

The various ‘spacing states’ – *normal*, *tight*, *loose* – can be stored in the same UFO: in the font lib, using a custom key.

This way we can have **one set of glyph contours and multiple spacing states** which we can load into the font, one at a time.

### Variable font generation

When generating the variable font, the spacing states can be exported into separate temporary UFOs, which are deleted at the end of the process.

{% comment %}
### This project includes

- data format and tools to work with variable fonts containing a spacing axis
- demo fonts and build scripts
- DrawBot-based tools to visualize spacing and kerning

{% endcomment %}
