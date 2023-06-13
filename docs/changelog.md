---
title  : Changelog
layout : default
class  : changelog
---

All notable changes to VariableSpacing are documented in this file.
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


0.1.5
-----

First public release.

- <span class='badge'>Changed</span> Changing private lib key from `com.hipertipo.spacingaxis` to `com.fontbureau.variableSpacing`.
- <span class='badge'>Changed</span> Cleaning up documentation content and layout.


0.1.4
-----

- <span class='badge'>Changed</span> Rewriting the code to keep components in place using a new algorithm (thanks DB!).
- <span class='badge'>Changed</span> Removing the `componentsLib` from the spacing states data format.
- <span class='badge'>Changed</span> Adding automatic documentation writer for the `spacingStates` Python module.
- <span class='badge'>Changed</span> Updating and improving the documentation.

0.1.3
-----

- <span class='badge'>Added</span> Adding functions to export/import spacing states to/from external JSON files in the SpacingStates tool.
- <span class='badge'>Added</span> Adding a new [Smart Margins] tool to change glyph margins without breaking component positioning.
- <span class='badge'>Changed</span> Moving code to save/load components lib to standalone functions.

[Smart Margins]: ../reference/smart-margins-tool/

0.1.2
-----

- <span class='badge'>Changed</span> Modified the components lib specification to allow multiple copies of the same component.
- <span class='badge'>Changed</span> Updated code, tools and demo fonts to the new data format.

0.1.1
-----

- <span class='badge'>Added</span> Added a new `components` lib to store component positions relative to glyph bounds.
- <span class='badge'>Added</span> Added documentation of the `spacingStates` module API.
- <span class='badge'>Changed</span> Improved overview, updated Spacing States format specification.
- <span class='badge'>Fixed</span> Fixed bug which caused components to shift when loading spacing states.

0.1.0
-----

Initial private release.
