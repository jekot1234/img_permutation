import sys
import os
import copy
from pathlib import Path
from PIL import Image
import numpy as np
import colorsys
import pygame

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h += hout 
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def colorize(img, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
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


    pygame.init()

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

    if not os.path.isdir('results'):
        os.mkdir('results')

    file_paths = []
    try:
        hue = int(sys.argv[2])
    except:
        hue = 1

    try:
        offset = int(sys.argv[3])
    except:
        offset = 0
    
    hue_arr = np.arange(start = 0, stop = 360, step=360/hue, dtype=np.uint16) + offset

    perm = Permutation_counter(hue)
    i = 0
    for dir in dirs:
        if os.path.isdir(os.path.join(main_path, dir)):
            file_paths.append([])
            files = os.listdir(os.path.join(main_path, dir))
            fs = 0
            for file in files:
                path = os.path.join(main_path, dir, file)
                if os.path.isfile(path) and path.endswith('png'):    
                    file_paths[i].append(path)
                    fs += 1
            if fs > 0:
                perm.add_sign(fs)
            i += 1
    counter = 0
    size = (500, 500)
    with Image.open(file_paths[0][0], 'r') as im:
        size = im.size

    display = pygame.display.set_mode(size)

    next = True
    while 1:

        next = False
        indexes = perm.get()
        if indexes is not None:
            path_indexes = indexes // perm.hue
            hue_indexes = indexes % perm.hue
        else:
            break
        image = Image.new('RGBA', size)
        i = 0
        for index in path_indexes:
            element = Image.open(file_paths[i][index], 'r')
            el = colorize(element, hue_arr[hue_indexes[i]])
            image.paste(el, (0, 0), el)
            i += 1

        mode = image.mode
        size = image.size
        data = image.tobytes()
        pygm_image = pygame.image.fromstring(data, size, mode)
        display.blit(pygm_image, (0, 0))
        pygame.display.update()
        image.save(os.path.join('results', str(counter) + '.png'))
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()