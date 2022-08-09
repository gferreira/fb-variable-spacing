import os, sys

modulePath = os.getcwd()

if modulePath not in sys.path:
    print('installing variableSpacing module…')
    sys.path.append(modulePath)

print('initializing variableSpacing module…')
import variableSpacing
print(variableSpacing)
