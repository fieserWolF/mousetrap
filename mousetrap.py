#!/usr/bin/env python3

"""
MouseTrap v1.05 [03.07.2022] *** by fieserWolF
usage: mousetrap.py [-h] [-a ANIM_FILE] [-b BACKGROUND_FILE] [-p POINTER_FILE] [-g GHOST_FILE] [-xl POSX_LO_FILE] [-xh POSX_HI_FILE] [-y POSY_FILE]
                    [-l LOOK_FILE] [-ml MARKER_LO_FILE] [-mh MARKER_HI_FILE]

This records mouse movements and writes them to binary data files. Press F1 for help in the program.

options:
  -h, --help            show this help message and exit
  -a ANIM_FILE, --anim_file ANIM_FILE
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
  -l LOOK_FILE, --look_file LOOK_FILE
                        look-datafile: which sprite is used for each position (default="look.bin")
  -ml MARKER_LO_FILE, --marker_lo_file MARKER_LO_FILE
                        marker file (default="marker_lo.bin")
  -mh MARKER_HI_FILE, --marker_hi_file MARKER_HI_FILE
                        marker file (default="marker_hi.bin")

Example: ./mousetrap.py -b image.png -p ball.png -a rocket.webp -g ghost.png -xl posx-low.bin -xh posx-high.bin -y posy.bin -l look.bin -ml marker_lo.bin -mh marker_hi.bin
"""

import code.main as main




if __name__ == '__main__':
    main._main_procedure()
