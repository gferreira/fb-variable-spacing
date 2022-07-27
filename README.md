The Spacing axis
================

The spacing axis is different from tracking:

- Tracking is the mechanical addition/subtraction of equal space to each glyph.
- The spacing axis is proportional to the side-bearings of each glyph.


Resources
---------

- [Spacing Axis Proposal by Frank Blokland](http://github.com/Microsoft/OpenTypeDesignVariationAxisTags/blob/master/Proposals/Spacing_Axis/ProposalSummary.md)
- [discussion of the proposal](https://github.com/Microsoft/OpenTypeDesignVariationAxisTags/issues/11)
- [discussion on TypeDrawers](https://typedrawers.com/discussion/2088/otvar-spacing-axis)




- - -








The spacing axis employs OpenType variation technology to provide a better tracking mechanism for fonts.

Tracking functionality provided by apps apply the same number of units to all glyphs in the font. The tracking axis 


The tracking axis is used to collapse sidebearings


- glyph margins indicate the max value, TRAC guides indicate the min value


# vertical guidelines

- glyphs should contain two vertical guidelines to the left and right side of the glyph box
- both guidelines should be named 'TRAC'






append Guidelines script

vertical guidelines placed at a distance D to the left and right of the glyph shape, or twice this distance if the glyph has no contours



