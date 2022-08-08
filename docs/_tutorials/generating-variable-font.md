---
title  : Generating variable font with spacing axis
layout : default
order  : 1
---

How to generate a variable font with a spacing axis using the spacing states as sources.
{: .lead }

* Table of Contents
{:toc}


Folder structure
----------------

```
folder/
├── MyFont.designspace
├── MyFont_default.ufo
├── MyFont_tight.ufo*
└── MyFont.ttf
```

\* generated automatically and deleted at the end of the process


Designspace file
----------------

```xml
<designspace>
  <axes>
    <axis tag="SPAC" name="spacing" minimum="-1000" maximum="0" default="0"/>
  </axes>
  <sources>
    <source filename="MyFont_default.ufo" name="normal" familyname="MyFont" stylename="normal">
      <lib copy="1"/>
      <groups copy="1"/>
      <features copy="1"/>
      <info copy="1"/>
      <location>
        <dimension name="spacing" xvalue="0"/>
      </location>
    </source>
    <source filename="MyFont_tight.ufo" name="tight" familyname="MyFont" stylename="tight">
      <location>
        <dimension name="spacing" xvalue="-1000"/>
      </location>
    </source>
  </sources>
</designspace>
```


Build script
------------

```python
# parent folder with ufo source(s) and designspace file
folder = '/folder/'

# build temporary 'tight' spacing sources
from variableSpacingLib import buildSpacingSources
newSources = buildSpacingSources(folder)

# generate variable font
from fontmake.font_project import FontProject
designspacePath = os.path.join(folder, 'MyFont.designspace')
varFontPath = os.path.join(folder, 'MyFont.ttf')
P = FontProject()
P.build_variable_font(designspacePath, output_path=varFontPath, verbose=True)

# clear temporary sources
import shutil
for ufoPath in newSources:
    shutil.rmtree(ufoPath)
```
