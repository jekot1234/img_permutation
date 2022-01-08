import os
import sys
import numpy as np
from PIL import Image
from pathlib import Path
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

try:
        main_path = Path(sys.argv[1])
except:
    print('No path given')
    exit()

if not os.path.isdir(main_path):
    print('No such directory exists')
    exit()

file_paths = []

dirs = os.listdir(main_path)
dirs.sort()
i = 0

try:
    hue = int(sys.argv[2])
except:
    hue = 1

try:
    offset = int(sys.argv[3])
except:
    offset = 0

hue_arr = np.arange(start = 0, stop = 360, step=360/hue, dtype=np.uint16) + offset

for dir in dirs:
        if os.path.isdir(os.path.join(main_path, dir)):
            files = os.listdir(os.path.join(main_path, dir))
            for file in files:
                path = os.path.join(main_path, dir, file)
                if os.path.isfile(path) and path.endswith('png'):    
                    file_paths.append(path)
            i += 1
print(file_paths)

for p in file_paths:
    counter = 0
    for h in hue_arr:
        image = Image.open(p)
        im = colorize(image, h)
        im.save(p[:-4] + str(counter) + '.png')
        counter += 1