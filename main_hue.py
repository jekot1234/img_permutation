import sys
import os
import copy
from pathlib import Path
from PIL import Image
import numpy as np
import colorsys

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def colorize(img, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    print(hue)
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(shift_hue(arr, hue/360.).astype('uint8'), 'RGBA')

    return new_img

class Permutation_counter:
    def __init__(self, hue = 1) -> None:
        self.len = 0
        self.signs = []
        self.maxes = []
        self.counter = 0
        self.stop = False
        self.hue = hue

    def add_sign(self, max):
        self.len += 1
        self.signs.append(0)
        self.maxes.append(max * self.hue)

    def get(self):
        if self.stop:
            return None
        self.counter += 1
        i = 0
        ret = copy.copy(self.signs)
        while i < self.len:
            self.signs[i] += 1
            if self.signs[i] < self.maxes[i]:
                return np.array(ret, dtype=np.uint16)
            else:
                self.signs[i] = 0
            i += 1
        self.stop = True
        return np.array(ret, dtype=np.uint16)

            

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
    try:
        hue = int(sys.argv[2])
    except:
        hue = 1
    
    hue_arr = np.arange(start = 0, stop = 360, step=360/hue, dtype=np.uint16)

    perm = Permutation_counter(hue)
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
        path_indexes = indexes // perm.hue
        hue_indexes = indexes % perm.hue
        image = Image.new('RGBA', (500, 500))
        if indexes is not None:
            i = 0
            for index in path_indexes:
                element = Image.open(file_paths[i][index], 'r')
                el = colorize(element, hue_arr[hue_indexes[i]])
                image.paste(el, (0, 0), el)
                i += 1
        else:
            break
        image.save(os.path.join('results', str(counter) + '.png'))
        counter += 1

