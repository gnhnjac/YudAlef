import os
import subprocess
base_path = os.path.dirname(os.path.realpath(__file__))

path = os.path.join(base_path, 'MinGW/bin/')
subprocess.run(['setx', 'path', f'%PATH%;{path}'])
print("Added mingw to path.")