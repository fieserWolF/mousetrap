#!/bin/bash -e

./mousetrap.py -i image.png -p ball.png -g ghost.png
#./mousetrap.py -i image.png -p ball.png -xl posx1.bin -xh posx2.bin -y posy.bin

exit 0
MouseTrap v1.03 [15.01.2022] *** by fieserWolF
usage: mousetrap.py [-h] [-i IMAGE_FILE] [-p POINTER_FILE] [-g GHOST_FILE] [-xl POSX_LO_FILE] [-xh POSX_HI_FILE] [-y POSY_FILE] [-ml MARKER_LO_FILE]
                    [-mh MARKER_HI_FILE]

This records mouse movements and writes them to binary data files. Press F1 for help in the program.

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_FILE, --image_file IMAGE_FILE
                        image file
  -p POINTER_FILE, --pointer_file POINTER_FILE
                        optional pointer image file: it follows the mousepointer
  -g GHOST_FILE, --ghost_file GHOST_FILE
                        optional ghost pointer image file: it follows the recorded data
  -xl POSX_LO_FILE, --posx_lo_file POSX_LO_FILE
                        posx low file (default="posx_lo.bin")
  -xh POSX_HI_FILE, --posx_hi_file POSX_HI_FILE
                        posx high file (default="posx_hi.bin")
  -y POSY_FILE, --posy_file POSY_FILE
                        posy file (default="posy.bin")
  -ml MARKER_LO_FILE, --marker_lo_file MARKER_LO_FILE
                        marker file (default="marker_lo.bin")
  -mh MARKER_HI_FILE, --marker_hi_file MARKER_HI_FILE
                        marker file (default="marker_hi.bin")

Example: ./mousetrap.py -i image.png -p ball.png -g ghost.png -xl posx-low.bin -xh posx-high.bin -y posy.bin -ml marker_lo.bin -mh marker_hi.bin
