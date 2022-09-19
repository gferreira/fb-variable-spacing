---
title  : Changelog
layout : default
class  : changelog
order  : 3
---

All notable changes to Variable Spacing are documented in this file.
{: .lead }

<!--

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
VarTools adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

semantic versioning: MAJOR.MINOR.PATCH
see http://keepachangelog.com/

| MAJOR | incompatible API changes                           |
| MINOR | new functionality in a backwards compatible manner |
| PATCH | backwards compatible bug fixes                     |

additional labels for pre-release and build 
as extensions to the MAJOR.MINOR.PATCH format

types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

-->

0.1.2
-----

- <span class='badge'>Changed</span> Modified the [components lib specification] to allow multiple copies of the same component.
- <span class='badge'>Changed</span> Updated code, tools and demo fonts to the new data format.

[components lib specification]: ../reference/spacing-states-format/#components-lib

0.1.1
-----

- <span class='badge'>Added</span> Added a new `components` lib to store component positions relative to glyph bounds.
- <span class='badge'>Added</span> Added documentation of the `spacingStates` module API.
- <span class='badge'>Changed</span> Improved overview, updated Spacing States format specification.
- <span class='badge'>Fixed</span> Fixed bug which caused components to shift when loading spacing states.

0.1.0
-----

Initial private release.
