The Spacing Axis
================

The spacing axis employs OpenType variation technology to provide a better tracking mechanism for fonts.


Resources
---------

- [Spacing Axis Proposal by Frank Blokland](http://github.com/Microsoft/OpenTypeDesignVariationAxisTags/blob/master/Proposals/Spacing_Axis/ProposalSummary.md)
- [discussion of the proposal](https://github.com/Microsoft/OpenTypeDesignVariationAxisTags/issues/11)
- [discussion on TypeDrawers](https://typedrawers.com/discussion/2088/otvar-spacing-axis)


Development notes
-----------------

First experimental implementation: [Publica](http://fonts.hipertipo.com/publica/test/) (grotesk sans)

- spacing axis is used to collapse sidebearings until glyphs are almost touching
- glyph margins correspond to the maximum value, `SPAC` guides indicate the minimum ‘collapsed’ value

### Implementation details

- glyphs contain two vertical guidelines to the left and right side of the glyph box
- both guidelines are named `SPAC`

### Appending guidelines

A Python script is used to create vertical guidelines at a distance `D` to the left and right of the glyph box, or twice this distance if the glyph has no contours.

### Generating spacing masters

...

### Kerning spacing masters

...
