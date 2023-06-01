---
title  : Overview of VariableSpacing
layout : default
order  : 1
---

Methodology and tools to add a spacing axis to variable fonts.
{: .lead }

* Table of Contents
{:toc}


### The spacing axis

Variable fonts make it possible to create a variation axis to change the spacing or ‘tracking’ of a font. This designer-made tracking included in the font is superior to the automatic tracking provided by applications or CSS.

Assuming that all glyph contours in a font remain the same when the spacing is changed\*, the visual difference between spacing sources is restricted to:

- different side-bearings (or rather: *left margin* and *glyph width*)
- different kerning values (but same pairs and kerning groups)

<div class="alert alert-primary" role="alert" markdown='1'>
\* Frank Blokland’s [original proposal](http://github.com/Microsoft/OpenTypeDesignVariationAxisTags/blob/master/Proposals/Spacing_Axis/ProposalSummary.md) mentions the possibility to use this axis to also make adjustments to the *shape* of some glyphs – for example retracting serifs as the margins get narrower. This feature can be added in the future.
{: .card-text }
</div>

### Practical considerations

In the design stage, when the glyph shapes are still changing, it is important to have an easy way to keep contours synchronized between the various spacing sources.

### Streamlined workflow

**The VariableSpacing workflow aims to reduce data duplication and streamline the process of creating and editing the spacing axis.**

The various ‘spacing states’ – *normal*, *tight*, *loose* – can be stored in the same UFO: in the font lib, using a custom key.

This way we can have **one set of glyph contours and multiple spacing states** which we can load into the font, one at a time.

### Variable font generation

When it's time to generate a variable font, the spacing states are exported into separate temporary UFOs, which are deleted at the end of the process.
