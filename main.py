import sys
import os
import copy
from pathlib import Path
from PIL import Image

class Permutation_counter:
    def __init__(self) -> None:
        self.len = 0
        self.signs = []
        self.maxes = []
        self.counter = 0
        self.stop = False

    def add_sign(self, max):
        self.len += 1
        self.signs.append(0)
        self.maxes.append(max)

    def get(self):
        if self.stop:
            return None
        self.counter += 1
        i = 0
        ret = copy.copy(self.signs)
        while i < self.len:
            self.signs[i] += 1
            if self.signs[i] < self.maxes[i]:
                return ret
            else:
                self.signs[i] = 0
            i += 1
        self.stop = True
        return ret

    def skip(self, val):
        for i in range(val):
            self.get()

            

if __name__ == '__main__':
    try:
        main_path = Path(sys.argv[1])
    except:
        print('No path given')
        exit()

    if not os.path.isdir(main_path):
        print('No such directory exists')
        exit()

    dirs = os.listdir(main_path)
    calsses = len(dirs)
    print(f'{calsses} classes:')

    file_paths = []
    perm = Permutation_counter()
    i = 0
    for dir in dirs:
        print(f'\t{dir}')
        file_paths.append([])
        files = os.listdir(os.path.join(main_path, dir))
        if len(files) > 0:
            perm.add_sign(len(files))
        for file in files:
            path = os.path.join(main_path, dir, file)
            if os.path.isfile(path):    
                file_paths[i].append(path)
        i += 1

    counter = 0

    while 1:
        indexes = perm.get()
        image = Image.new('RGBA', (500, 500))
        if indexes:
            i = 0
            for index in indexes:
                element = Image.open(file_paths[i][index], 'r')
                image.paste(element, (0, 0), element)
                i += 1
        else:
            break
        image.save(os.path.join('results', str(counter) + '.png'))
        counter += 1

