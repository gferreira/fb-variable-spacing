import os, sys
from importlib import reload

modulePath = os.getcwd()

if modulePath not in sys.path:
    print('installing variableSpacing module…')
    sys.path.append(modulePath)

print('initializing variableSpacing module…')
import variableSpacing
reload(variableSpacing)
print(variableSpacing)
