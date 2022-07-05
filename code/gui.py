import code.myGlobals as myGlobals
import code.action as action
import code.gui_info as gui_info

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename



def OpenFile_Image():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    action.load_background_image(user_filename_open)

def OpenFile_Pointer():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    action.load_image_ball(user_filename_open)

def OpenFile_Ghost():    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    action.load_image_ghost(user_filename_open)

def OpenFile_Animation():    
    ftypes = [('Image Files', '*.webp')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    action.load_image_anim(user_filename_open)


def quit_application():
    global command_play
    command_play = 'exit'
    #root.quit()    
    if messagebox.askokcancel("Quit", "Do you want to quit?"): myGlobals.root.quit()    #root.destroy()


def create_drop_down_menu (
	root
) :
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    datamenu = Menu(menu)
    infomenu = Menu(menu)

#    filemenu.add_command(label="open data", command=OpenFile_Data, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="open image", command=OpenFile_Image, underline=5, accelerator="Alt+I")
    filemenu.add_command(label="open pointer", command=OpenFile_Pointer, underline=5, accelerator="Alt+P")
    filemenu.add_command(label="open ghost", command=OpenFile_Ghost, underline=5, accelerator="Alt+G")
    filemenu.add_command(label="open animation", command=OpenFile_Animation, underline=5, accelerator="Alt+A")
    filemenu.add_command(label="save data", command=action.save_data, underline=0, accelerator="Alt+S")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=quit_application, underline=0, accelerator="Alt+Q")

    datamenu.add_command(label="reload data", command=action.load_data, underline=0, accelerator="Alt-R")
    datamenu.add_separator()
    datamenu.add_command(label="clear rest of data", command=action.delete_data_rest)
    datamenu.add_command(label="clear rest of markers", command=action.marker_delete_rest)
    datamenu.add_command(label="clear all data", command=action.clear_data)
    datamenu.add_command(label="clear all markers", command=action.marker_clear_all)
    datamenu.add_command(label="jump to next marker", command=action.marker_next, underline=8, accelerator="n")
    datamenu.add_command(label="jump to previous marker", command=action.marker_previous, underline=8, accelerator="p")

    infomenu.add_command(label="help", command=gui_info.show_info_window, underline=0, accelerator="f1")

    #add all menus
    menu.add_cascade(label="file", menu=filemenu)
    menu.add_cascade(label="data", menu=datamenu)
    menu.add_cascade(label="info", menu=infomenu)





def create_timeline (
	root,
    _row,
    _column
) :
    #writes label_timeline_image, slider_timeline
    
    frame_border = Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
 
    myGlobals.label_timeline_image = Label(
        frame_border,
        bg=myGlobals.BGCOLOR,
#        cursor=myGlobals.MOUSEPOINTER_NONE
    )
    myGlobals.label_timeline_image.grid(
        row=0,
        column=0,
        sticky=W+E
    )
 
 
        
    myGlobals.slider_timeline = Scale(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        variable=myGlobals.timeline_position,
        length=myGlobals.IMAGE_VISIBLE_WIDTH,
        cursor=myGlobals.MOUSEPOINTER_HAND,
        showvalue=0,
        command=action.timeline_slider_moved
    )

    myGlobals.slider_timeline.grid(
        row=1,
        column=0,
        sticky=W+E
    )

    #set default value
    myGlobals.slider_timeline.set(0)



def create_image (
	root,
    _row,
    _column
) :
    #writes label_background_image
    
    frame_border = Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    myGlobals.label_background_image = Label(
        frame_border,
        bg=myGlobals.BGCOLOR,
        cursor=myGlobals.mousepointer_image
    )
    myGlobals.label_background_image.grid(
        row=0,
        column=0,
        sticky=W+E
    )
    
    myGlobals.label_background_image.bind('<Motion>', action.mouseMotion)
    myGlobals.label_background_image.bind('<Button-1>', action.mouseButton1)
    #myGlobals.label_background_image.bind('<Button-3>', mouseButton3)




def create_player_controls (
	root,
    _row,
    _column
) :
    #writes button_play, button_forward, button_backward

    frame_border = Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W
    )
    frame_inner = Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals.FRAME_PADX,
        pady = myGlobals.FRAME_PADY,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
 
    
    MODES = [
            ('set marker', myGlobals.GFX_MARKER_SET, 0, 0,0, action.marker_set),
            ('previous marker', myGlobals.GFX_MARKER_PREV, 0, 0,1, action.marker_previous),
            ('go to marker', myGlobals.GFX_MARKER_GOTO, 0, 0,2, action.marker_goto),
            ('next marker', myGlobals.GFX_MARKER_NEXT, 0, 0,3, action.marker_next),
            ('delete marker', myGlobals.GFX_MARKER_DELETE, 0, 0,4, action.marker_delete),
            ('record look', myGlobals.GFX_RECORD_LOOK, 0, 0,5, action.record_look),

            ('previous', myGlobals.GFX_PREVIOUS, 3, 1,0, action.play_prev),
            ('backward', myGlobals.GFX_BACKWARD, 0, 1,1, action.play_backward),
            ('stop', myGlobals.GFX_STOP, 0, 1,2, action.play_stop),
            ('forward', myGlobals.GFX_FORWARD, 0, 1,3, action.play_forward),
            ('next', myGlobals.GFX_NEXT, 0, 1,4, action.play_next),
            ('reset', myGlobals.GFX_RESET, 0, 1,5, action.play_reset),
    ]
    
    for text, my_image, my_underline, my_row, my_column, my_command in MODES:
        my_button = Button(
            frame_inner,
            bitmap='@'+my_image,
            bg = myGlobals.BGCOLOR_LIGHT,
            text = text,
            command = my_command,
            cursor = myGlobals.MOUSEPOINTER_HAND,
            underline = my_underline,
            relief=RAISED
        )
        if (text == 'forward') : myGlobals.button_forward = my_button
        if (text == 'backward') : myGlobals.button_backward = my_button
        if (text == 'record look') : myGlobals.button_record_look = my_button
        #placement in grid layout
        my_button.grid(
            row= my_row,
            column= my_column,
            sticky=W
        )



def create_infobox (
    root,
    my_row,
    my_column,
    my_text,
    my_textvariable,
    my_width
) :
    frame_border = Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals.FRAME_PADX,
        pady = myGlobals.FRAME_PADY
        )

    frame_inner = Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals.FRAME_PADX,
        pady = myGlobals.FRAME_PADY,
        relief=RAISED
        )

    label_info = Label(
		frame_inner,
        bg=myGlobals.BGCOLOR2,
		text = my_text,
        bd=1
	)

    label_content = Label(
		frame_inner,
        bg=myGlobals.BGCOLOR_LIGHT,
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



def create_main (
        root,
        _row,
        _column
) :    
    frame_border = Frame(
        root,
        bd=1,
        bg=myGlobals.BGCOLOR,
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
        bg=myGlobals.BGCOLOR,
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
        bg=myGlobals.BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    create_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'mode:',    #text
        myGlobals.textvariable_mode,   #textvariable
        0   #text width
    )

    create_infobox (
        frame_right,   #root frame
        0,  #row
        0,  #column
        'coords:',    #text
        myGlobals.textvariable_coords,   #textvariable
        30   #text width
    )




    create_infobox (
        frame_left,   #root frame
        1,  #row
        0,  #column
        'pos:',    #text
        myGlobals.textvariable_pos,   #textvariable
        25   #text width
    )

    create_infobox (
        frame_right,   #root frame
        1,  #row
        0,  #column
        'markers:',    #text
        myGlobals.textvariable_marker,   #textvariable
        0   #text width
    )


    create_player_controls (
        frame_left,   #root frame
        2,  #row
        0  #column
    )

    create_settings (
        frame_right,   #root frame
        2,  #row
        0  #column
    )


        


def create_settings (
	root,
    _row,
    _column
) :
    #writes scale_settings_list, scale_settings_list_default

#scales modifiers
    frame_border = Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W
    )
    frame_inner = Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals.FRAME_PADX,
        pady = myGlobals.FRAME_PADY,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row=0
    label = Label(
        frame_inner,
        bg=myGlobals.BGCOLOR_LIGHT,
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
        ('player speed', myGlobals.player_speed, 1,0, 1,myGlobals.PLAYER_SPEED_MAX),
        ('animation', myGlobals.anim_image_number, 2,0, 0,myGlobals.anim_image_max),
    ]

    for text, var, my_row, my_column, low, high in SETTINGS:
        scale_settings = Scale(
            frame_inner,
            bg=myGlobals.BGCOLOR_LIGHT,
            from_=low,
            to=high,
            orient=HORIZONTAL,
            variable=var,
            label=text,
            length=200,
            cursor=myGlobals.MOUSEPOINTER_HAND,
            showvalue=0,
            #command=action.action_preview_scale
            command=lambda event: action.refresh_image()
        )
        scale_settings.grid(
            row=my_row,
            column=my_column,
            sticky='w'
        )
        #set default value
        scale_settings.set(high)
