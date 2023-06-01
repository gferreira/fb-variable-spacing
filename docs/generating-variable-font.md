---
title  : Generating variable fonts with a spacing axis
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
├── MyFont_loose.ufo*
└── MyFont.ttf
```

\* generated automatically and deleted at the end of the process


Designspace file
----------------

```xml
<designspace>
  <axes>
    <axis tag="SPAC" name="spacing" minimum="-100" maximum="100" default="0"/>
  </axes>
  <sources>
    <source filename="MyFont_default.ufo" name="normal" familyname="MyFont" stylename="normal">
      <location>
        <dimension name="spacing" xvalue="0"/>
      </location>
    </source>
    <source filename="MyFont_tight.ufo" name="tight" familyname="MyFont" stylename="tight">
      <location>
        <dimension name="spacing" xvalue="-100"/>
      </location>
    </source>
    <source filename="MyFont_loose.ufo" name="loose" familyname="MyFont" stylename="loose">
      <location>
        <dimension name="spacing" xvalue="100"/>
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

# build temporary 'tight' and 'loose' spacing sources
from variableSpacing import buildSpacingSources
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

<div class="alert alert-primary" role="alert" markdown='1'>
For a more complex example, see the [build script for Roboto Flex SPAC](http://github.com/gferreira/roboto-flex-spac/blob/master/scripts/build-variable-font.py).
{: .card-text }
</div>


