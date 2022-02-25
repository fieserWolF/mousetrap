#!/usr/bin/env python3

"""
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
"""

import os
import sys
from PIL import ImageTk
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import argparse
import struct


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



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

GFX_TIMELINE_CURSOR = resource_path('resources/cursor.png')
GFX_TIMELINE_MARKER = resource_path('resources/marker.png')

#GFX_PAUSE = resource_path('resources/icon_pause.xbm')
#GFX_REWIND = resource_path('resources/icon_rewind.xbm')



PROGNAME = 'MouseTrap';
VERSION = '1.03';
DATUM = '17.01.2022';

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
data_marker = []
data_length = 0
flag_record = False

scale_settings_list=[]
scale_settings_list_default=[]
timeline_position = IntVar()
slider_timeline = Scale()
player_speed = IntVar()

my_image = PilImage.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), 'black')
image_Tk = ImageTk.PhotoImage(my_image)
label_image = Label()

timeline_image = PilImage.new('RGBA', (TIMELINE_WIDTH, TIMELINE_HEIGHT), 'black')
image_timeline_Tk = ImageTk.PhotoImage(timeline_image)
label_timeline_image = Label()

ball_image = PilImage.new('RGBA', (OBJ_WIDTH, OBJ_HEIGHT), 'black')
ghost_image = PilImage.new('RGBA', (GHOST_WIDTH, GHOST_HEIGHT), 'black')
marker_single_image = PilImage.new('RGBA', (MARKER_SINGLE_WIDTH, MARKER_SINGLE_HEIGHT), 'black')
cursor_timeline_image = PilImage.new('RGBA', (CURSOR_WIDTH, CURSOR_HEIGHT), 'black')

button_play = Button()
button_forward = Button()
button_backward = Button()

textvariable_mode   = StringVar()
textvariable_coords = StringVar()
textvariable_pos   = StringVar()
textvariable_marker = StringVar()

mouse_posx = 0
mouse_posy = 0

ghost_posx = 0
ghost_posy = 0

play_pos = 0
marker_number = 0

last_posx   = 0
last_posy   = 0
last_marker   = 0

mode='idle'
command_play = 'stop'




def play_thread():
    if (command_play == 'play forward'): action_play_next()
    if (command_play == 'play backward'): action_play_prev()
    root.after(PLAYER_SPEED_MAX+1-int(player_speed.get()), play_thread)

def jump_to_marker():
    global play_pos, ghost_posx, ghost_posy
    play_pos = data_marker[marker_number]
    timeline_position.set( int(( play_pos / len(data_posx) )*100) )

    ghost_posx = data_posx[play_pos]*2
    ghost_posy = data_posy[play_pos]*2

    if (mode == 'play') : action_image_refresh()
    else :  action_image_refresh()


def save_some_data(
    filename,
    data
):
    print ('Opening file "%s" for writing data (%d ($%04x) bytes)...' % (filename, len(data), len(data)))
    try:
        file_out = open(filename , 'wb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None
    file_out.write(bytearray(data))
    file_out.close()


def action_SaveData():

    #posx low
    tmp = []
    for i in data_posx :
        tmp.append(i & 0b11111111)    
    save_some_data(args.posx_lo_file, tmp)

    #posx high
    tmp = []
    for i in data_posx :
        tmp.append(i >> 8)    
    save_some_data(args.posx_hi_file, tmp)

    #posy
    save_some_data(args.posy_file, data_posy)

    #marker low
    tmp = []
    for i in data_marker :
        tmp.append(i & 0b11111111)    
    save_some_data(args.marker_lo_file, tmp)

    #marker high
    tmp = []
    for i in data_marker :
        tmp.append(i >> 8)    
    save_some_data(args.marker_hi_file, tmp)


def load_some_data (
    filename
) :
	#open input file
    print ('Opening file "%s" for reading...' % filename)
    try:
        file_in = open(filename , 'rb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None

    buffer=[]
    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])

    return buffer




def load_data() :
    global data_posx, data_posy, data_marker, ghost_posx, ghost_posy, play_pos

    tmp_l = load_some_data(args.posx_lo_file)
    tmp_h = load_some_data(args.posx_hi_file)
    
    data_posx = []
    for i in range(len(tmp_l)) :
        data_posx.append(tmp_l[i] + (tmp_h[i] << 8))
    
    data_posy = load_some_data(args.posy_file)

    tmp_l = load_some_data(args.marker_lo_file)
    tmp_h = load_some_data(args.marker_hi_file)
    data_marker = []
    for i in range(len(tmp_l)) :
        data_marker.append(tmp_l[i] + (tmp_h[i] << 8))


    play_pos = 0
    timeline_position.set(0)

    if (len(data_posx)>0) :
        ghost_posx = data_posx[play_pos]*2
        ghost_posy = data_posy[play_pos]*2

    update_timeline()
    action_image_refresh()
   


def load_image(
	filename
):
    global my_image
    print('Opening background-image "%s"...' % filename)

    my_image = PilImage.open(filename)
    my_image = my_image.resize((IMAGE_VISIBLE_WIDTH, IMAGE_VISIBLE_HEIGHT))
    my_image = my_image.convert('RGB')
        


def update_timeline():
    global timeline_image

    #new clear timeline
    timeline_image = PilImage.new('RGBA', (TIMELINE_WIDTH, TIMELINE_HEIGHT), 'black')

    #add markers
    for i in range(0,len(data_marker)) :
        xpos = int ( (data_marker[i] / len(data_posx)) * TIMELINE_WIDTH)
        timeline_image.paste(marker_single_image, (xpos,0), marker_single_image)

    action_image_refresh()
 



def action_image_refresh():
    global image_Tk, image_timeline_Tk
    
    #image
    final_image = my_image.copy()    
    final_image.paste(ghost_image, (ghost_posx, ghost_posy), ghost_image)
    final_image.paste(ball_image, (mouse_posx, mouse_posy), ball_image)
    image_Tk = ImageTk.PhotoImage(final_image)
    label_image.configure(image=image_Tk)
    label_image.image = final_image # keep a reference!
    


    #timeline
    xpos = int ( (play_pos / len(data_posx)) * TIMELINE_WIDTH)
    final_image = timeline_image.copy()    
    #add cursor
    final_image.paste(cursor_timeline_image, (xpos, 0), cursor_timeline_image)
    image_timeline_Tk = ImageTk.PhotoImage(final_image)
    label_timeline_image.configure(image=image_timeline_Tk)
    label_timeline_image.image = final_image # keep a reference!

    update_info()



def load_image_ball(
	filename
):
    global ball_image
    
    print('Opening ball-image "%s"...' % filename)

    ball_image = PilImage.open(filename)
    ball_image = ball_image.resize((OBJ_WIDTH, OBJ_HEIGHT))
    ball_image = ball_image.convert("RGBA")


def load_image_ghost(
	filename
):
    global ghost_image
    
    print('Opening ghost-image "%s"...' % filename)

    ghost_image = PilImage.open(filename)
    ghost_image = ghost_image.resize((GHOST_WIDTH, GHOST_HEIGHT))
    ghost_image = ghost_image.convert("RGBA")


def load_image_marker(
	filename
):
    global marker_single_image
    
    print('Opening marker-image "%s"...' % filename)

    marker_single_image = PilImage.open(filename)
    marker_single_image = marker_single_image.convert("RGBA")

def load_image_cursor(
	filename
):
    global cursor_timeline_image
    
    print('Opening cursor-image "%s"...' % filename)

    cursor_timeline_image = PilImage.open(filename)
    cursor_timeline_image = cursor_timeline_image.convert("RGBA")







def quit_application():
    global command_play
    command_play = 'exit'
    #root.quit()    
    if messagebox.askokcancel("Quit", "Do you want to quit?"): root.quit()    #root.destroy()


#keyboard shortcuts

    



def create_gui_drop_down_menu (
	root
) :
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    datamenu = Menu(menu)
    infomenu = Menu(menu)

#    filemenu.add_command(label="open data", command=action_OpenFile_Data, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="open image", command=action_OpenFile_Image, underline=5, accelerator="Alt+I")
    filemenu.add_command(label="open pointer", command=action_OpenFile_Pointer, underline=5, accelerator="Alt+P")
    filemenu.add_command(label="open ghost", command=action_OpenFile_Ghost, underline=5, accelerator="Alt+G")
    filemenu.add_command(label="save data", command=action_SaveData, underline=0, accelerator="Alt+S")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Alt+Q")

    datamenu.add_command(label="reload data", command=load_data, underline=0, accelerator="Alt-R")
    datamenu.add_separator()
    datamenu.add_command(label="clear rest of data", command=action_delete_data_rest)
    datamenu.add_command(label="clear rest of markers", command=action_marker_delete_rest)
    datamenu.add_command(label="clear all data", command=action_clear_data)
    datamenu.add_command(label="clear all markers", command=action_marker_clear_all)
    datamenu.add_command(label="jump to next marker", command=action_marker_next, underline=8, accelerator="n")
    datamenu.add_command(label="jump to previous marker", command=action_marker_previous, underline=8, accelerator="p")

    infomenu.add_command(label="help", command=action_Info, underline=0, accelerator="f1")

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu)
    menu.add_cascade(label="data", menu=datamenu)
    menu.add_cascade(label="info", menu=infomenu)









def action_marker_clear_all():
    global data_marker
    print('Clearing markers...')
    data_marker = []
    update_timeline()
    action_image_refresh()

def action_marker_delete():
    global data_marker
    if (marker_number < len(data_marker)) :
        #print('Deleting marker %d...' % (int(marker_number+1)))
        del data_marker[marker_number]
        update_timeline()
        action_image_refresh()


#def action_OpenFile_Data():    
#    ftypes = [('Data Files', '*.bin')]
#    user_filename_open = askopenfilename(filetypes = ftypes)
#    if not user_filename_open : return None
#    load_data(user_filename_open)


def action_OpenFile_Image():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    load_image(user_filename_open)



def action_OpenFile_Pointer():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    load_image_ball(user_filename_open)

def action_OpenFile_Ghost():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    load_image_ghost(user_filename_open)


        
def play_pos_to_ghost() :
    global play_pos, ghost_posx, ghost_posy

    #sanity checks
    if (play_pos < 0) : play_pos = len(data_posx)-1
    if (play_pos > len(data_posx)-1) : play_pos = 0

    if (len(data_posx)>0) :
        ghost_posx = data_posx[play_pos]*2
        ghost_posy = data_posy[play_pos]*2
        timeline_position.set( int(( play_pos / len(data_posx) )*100) )
    action_image_refresh()
#    root.update()


def action_Record_Stop():
    global flag_record, mode
    flag_record = False
    mode = 'idle'
    update_timeline()
    action_image_refresh()
    timeline_position.set( int(( play_pos / len(data_posx) )*100) )


def action_play_stop () :
    global command_play
    command_play = 'stop'
    button_forward.configure(relief=RAISED)
    button_backward.configure(relief=RAISED)
    
def action_play_forward () :
    global command_play
    if (command_play == 'play forward') :
        command_play = 'stop'
        button_forward.configure(relief=RAISED)
        return None
        
    command_play = 'play forward'
    button_forward.configure(relief=SUNKEN)
    button_backward.configure(relief=RAISED)

def action_play_backward () :
    global command_play
    if (command_play == 'play backward') :
        command_play = 'stop'
        button_backward.configure(relief=RAISED)
        return None
        
    command_play = 'play backward'
    button_backward.configure(relief=SUNKEN)
    button_forward.configure(relief=RAISED)
        
        
    
def action_play_next () :
    global play_pos
    play_pos += 1
    play_pos_to_ghost()

def action_play_prev () :
    global play_pos
    play_pos -= 1
    play_pos_to_ghost()
    
    
def action_play_reset () :
    global play_pos
    play_pos = 0
    play_pos_to_ghost()
            


def action_timeline_slider_moved(self):
    global play_pos
    percent = timeline_position.get()
    tmp = int( (percent*0.01)* len(data_posx) )
    if (tmp > (len(data_posx)-1)) : tmp = len(data_posx)-1
    play_pos = tmp

    play_pos_to_ghost()



def action_clear_data():
    global data_posx, data_posy, data_marker, play_pos    
    print('Clearing data...')
    data_posx = []
    data_posy = []
    data_marker = []
    play_pos = 0
    action_image_refresh()

def action_Record_Start():
    global flag_record, mode
    flag_record = True
    mode = 'record'
    action_image_refresh()


def mouseButton1(event):
    #if (flag_play == True) : return None

    if flag_record : action_Record_Stop()
    else : action_Record_Start()


def action_marker_set():
    global data_marker, last_marker, marker_number
    
    position = play_pos
        
    if ( (len(data_marker)>0) &
        (last_marker == position)
    ) :
        return None
        
    last_marker = position        
    data_marker.append(position)
    marker_number = len(data_marker)-1
    update_timeline()


#def mouseButton3(event):
    #right click


def update_info():
    global slider_timeline
    
    tmp_posx = int(mouse_posx/2)
    tmp_posy = int(mouse_posy/2)

    textvariable_mode.set('%s' % mode)

    textvariable_coords.set('x=%03d y=%03d | x=$%04x y=$%02x' % (
        tmp_posx, tmp_posy,
        tmp_posx, tmp_posy
    ))

    textvariable_pos.set('%05d/%05d $%04x/$%04x' % (
        play_pos, len(data_posx),
        play_pos, len(data_posx)
    ))

    textvariable_marker.set('%02d/%02d $%02x/$%02x' % (
        marker_number+1, len(data_marker),
        marker_number+1, len(data_marker)
    ))


def mouseMotion(event):
    global mouse_posx, mouse_posy, data_posx, data_posy, last_posx, last_posy, mousepointer_image
    global label_image
    
    label_image.config(cursor = MOUSEPOINTER_NORMAL)
    
#    if (mode == 'play') :
#        label_image.config(cursor = MOUSEPOINTER_NONE)
#        return None
    
    mouse_posx = event.x
    mouse_posy = event.y
    if (
        (last_posx == mouse_posx) &
        (last_posy == mouse_posy)
    ) :
        return None
        

    if (flag_record == True) :
        tmp_posx = int(mouse_posx/2)
        tmp_posy = int(mouse_posy/2)
        data_posx.append(tmp_posx)
        data_posy.append(tmp_posy & 0b11111111)


    action_image_refresh()



def create_gui_timeline (
	root,
    _row,
    _column
) :
    global label_timeline_image, slider_timeline
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
 
    label_timeline_image = Label(
        frame_border,
        bg=BGCOLOR,
#        cursor=MOUSEPOINTER_NONE
    )
    label_timeline_image.grid(
        row=0,
        column=0,
        sticky=W+E
    )
 
 
        
    slider_timeline = Scale(
        frame_border,
        bg=BGCOLOR_LIGHT,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        variable=timeline_position,
        length=IMAGE_VISIBLE_WIDTH,
        cursor=MOUSEPOINTER_HAND,
        showvalue=0,
        command=action_timeline_slider_moved
    )

    slider_timeline.grid(
        row=1,
        column=0,
        sticky=W+E
    )

    #set default value
    slider_timeline.set(0)



def create_gui_image (
	root,
    _row,
    _column
) :
    global label_image
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    label_image = Label(
        frame_border,
        bg=BGCOLOR,
        cursor=mousepointer_image
    )
    label_image.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    
    label_image.bind('<Motion>', mouseMotion)
    label_image.bind('<Button-1>', mouseButton1)
    #label_image.bind('<Button-3>', mouseButton3)


def create_gui_player_controls (
	root,
    _row,
    _column
) :
    global button_play, button_forward, button_backward

    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = FRAME_PADX,
        pady = FRAME_PADY,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
 
    
    MODES = [
            ('set marker', GFX_MARKER_SET, 0, 0,0, action_marker_set),
            ('previous marker', GFX_MARKER_PREV, 0, 0,1, action_marker_previous),
            ('go to marker', GFX_MARKER_GOTO, 0, 0,2, action_marker_goto),
            ('next marker', GFX_MARKER_NEXT, 0, 0,3, action_marker_next),
            ('delete marker', GFX_MARKER_DELETE, 0, 0,4, action_marker_delete),

            ('previous', GFX_PREVIOUS, 3, 1,0, action_play_prev),
            ('backward', GFX_BACKWARD, 0, 1,1, action_play_backward),
            ('stop', GFX_STOP, 0, 1,2, action_play_stop),
            ('forward', GFX_FORWARD, 0, 1,3, action_play_forward),
            ('next', GFX_NEXT, 0, 1,4, action_play_next),
            ('reset', GFX_RESET, 0, 1,5, action_play_reset),
    ]
    
    for text, my_image, my_underline, my_row, my_column, my_command in MODES:
        my_button = Button(
            frame_inner,
            bitmap='@'+my_image,
            bg = BGCOLOR_LIGHT,
            text = text,
            command = my_command,
            cursor = MOUSEPOINTER_HAND,
            underline = my_underline,
            relief=RAISED
        )
        if (text == 'forward') : button_forward = my_button
        if (text == 'backward') : button_backward = my_button
        #placement in grid layout
        my_button.grid(
            row= my_row,
            column= my_column,
            sticky=W
        )



def create_gui_infobox (
    root,
    my_row,
    my_column,
    my_text,
    my_textvariable,
    my_width
) :
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=1,
        padx = FRAME_PADX,
        pady = FRAME_PADY
        )

    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = FRAME_PADX,
        pady = FRAME_PADY,
        relief=RAISED
        )

    label_info = Label(
		frame_inner,
        bg=BGCOLOR2,
		text = my_text,
        bd=1
	)

    label_content = Label(
		frame_inner,
        bg=BGCOLOR_LIGHT,
		textvariable = my_textvariable,
        bd=1,
        width=my_width,
	)


    # layout
    frame_border.grid(
        row=my_row,
        column=my_column,
        sticky=W,
    )

    frame_inner.grid(
        row=0,
        column=0,
        sticky=W,
    )

    label_info.grid(
        row=0,
        column=0,
        sticky=W,
    )

    label_content.grid(
        row=0,
        column=1,
        sticky=W,
    )



def create_gui_main (
	root,
    _row,
    _column
) :    
    frame_border = Frame(
        root,
        bd=1,
        bg=BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W+E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)

    frame_left = Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky=W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)


    frame_right = Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    create_gui_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'mode:',    #text
        textvariable_mode,   #textvariable
        0   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        0,  #row
        0,  #column
        'coords:',    #text
        textvariable_coords,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_left,   #root frame
        1,  #row
        0,  #column
        'pos:',    #text
        textvariable_pos,   #textvariable
        25   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        1,  #row
        0,  #column
        'markers:',    #text
        textvariable_marker,   #textvariable
        0   #text width
    )


    create_gui_player_controls (
        frame_left,   #root frame
        2,  #row
        0  #column
    )

    create_gui_settings (
        frame_right,   #root frame
        2,  #row
        0  #column
    )


        


def create_gui_settings (
	root,
    _row,
    _column
) :
    global scale_settings_list, scale_settings_list_default

#scales modifiers
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = FRAME_PADX,
        pady = FRAME_PADY,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row=0
    label = Label(
        frame_inner,
        bg=BGCOLOR_LIGHT,
        text='settings',
        wraplength=100,
        anchor='c',
        justify='left',
        fg='#000088'
    )
    label.grid(
        row=_row,
        column=0,
        sticky=W
    )


    SETTINGS = [
        #text, variable, row, column, low, high
        ('player speed', player_speed, 1,0, 1,PLAYER_SPEED_MAX),
    ]

    for text, var, my_row, my_column, low, high in SETTINGS:
        scale_settings = Scale(
            frame_inner,
            bg=BGCOLOR_LIGHT,
            from_=low,
            to=high,
            orient=HORIZONTAL,
            variable=var,
            label=text,
            length=200,
            cursor=MOUSEPOINTER_HAND,
            showvalue=0,
            #command=action_preview_scale
        )
        scale_settings.grid(
            row=my_row,
            column=my_column,
            sticky='w'
        )
        #set default value
        scale_settings.set(high)
 
 

def action_delete_data_rest():
    global data_posx, data_posy, data_marker
    print('Deleting data from %d to the end.' %(play_pos))
    data_posx = data_posx[:play_pos+1]
    data_posy = data_posy[:play_pos+1]
    
    new_list = []
    for i in range(0,len(data_marker)) :
        if (data_marker[i] < len(data_posx)) :
            new_list.append(data_marker[i])
    
    data_marker = new_list
    
    update_timeline()
   
    

def action_marker_delete_rest():
    global data_marker
    print('Deleting marker from %d to the end.' %(marker_number))
    data_marker = data_marker[:marker_number+1]
    update_timeline()
    
    

def action_marker_next():
    global marker_number
    if (len(data_marker) > 0) :        
        if (marker_number < len(data_marker)-1) : marker_number += 1
        else : marker_number = 0
        jump_to_marker()
    
def action_marker_goto():
    if (len(data_marker) > 0) :        
        jump_to_marker()
    
def action_marker_previous():
    global marker_number
    if (len(data_marker) > 0) :        
        if (marker_number > 0) : marker_number -= 1
        else : marker_number = len(data_marker)-1
        jump_to_marker()




   
def action_Info (
) :
    message = \
        'main control\n' \
        '------------\n' \
        'Left-mousebutton: start/stop recording\n' \
        '<Alt-q>: quit\n' \
        '<Alt-i>: open image\n' \
        '<Alt-p>: open pointer-image\n' \
        '<Alt-g>: open ghost-image\n' \
        '<Alt-s>: save data\n' \
        '<Alt-r>: reload data\n' \
        '\n' \
        'player controls\n' \
        '---------------\n' \
        'r: reset\n' \
        'f: play forward\n' \
        '<space>: stop\n' \
        'b: play backward\n' \
        'n: play next step\n' \
        'v: play previous step\n' \
        '\n' \
        'marker controls\n' \
        '---------------\n' \
        'm: set marker\n' \
        'n: jump to next marker\n' \
        'p: jump to previous marker\n' \
        'g: go to current marker\n' \
    
    
    TEXT_HEIGHT=20
    TEXT_WIDTH=40

    def close_window():
        global info_window
        global info_window_open
        
        if (info_window_open == True) :
            info_window.destroy()
            info_window_open = False

    def close_window_key(self):
        close_window()

    def keyboard_up(event):
        msg.yview_scroll(-1,'units')

    def keyboard_down(event):
        msg.yview_scroll(1,'units')

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,'units')

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,'units')


    FRAME_PADX = 10
    FRAME_PADY = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = Toplevel(
        bd=10
    )
    info_window.title('Help')
    info_window.configure(background=BGCOLOR)

    frame_left = Frame( info_window)
    frame_right = Frame( info_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = Text(
        frame_right,
#        bd=10,
        relief=FLAT,
        width=TEXT_WIDTH,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = Scrollbar(
        frame_right,
        bg=BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(END, message)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=DISABLED)


    #button
    button = Button(
        frame_left,
        bg=BGCOLOR,
        text='OK',
        command=info_window.destroy,
        padx=FRAME_PADX,
        pady=FRAME_PADY
    )




    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky=W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky=W
    )
    button.grid(
        row=1,
        column=0,
        sticky=W+E
    )

    msg.grid(
        row=0,
        column=0,
        sticky=W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=N+S
    )

    info_window.bind('<Up>', keyboard_up) 
    info_window.bind('<Down>', keyboard_down) 
    info_window.bind('<Next>', keyboard_pageup) 
    info_window.bind('<Prior>', keyboard_pagedown) 




def _main_procedure() :
    global args

    print('%s v%s [%s] *** by fieserWolF' % (PROGNAME, VERSION, DATUM))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This records mouse movements and writes them to binary data files. Press F1 for help in the program.',
        epilog='Example: ./mousetrap.py -i image.png -p ball.png -g ghost.png -xl posx-low.bin -xh posx-high.bin -y posy.bin -ml marker_lo.bin -mh marker_hi.bin'
    )
    parser.add_argument('-i', '--image_file', dest='image_file', help='image file ('+str(IMAGE_WIDTH)+'x'+str(IMAGE_HEIGHT)+' pixel)')
    parser.add_argument('-p', '--pointer_file', dest='pointer_file', help='optional pointer image file ('+str(OBJ_WIDTH)+'x'+str(OBJ_HEIGHT)+' pixel): it follows the mousepointer')
    parser.add_argument('-g', '--ghost_file', dest='ghost_file', help='optional ghost pointer image file ('+str(GHOST_WIDTH)+'x'+str(GHOST_HEIGHT)+' pixel): it follows the recorded data')
    parser.add_argument('-xl', '--posx_lo_file', dest='posx_lo_file', help='posx low file (default="posx_lo.bin")', default='posx_lo.bin')
    parser.add_argument('-xh', '--posx_hi_file', dest='posx_hi_file', help='posx high file (default="posx_hi.bin")', default='posx_hi.bin')
    parser.add_argument('-y', '--posy_file', dest='posy_file', help='posy file (default="posy.bin")', default='posy.bin')
    parser.add_argument('-ml', '--marker_lo_file', dest='marker_lo_file', help='marker file (default="marker_lo.bin")', default='marker_lo.bin')
    parser.add_argument('-mh', '--marker_hi_file', dest='marker_hi_file', help='marker file (default="marker_hi.bin")', default='marker_hi.bin')
    args = parser.parse_args()

            
    #main procedure
    title_string = PROGNAME+' v'+VERSION+' ['+DATUM+'] *** by fieserWolF'
    root.title(title_string)
    create_gui_drop_down_menu(root)

    root.configure(
        background=BGCOLOR
    )
    create_gui_main(
        root,
        0,  #row
        0   #column
    )
    create_gui_timeline(
        root,
        1,  #row
        0   #column
    )
    create_gui_image(
        root,
        2,  #row
        0   #column
    )

           
    root.bind_all('<Alt-q>', lambda event: quit_application())
#    root.bind_all('<Alt-o>', lambda event: action_OpenFile_Data())
    root.bind_all('<Alt-i>', lambda event: action_OpenFile_Image())
    root.bind_all('<Alt-p>', lambda event: action_OpenFile_Pointer())
    root.bind_all('<Alt-g>', lambda event: action_OpenFile_Ghost())
    root.bind_all('<Alt-s>', lambda event: action_SaveData())
    root.bind_all('<Alt-r>', lambda event: load_data())
    root.bind_all('<F1>', lambda event: action_Info())
    root.bind_all('r', lambda event: action_play_reset())
    root.bind_all('f', lambda event: action_play_forward())
    root.bind_all('<space>', lambda event: action_play_stop())
    root.bind_all('b', lambda event: action_play_backward())
    root.bind_all('n', lambda event: action_play_next())
    root.bind_all('v', lambda event: action_play_prev())
    root.bind_all('m', lambda event: action_marker_set())
    root.bind_all('n', lambda event: action_marker_next())
    root.bind_all('p', lambda event: action_marker_previous())
    root.bind_all('g', lambda event: action_marker_goto())

    root.protocol('WM_DELETE_WINDOW', quit_application)

    root.after(10, play_thread)


    load_image_marker(GFX_TIMELINE_MARKER)
    load_image_cursor(GFX_TIMELINE_CURSOR)

    if (args.image_file) :
        load_image(args.image_file)

    if (args.pointer_file) :
        load_image_ball(args.pointer_file)

    if (args.ghost_file) :
        load_image_ghost(args.ghost_file)

    load_data()
    update_timeline()

    action_image_refresh()


    #https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    #t1 = threading.Thread(target = play_thread)
    #t1.start()

    mainloop()

    #t1.join()   #kill thread






if __name__ == '__main__':
    _main_procedure()
    
    
    
    
    
    

