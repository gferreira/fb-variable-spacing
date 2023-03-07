import os, sys
from importlib import reload

# add module
libFolder = os.getcwd()
print('adding variableSpacing module to sys.path...')
sys.path.append(libFolder)
