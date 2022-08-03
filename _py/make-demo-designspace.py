import os
from hTools3.modules.varfonts import makeDesignSpace

familyName = 'VariableSpacingDemo'
axes = {
    "spacing" : dict(tag="SPAC", minimum=0, maximum=1000, default=0),

}
sources = {
    'normal' : dict(spacing=0),
    'tight'  : dict(spacing=1000),

}

designspacePath = os.path.join(os.getcwd(), 'VariableSpacingDemo.designspace')

designspace = makeDesignSpace(familyName, axes, sources)
designspace.write(designspacePath)
