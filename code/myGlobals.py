import os
import sys
from tkinter import *
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__) ))
    return os.path.join(base_path, '../'+relative_path)



def _global_constants():
        return None
    
#GFX_PLAY = resource_path('resources/icon_play.xbm')
GFX_RESET = resource_path('resources/icon_reset.xbm')
#GFX_EXIT = resource_path('resources/icon_exit.xbm')

GFX_FORWARD = resource_path('resources/icon_forward.xbm')
GFX_STOP = resource_path('resources/icon_pause.xbm')
GFX_BACKWARD = resource_path('resources/icon_backward.xbm')

GFX_NEXT = resource_path('resources/icon_next.xbm')
GFX_PREVIOUS = resource_path('resources/icon_previous.xbm')

GFX_MARKER_SET = resource_path('resources/icon_set_marker.xbm')
GFX_MARKER_NEXT = resource_path('resources/icon_next_marker.xbm')
GFX_MARKER_PREV = resource_path('resources/icon_prev_marker.xbm')
GFX_MARKER_DELETE = resource_path('resources/icon_del_marker.xbm')
GFX_MARKER_GOTO = resource_path('resources/icon_goto_marker.xbm')

GFX_RECORD_ANIMATION = resource_path('resources/icon_record_animation.xbm')

GFX_TIMELINE_CURSOR = resource_path('resources/cursor.png')
GFX_TIMELINE_MARKER = resource_path('resources/marker.png')


#GFX_PAUSE = resource_path('resources/icon_pause.xbm')
#GFX_REWIND = resource_path('resources/icon_rewind.xbm')



PROGNAME = 'MouseTrap';
VERSION = '1.05';
LAST_EDITED = '03.07.2022';

IMAGE_WIDTH     = 320
IMAGE_HEIGHT    = 200
IMAGE_VISIBLE_WIDTH     = IMAGE_WIDTH*2
IMAGE_VISIBLE_HEIGHT    = IMAGE_HEIGHT*2

TIMELINE_WIDTH    = IMAGE_VISIBLE_WIDTH
TIMELINE_HEIGHT    = 20

OBJ_WIDTH    = (11*2)*2
OBJ_HEIGHT    = 23*2

GHOST_WIDTH     = OBJ_WIDTH
GHOST_HEIGHT    = OBJ_HEIGHT

MARKER_SINGLE_WIDTH    = 3
MARKER_SINGLE_HEIGHT    = TIMELINE_HEIGHT

CURSOR_WIDTH    = 2
CURSOR_HEIGHT    = TIMELINE_HEIGHT

BGCOLOR='#cccccc'
BGCOLOR_LIGHT='#dddddd'
BGCOLOR2='#ccccff'

FRAME_PADX = 2
FRAME_PADY = 2
FRAME_BORDER = 4

#animation_refresh_seconds = 0.01

MOUSEPOINTER_HAND = 'hand2'
MOUSEPOINTER_NORMAL = 'tcross'
MOUSEPOINTER_NONE = 'X_cursor'

PLAYER_SPEED_MAX = 100



#global variables
def _global_variables():
        return None

root = Tk()
args = None

mousepointer_image = MOUSEPOINTER_NORMAL

data_posx = []
data_posy = []
data_animation = []
data_marker = []
data_length = 0
flag_record = False

scale_settings_list=[]
scale_settings_list_default=[]
timeline_position = IntVar()
slider_timeline = Scale()
player_speed = IntVar()

background_image = PilImage.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), 'black')
image_background_Tk = None
label_background_image = Label()

timeline_image = PilImage.new('RGBA', (TIMELINE_WIDTH, TIMELINE_HEIGHT), 'black')
image_timeline_Tk = None
label_timeline_image = Label()

ball_image = PilImage.new('RGBA', (OBJ_WIDTH, OBJ_HEIGHT), 'black')
ghost_image = PilImage.new('RGBA', (GHOST_WIDTH, GHOST_HEIGHT), 'black')
marker_single_image = PilImage.new('RGBA', (MARKER_SINGLE_WIDTH, MARKER_SINGLE_HEIGHT), 'black')
cursor_timeline_image = PilImage.new('RGBA', (CURSOR_WIDTH, CURSOR_HEIGHT), 'black')
#anim_image = PilImage.new('RGBA', (OBJ_WIDTH, OBJ_HEIGHT), 'black')
anim_image = []
anim_image_number = IntVar()
anim_image_max = 50

button_play = Button()
button_forward = Button()
button_backward = Button()
button_record_animation = Button()

textvariable_mode   = StringVar()
textvariable_coords = StringVar()
textvariable_pos   = StringVar()
textvariable_marker = StringVar()

mouse_posx = 0
mouse_posy = 0

ghost_posx = 0
ghost_posy = 0
ghost_animation = 0

play_pos = 0
marker_number = 0

last_posx   = 0
last_posy   = 0
last_marker   = 0

mode='idle'
command_play = 'stop'
command_record_animation = 'stop'

