from importlib import reload
import variableSpacing
reload(variableSpacing)

from variableSpacing import getComponentsLib

f = CurrentFont()
componentsLib = getComponentsLib(f)

newLib = {}

for glyphName in componentsLib.keys():
    print(componentsLib[glyphName])
    # if type(componentsLib[glyphName]) is dict:    
    #     parts = []
    #     # print(glyphName, componentsLib[glyphName])
    #     for item, value in componentsLib[glyphName]:
    #         print()
