---
title  : Installing VariableSpacing
layout : default
order  : 1
---

VariableSpacing tools are available as a Python module and as a RoboFont extension.
{: .lead }

* Table of Contents
{:toc}

<!--
The repository currently contains various scripts rather than a single module or tool, so there is no single central installation process.

See the sections below for instructions on how to use each one of the tools.
-->

Installing the Python module
----------------------------

<div class="alert alert-warning" role="alert" markdown='1'>
If you use the RoboFont extension, you don’t need to install the module separately – it is installed with the extension.
{: .card-text }
</div>

The `VariableSpacing` Python module contains various functions to create and edit spacing states in UFO fonts. The functions can be used in any Python environment alongside [FontParts](#).

To use the module outside of RoboFont, you can copy the file `variableSpacingLib.py` into the same repository as your script, so you can simply import the functions into your code:

```python
from variableSpacingLib import *
```

If you prefer to keep the Python module somewhere else, you’ll need to add its location to `sys.path` before you can use it:

```python
import sys

# path to local folder containing variableSpacingLib.py
libPath = '/someFolder/VariableSpacing/code/'

if libPath not in sys.path:
    sys.path.append(libPath)

# use some code from the module
from variableSpacingLib import *
```


Installing the RoboFont extension
---------------------------------

<div class="alert alert-warning" role="alert" markdown='1'>
The extension is being developed in RoboFont 3. It probably works in RoboFont 4 too, but the preview may look blurry.
{: .card-text }
</div>

### Installing with Mechanic

It is recommended to install the extension using [Mechanic], so it can automatically check for updates and install them.

1. Download the file `VariableSpacing.mechanic` from the repository.
2. Go to the Mechanic extension’s settings.
3. Use the plus button to add the `.mechanic` file to the list of [Single Extension Items].

[Mechanic]: http://github.com/robofont-mechanic/mechanic-2
[Single Extension Items]: http://robofont.com/documentation/extensions/managing-extension-streams/#adding-single-extension-items

### Installing from source

The VariableSpacing tools can also be used directly from the source code once you have downloaded it.

This mode allows developers to make changes to the code while using and testing the tools in RoboFont.

1. Clone the repository using `git clone` (recommended) or download the source code.
2. In the RoboFont Preferences window, go to [Extensions > Start Up Scripts].
3. Add the file `VariableSpacing/code/start.py` to the list of start-up scripts.
4. Save the settings and restart RoboFont – VariableSpacing will now appear under the *Extensions* menu.

[Extensions > Start Up Scripts]: http://robofont.com/documentation/workspace/preferences-window/extensions/#start-up-scripts


