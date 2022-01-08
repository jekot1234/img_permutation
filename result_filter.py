import os
import pygame
from PIL import Image

main_path = 'results'
dirs = os.listdir(main_path)

pygame.init()

im = Image.open(os.path.join(main_path, dirs[0]))
size = im.size

display = pygame.display.set_mode(size)

cont = True
i = 0
while 1:
    if cont:
        try:
            path = os.path.join(main_path, dirs[i])
        except:
            exit()
        cont = False
        image = Image.open(path)
        i += 1
        mode = image.mode
        size = image.size
        data = image.tobytes()
        pygm_image = pygame.image.fromstring(data, size, mode)
        display.blit(pygm_image, (0, 0))
        pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cont = True
                elif event.key == pygame.K_BACKSPACE:
                    cont = True
                    os.remove(path)
            elif event.type == pygame.QUIT:
                exit()
