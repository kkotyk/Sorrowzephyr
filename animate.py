import PIL.Image
import PIL.ImageOps
import aalib
import subprocess as sp

import os
import sys

term_size = sp.check_output('stty size', shell=True).decode('utf-8')
term_size = term_size.split(' ')
term_size = (int(term_size[0]),int(term_size[1]))


aalib_screen_height= int(term_size[0]*0.95)
aalib_screen_width= int(term_size[1] * 0.47)

print(aalib_screen_height, aalib_screen_width)

game_dir = sys.argv[1]

for d in os.listdir(game_dir):
    for jpg in os.listdir(game_dir+"/"+d+"/animations"):
        if ".jpg" in jpg:
            with open(game_dir+"/"+d+"/animations/"+jpg, 'rb') as f:

                screen = aalib.AsciiScreen(width=aalib_screen_width, height=aalib_screen_height)
                raw_image = PIL.Image.open(f).convert('L').resize(screen.virtual_size)

                #inverted=PIL.ImageOps.invert(raw_image)
                screen.put_image((0,0), raw_image)
                new_ascii = screen.render()

                txt_file = os.path.splitext(jpg)[0]+'.txt'

                with open(game_dir+"/"+d+"/animations/"+txt_file, 'w') as output:
                    output.write(new_ascii)
