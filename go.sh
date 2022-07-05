#!/bin/bash -e

# rocket - with animation
./mousetrap.py -ai rocket.webp -b rocket-bg.png -p ball.png -xl ./data-rocket/posx_lo.bin -xh ./data-rocket/posx_hi.bin -y ./data-rocket/posy.bin -a ./data-rocket/animation.bin -ml ./data-rocket/marker_lo.bin -mh ./data-rocket/marker_hi.bin

# escher - no animation
#./mousetrap.py -b escher-bg.png -p ball.png -g ghost.png -xl ./data-escher/posx_lo.bin -xh ./data-escher/posx_hi.bin -y ./data-escher/posy.bin -a ./data-escher/animation.bin -ml ./data-escher/marker_lo.bin -mh ./data-escher/marker_hi.bin

exit 0

MouseTrap v1.05 [03.07.2022] *** by fieserWolF
usage: mousetrap.py [-h] [-ai ANIM_IMAGE_FILE] [-b BACKGROUND_FILE] [-p POINTER_FILE] [-g GHOST_FILE] [-xl POSX_LO_FILE] [-xh POSX_HI_FILE]
                    [-y POSY_FILE] [-a ANIM_FILE] [-ml MARKER_LO_FILE] [-mh MARKER_HI_FILE]

This records mouse movements and writes them to binary data files. Press F1 for help in the program.

options:
  -h, --help            show this help message and exit
  -ai ANIM_IMAGE_FILE, --anim_image_file ANIM_IMAGE_FILE
                        animation pointer image file
  -b BACKGROUND_FILE, --background_file BACKGROUND_FILE
                        background image file (320x200 pixel)
  -p POINTER_FILE, --pointer_file POINTER_FILE
                        optional pointer image file (44x46 pixel): it follows the mousepointer
  -g GHOST_FILE, --ghost_file GHOST_FILE
                        optional ghost pointer image file (44x46 pixel): it follows the recorded data
  -xl POSX_LO_FILE, --posx_lo_file POSX_LO_FILE
                        posx low file (default="posx_lo.bin")
  -xh POSX_HI_FILE, --posx_hi_file POSX_HI_FILE
                        posx high file (default="posx_hi.bin")
  -y POSY_FILE, --posy_file POSY_FILE
                        posy file (default="posy.bin")
  -a ANIM_FILE, --animation_file ANIM_FILE
                        animation-datafile: which sprite is used for each position (default="animation.bin")
  -ml MARKER_LO_FILE, --marker_lo_file MARKER_LO_FILE
                        marker file (default="marker_lo.bin")
  -mh MARKER_HI_FILE, --marker_hi_file MARKER_HI_FILE
                        marker file (default="marker_hi.bin")

Example: ./mousetrap.py -b image.png -p ball.png -ai rocket.webp -g ghost.png -xl posx-low.bin -xh posx-high.bin -y posy.bin -a animation.bin -ml marker_lo.bin -mh marker_hi.bin
