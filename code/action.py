import code.myGlobals as myGlobals

import os
import struct
from PIL import ImageTk
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
from tkinter import RAISED, SUNKEN



def record_Stop():
    #writes flag_record, mode
    myGlobals.flag_record = False
    myGlobals.mode = 'idle'
    update_timeline()
    refresh_image()
    factor = len(myGlobals.data_posx)
    if (factor == 0) : factor = 1
    myGlobals.timeline_position.set( int(( myGlobals.play_pos / factor )*100) )


def play_stop () :
    #writes command_play
    myGlobals.command_play = 'stop'
    myGlobals.button_forward.configure(relief=RAISED)
    myGlobals.button_backward.configure(relief=RAISED)
    
def play_forward () :
    #writes command_play
    if (myGlobals.command_play == 'play forward') :
        myGlobals.command_play = 'stop'
        myGlobals.button_forward.configure(relief=RAISED)
        return None
        
    myGlobals.command_play = 'play forward'
    myGlobals.button_forward.configure(relief=SUNKEN)
    myGlobals.button_backward.configure(relief=RAISED)

def play_backward () :
    #writes command_play
    if (myGlobals.command_play == 'play backward') :
        myGlobals.command_play = 'stop'
        myGlobals.button_backward.configure(relief=RAISED)
        return None
        
    myGlobals.command_play = 'play backward'
    myGlobals.button_backward.configure(relief=SUNKEN)
    myGlobals.button_forward.configure(relief=RAISED)
        
        
    
def play_next () :
    #writes play_pos
    myGlobals.play_pos += 1
    play_pos_to_ghost()

def play_prev () :
    #writes play_pos
    myGlobals.play_pos -= 1
    play_pos_to_ghost()
    
    
def play_reset () :
    #writes play_pos
    myGlobals.play_pos = 0
    play_pos_to_ghost()
            


def timeline_slider_moved(self):
    #writes play_pos
    percent = myGlobals.timeline_position.get()
    tmp = int( (percent*0.01)* len(myGlobals.data_posx) )
    if (tmp > (len(myGlobals.data_posx)-1)) : tmp = len(myGlobals.data_posx)-1
    myGlobals.play_pos = tmp

    play_pos_to_ghost()



def clear_data():
    #writes data_posx, data_posy, data_marker, play_pos    
    print('Clearing data...')
    myGlobals.data_posx = []
    myGlobals.data_posy = []
    myGlobals.data_animation = []
    myGlobals.data_marker = []
    myGlobals.play_pos = 0
    refresh_image()

def record_Start():
    #writes flag_record, mode
    myGlobals.flag_record = True
    myGlobals.mode = 'record'
    refresh_image()



def marker_set():
    #writes data_marker, last_marker, marker_number
    
    position = myGlobals.play_pos
        
    if ( (len(myGlobals.data_marker)>0) &
        (myGlobals.last_marker == position)
    ) :
        return None
        
    myGlobals.last_marker = position        
    myGlobals.data_marker.append(position)
    myGlobals.marker_number = len(myGlobals.data_marker)-1
    update_timeline()


 

def delete_data_rest():
    #writes data_posx, data_posy, data_marker
    print('Deleting data from %d to the end.' %(myGlobals.play_pos))
    myGlobals.data_posx = myGlobals.data_posx[:myGlobals.play_pos+1]
    myGlobals.data_posy = myGlobals.data_posy[:myGlobals.play_pos+1]
    
    new_list = []
    for i in range(0,len(myGlobals.data_marker)) :
        if (myGlobals.data_marker[i] < len(myGlobals.data_posx)) :
            new_list.append(myGlobals.data_marker[i])
    
    myGlobals.data_marker = new_list
    
    update_timeline()
   
    

def marker_delete_rest():
    #writes data_marker
    print('Deleting marker from %d to the end.' %(myGlobals.marker_number))
    myGlobals.data_marker = myGlobals.data_marker[:myGlobals.marker_number+1]
    update_timeline()
    
    

def toggle_record_animation():
    if (myGlobals.command_record_animation == 'start') :
        #print('record animation stop')
        myGlobals.command_record_animation = 'stop'
        myGlobals.button_record_animation.configure(relief=RAISED)
        return None
        
    #print('record animation start')
    myGlobals.command_record_animation = 'start'
    myGlobals.button_record_animation.configure(relief=SUNKEN)


def marker_next():
    #writes marker_number
    if (len(myGlobals.data_marker) > 0) :        
        if (myGlobals.marker_number < len(myGlobals.data_marker)-1) : myGlobals.marker_number += 1
        else : myGlobals.marker_number = 0
        jump_to_marker()
    
def marker_goto():
    if (len(myGlobals.data_marker) > 0) :        
        jump_to_marker()
    
def marker_previous():
    #writes marker_number
    if (len(myGlobals.data_marker) > 0) :        
        if (myGlobals.marker_number > 0) : myGlobals.marker_number -= 1
        else : myGlobals.marker_number = len(myGlobals.data_marker)-1
        jump_to_marker()







def marker_clear_all():
    #writes data_marker
    print('Clearing markers...')
    myGlobals.data_marker = []
    update_timeline()
    refresh_image()

def marker_delete():
    #writes data_marker
    if (myGlobals.marker_number < len(myGlobals.data_marker)) :
        #print('Deleting marker %d...' % (int(myGlobals.marker_number+1)))
        del myGlobals.data_marker[myGlobals.marker_number]
        update_timeline()
        refresh_image()


#def OpenFile_Data():    
#    ftypes = [('Data Files', '*.bin')]
#    user_filename_open = askopenfilename(filetypes = ftypes)
#    if not user_filename_open : return None
#    load_data(user_filename_open)





def refresh_image():
    #image

    if (myGlobals.command_record_animation == 'start' ) :
        anim_image_number = myGlobals.anim_image_number.get() % myGlobals.anim_image_max
    else :
        anim_image_number = myGlobals.ghost_animation
    
    final_image = myGlobals.background_image.copy()    

    if (len(myGlobals.anim_image) > 0) :
        #final_image.paste(myGlobals.anim_image[anim_image_number], (myGlobals.ghost_posx, myGlobals.ghost_posy), myGlobals.anim_image[anim_image_number])
        final_image.paste(myGlobals.anim_image[anim_image_number], (myGlobals.ghost_posx, myGlobals.ghost_posy), myGlobals.anim_image[anim_image_number])
    else :
        final_image.paste(myGlobals.ghost_image, (myGlobals.ghost_posx, myGlobals.ghost_posy), myGlobals.ghost_image)

    final_image.paste(myGlobals.ball_image, (myGlobals.mouse_posx, myGlobals.mouse_posy), myGlobals.ball_image)

    myGlobals.image_background_Tk = ImageTk.PhotoImage(final_image)
    myGlobals.label_background_image.configure(image=myGlobals.image_background_Tk)
    myGlobals.label_background_image.image = final_image # keep a reference!
    

    #timeline
    factor = len(myGlobals.data_posx)
    if factor==0 : factor=1
    
    xpos = int ( (myGlobals.play_pos / factor) * myGlobals.TIMELINE_WIDTH)
    final_image = myGlobals.timeline_image.copy()
    #add cursor
    final_image.paste(myGlobals.cursor_timeline_image, (xpos, 0), myGlobals.cursor_timeline_image)
    myGlobals.image_timeline_Tk = ImageTk.PhotoImage(final_image)
    myGlobals.label_timeline_image.configure(image=myGlobals.image_timeline_Tk)
    myGlobals.label_timeline_image.image = final_image # keep a reference!

    # slider: animation of ghost-pointer
    if (myGlobals.command_record_animation == 'stop' ) :
        myGlobals.anim_image_number.set(myGlobals.ghost_animation)

    update_info()




def jump_to_marker():
    #writes play_pos, ghost_posx, ghost_posy
    myGlobals.play_pos = myGlobals.data_marker[myGlobals.marker_number]
    factor = len(myGlobals.data_posx)
    if (factor == 0) : factor = 1
    myGlobals.timeline_position.set( int(( myGlobals.play_pos / factor )*100) )

    myGlobals.ghost_posx = myGlobals.data_posx[myGlobals.play_pos]*2
    myGlobals.ghost_posy = myGlobals.data_posy[myGlobals.play_pos]*2

    if (myGlobals.mode == 'play') : refresh_image()
    else :  refresh_image()


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


def save_data():

    #posx low
    tmp = []
    for i in myGlobals.data_posx :
        tmp.append(i & 0b11111111)    
    save_some_data(myGlobals.args.posx_lo_file, tmp)

    #posx high
    tmp = []
    for i in myGlobals.data_posx :
        tmp.append(i >> 8)    
    save_some_data(myGlobals.args.posx_hi_file, tmp)

    #posy
    save_some_data(myGlobals.args.posy_file, myGlobals.data_posy)

    #animation
    save_some_data(myGlobals.args.anim_file, myGlobals.data_animation)

    #marker low
    tmp = []
    for i in myGlobals.data_marker :
        tmp.append(i & 0b11111111)    
    save_some_data(myGlobals.args.marker_lo_file, tmp)

    #marker high
    tmp = []
    for i in myGlobals.data_marker :
        tmp.append(i >> 8)    
    save_some_data(myGlobals.args.marker_hi_file, tmp)


def load_some_data (
    filename
) :
    buffer=[]

	#open input file
    print ('Opening file "%s" for reading...' % filename)
    try:
        file_in = open(filename , 'rb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return buffer

    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])

    return buffer




def load_data(
) :
    #writes data_posx, data_posy, data_marker, ghost_posx, ghost_posy, play_pos
    
    tmp_l = load_some_data(myGlobals.args.posx_lo_file)
    tmp_h = load_some_data(myGlobals.args.posx_hi_file)
    
    myGlobals.data_posx = []
    for i in range(len(tmp_l)) :
        myGlobals.data_posx.append(tmp_l[i] + (tmp_h[i] << 8))
    
    myGlobals.data_posy = load_some_data(myGlobals.args.posy_file)
    myGlobals.data_animation = load_some_data(myGlobals.args.anim_file)

    tmp_l = load_some_data(myGlobals.args.marker_lo_file)
    tmp_h = load_some_data(myGlobals.args.marker_hi_file)
    myGlobals.data_marker = []
    for i in range(len(tmp_l)) :
        myGlobals.data_marker.append(tmp_l[i] + (tmp_h[i] << 8))


    myGlobals.play_pos = 0
    myGlobals.timeline_position.set(0)

    if (len(myGlobals.data_posx)>0) :
        myGlobals.ghost_posx = myGlobals.data_posx[myGlobals.play_pos]*2
        myGlobals.ghost_posy = myGlobals.data_posy[myGlobals.play_pos]*2

    update_timeline()
    refresh_image()








def load_background_image(
	filename
):
    #writes background_image
    print('Opening background-image "%s"...' % filename)

    myGlobals.background_image = PilImage.open(filename)
    myGlobals.background_image = myGlobals.background_image.resize((myGlobals.IMAGE_VISIBLE_WIDTH, myGlobals.IMAGE_VISIBLE_HEIGHT))
    myGlobals.background_image = myGlobals.background_image.convert('RGB')




def load_image_anim(
	filename
):    
    print('Opening multi-layered animation-image "%s"...' % filename)

    my_image = PilImage.open(filename)
    if ( my_image.is_animated ) :
        print('%d frames found.' %my_image.n_frames)
        myGlobals.anim_image_max = my_image.n_frames
        
        myGlobals.anim_image = []
        for frame in range(0,my_image.n_frames):
            my_image.seek(frame)
            new_image = my_image.copy()
            new_image = new_image.resize((myGlobals.OBJ_WIDTH, myGlobals.OBJ_HEIGHT))
            new_image = new_image.convert("RGBA")
            myGlobals.anim_image.append(new_image)

        #myGlobals.anim_image[0].show()
        #myGlobals.anim_image[1].show()
        
    else :
        print('Error: No multiple layers found in image.')



def load_image_ball(
	filename
):
    #writes ball_image
    
    print('Opening ball-image "%s"...' % filename)

    myGlobals.ball_image = PilImage.open(filename)
    myGlobals.ball_image = myGlobals.ball_image.resize((myGlobals.OBJ_WIDTH, myGlobals.OBJ_HEIGHT))
    myGlobals.ball_image = myGlobals.ball_image.convert("RGBA")


def load_image_ghost(
	filename
):
    #writes ghost_image
    
    print('Opening ghost-image "%s"...' % filename)

    myGlobals.ghost_image = PilImage.open(filename)
    myGlobals.ghost_image = myGlobals.ghost_image.resize((myGlobals.GHOST_WIDTH, myGlobals.GHOST_HEIGHT))
    myGlobals.ghost_image = myGlobals.ghost_image.convert("RGBA")


def load_image_marker(
	filename
):
    #writes marker_single_image
    
    print('Opening marker-image "%s"...' % filename)

    myGlobals.marker_single_image = PilImage.open(filename)
    myGlobals.marker_single_image = myGlobals.marker_single_image.convert("RGBA")



def load_image_cursor(
	filename
):
    #writes cursor_timeline_image
    
    print('Opening cursor-image "%s"...' % filename)

    myGlobals.cursor_timeline_image = PilImage.open(filename)
    myGlobals.cursor_timeline_image = myGlobals.cursor_timeline_image.convert("RGBA")





def update_timeline():
    #writes timeline_image

    #new clear timeline
    myGlobals.timeline_image = PilImage.new('RGBA', (myGlobals.TIMELINE_WIDTH, myGlobals.TIMELINE_HEIGHT), 'black')

    #add markers
    for i in range(0,len(myGlobals.data_marker)) :
        xpos = int ( (myGlobals.data_marker[i] / len(myGlobals.data_posx)) * myGlobals.TIMELINE_WIDTH)
        myGlobals.timeline_image.paste(myGlobals.marker_single_image, (xpos,0), myGlobals.marker_single_image)

    refresh_image()




#keyboard shortcuts

    







        
def play_pos_to_ghost() :
    #writes play_pos, ghost_posx, ghost_posy

    #sanity checks
    if (myGlobals.play_pos < 0) : myGlobals.play_pos = len(myGlobals.data_posx)-1
    if (myGlobals.play_pos > len(myGlobals.data_posx)-1) : myGlobals.play_pos = 0

    if (myGlobals.command_record_animation == 'start') :
        myGlobals.data_animation[myGlobals.play_pos] = myGlobals.anim_image_number.get() % myGlobals.anim_image_max

    factor = len(myGlobals.data_posx)
    if (factor == 0) : factor = 1
    
    if (len(myGlobals.data_posx)>0) :
        myGlobals.ghost_posx = myGlobals.data_posx[myGlobals.play_pos]*2
        myGlobals.ghost_posy = myGlobals.data_posy[myGlobals.play_pos]*2
        myGlobals.ghost_animation = myGlobals.data_animation[myGlobals.play_pos]
        myGlobals.timeline_position.set( int(( myGlobals.play_pos / factor )*100) )
    refresh_image()
#    root.update()


def mouseButton1(event):
    #if (flag_play == True) : return None

    if myGlobals.flag_record : record_Stop()
    else : record_Start()


#def mouseButton3(event):
    #right click


def update_info():
    #writes slider_timeline
    
    tmp_posx = int(myGlobals.mouse_posx/2)
    tmp_posy = int(myGlobals.mouse_posy/2)

    myGlobals.textvariable_mode.set('%s' % myGlobals.mode)

    myGlobals.textvariable_coords.set('x=%03d y=%03d | x=$%04x y=$%02x' % (
        tmp_posx, tmp_posy,
        tmp_posx, tmp_posy
    ))

    myGlobals.textvariable_pos.set('%05d/%05d $%04x/$%04x' % (
        myGlobals.play_pos, len(myGlobals.data_posx),
        myGlobals.play_pos, len(myGlobals.data_posx)
    ))

    myGlobals.textvariable_marker.set('%02d/%02d $%02x/$%02x' % (
        myGlobals.marker_number+1, len(myGlobals.data_marker),
        myGlobals.marker_number+1, len(myGlobals.data_marker)
    ))


def mouseMotion(event):
    #writes mouse_posx, mouse_posy, data_posx, data_posy, last_posx, last_posy, mousepointer_image
    #writes label_background_image
    
    myGlobals.label_background_image.config(cursor = myGlobals.MOUSEPOINTER_NORMAL)
    
#    if (mode == 'play') :
#        label_background_image.config(cursor = MOUSEPOINTER_NONE)
#        return None
    
    myGlobals.mouse_posx = event.x
    myGlobals.mouse_posy = event.y
    if (
        (myGlobals.last_posx == myGlobals.mouse_posx) &
        (myGlobals.last_posy == myGlobals.mouse_posy)
    ) :
        return None
        

    if (myGlobals.flag_record == True) :
        tmp_posx = int(myGlobals.mouse_posx/2)
        tmp_posy = int(myGlobals.mouse_posy/2)
        myGlobals.data_posx.append(tmp_posx)
        myGlobals.data_posy.append(tmp_posy & 0b11111111)
        myGlobals.data_animation.append(0)


    refresh_image()

