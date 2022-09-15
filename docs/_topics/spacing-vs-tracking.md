---
title  : Spaxing axis vs. tracking
layout : default
order  : 1
---

Looking into the fundamental differences between tracking and the spacing axis.
{: .lead }

* Table of Contents
{:toc}


Introduction
------------

In this page we are investigating and comparing two fundamentally different ways to a modify a font’s spacing:

1. through the **tracking function** provided by applications (the current standard approach)
2. through the **spacing axis** provided by the designer (a new approach)

We hope to demonstrate the advantages of the new approach in both tight and loose text settings.

### What we are looking at

The illustrations are generated with [DrawBot] from a designspace file and related UFO sources. Individual font locations are instantiated with [ufoProcessor].

The typesetting code was written from scratch for the purpose of this demonstration. It handles spacing, tracking and kerning. Tracking is expressed in *thousands of em*; kerning is expressed in font units.

The demo font is a simplified version of [Roboto] containing fewer characters and only a weight axis. The spacing axis is implemented using the [Spacing States tool].

The illustrations show a range of 5 steps with different spacing or tracking settings, going from loose (`100`) to default (`0`) to tight (`-100`). The colors are used to reveal how the different types of whitespace interact.


Basic typesetting
-----------------

Let’s start by looking at the basic typesetting mechanism at work, without kerning.

### Tracking

Tracking makes text tighter or looser by adding or removing a fixed amount of space *after* each glyph. The glyph boxes and their left and right margins don’t change.

![]({{ site.url }}/images/spacing-axis-vs-tracking_1.png){: .img-fluid}

In tight settings, the glyph boxes overlap with one another by a fixed negative amount. As the tracking value decreases, glyph collisions and occlusions appear unevenly. There is no limit for maximum or minimum tracking values.

### Spacing axis

The spacing axis makes text tighter or looser by modifying the glyph boxes, reducing or increasing the left and right margins. There is no tracking involved.

![]({{ site.url }}/images/spacing-axis-vs-tracking_2.png){: .img-fluid}

In tight settings, the left and right margins are reduced to zero causing glyph edges to touch; there is no lower setting beyond that. Glyph occlusions do not occur.


Adding kerning to the mix
-------------------------

To get the full picture we need to turn on kerning and add it to the visualization.

### Tracking

Automatic tracking employs **static kerning**: the same set of kerning values is used for default, tight and loose spacing settings.

![]({{ site.url }}/images/spacing-axis-vs-tracking_3.png){: .img-fluid}

In tight and loose settings, kerning values loose their reference and interact wit tracking in a way which designers cannot control.

### Spacing axis

The spacing axis employs **variable kerning**: the kerning values can be different for default, tight and loose spacing settings.

![]({{ site.url }}/images/spacing-axis-vs-tracking_4.png){: .img-fluid}

In tight settings, kerning is adjusted to allow characters to touch but not overlap. In loose settings, kerning is adjusted to give text an even rhtyhm.


Comparing the result
--------------------

The animations below allow us to compare the different results of tracking and the spacing axis:

### Tight spacing

<div id="carousel_tight" class="carousel slide carousel-fade" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="{{ site.url }}/images/spacing-axis-vs-tracking_7.png" class="d-block w-100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/spacing-axis-vs-tracking_8.png" class="d-block w-100" alt="...">
    </div>
  </div>
</div>

### Loose spacing

<div id="carousel_loose" class="carousel slide carousel-fade" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="{{ site.url }}/images/spacing-axis-vs-tracking_5.png" class="d-block w-100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/spacing-axis-vs-tracking_6.png" class="d-block w-100" alt="...">
    </div>
  </div>
</div>

### Advantages of the spacing axis

- better distribution of whitespace between the glyphs thanks to proportional scaling
- in tight settings: maximum tightness by allowing glyphs to touch but not overlap
- in loose settings: more even text rhythm 


[Roboto]: http://github.com/googlefonts/roboto
[DrawBot]: http://www.drawbot.com/
[ufoProcessor]: http://github.com/LettError/ufoProcessor
[Spacing States tool]: ../reference/spacing-states-tool
