The Spacing Axis
================

Resources
---------

- [Spacing Axis Proposal by Frank Blokland](http://github.com/Microsoft/OpenTypeDesignVariationAxisTags/blob/master/Proposals/Spacing_Axis/ProposalSummary.md)
- [discussion of the proposal](https://github.com/Microsoft/OpenTypeDesignVariationAxisTags/issues/11)
- [discussion on TypeDrawers](https://typedrawers.com/discussion/2088/otvar-spacing-axis)

- - -

Development notes
-----------------

The spacing axis employs OpenType variation technology to provide a better tracking mechanism for fonts.

The spacing axis is used to collapse sidebearings until glyphs are almost touching.

The glyph margins correspond to the max value, `SPAC` guides indicate the minimal ‘collapsed’ value.

first experimental implementation: [Publica](http://fonts.hipertipo.com/publica/test/)

### Implementation details

- glyphs should contain two vertical guidelines to the left and right side of the glyph box
- both guidelines should be named 'SPAC'

### Appending guidelines

A Python script is used to create vertical guidelines at a distance `D` to the left and right of the glyph box, or twice this distance if the glyph has no contours.

### Generating spacing masters

...

### Kerning spacing masters

...
