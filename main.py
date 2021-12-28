import sys
import os
from pathlib import Path
from PIL import Image

#
try:
    main_path = Path(sys.argv[1])
except:
    print('No path given')
    exit()
if not os.path.isdir(main_path):
    print('No such directory exists')
    exit()

dirs = os.listdir(main_path)
print(f'{len(dirs)} classes:')

for d in dirs:
    print(f'\t{d}')
