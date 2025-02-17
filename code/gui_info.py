import code.myGlobals as myGlobals
from tkinter import *


def show_info_window (
) :
    message = \
        'main control\n' \
        '------------\n' \
        'Left-mousebutton: start/stop recording\n' \
        '<Alt-q>: quit\n' \
        '<Alt-i>: open image\n' \
        '<Alt-p>: open pointer-image\n' \
        '<Alt-g>: open ghost-image\n' \
        '<Alt-a>: open animation-image\n' \
        '<Alt-s>: save data\n' \
        '<Alt-r>: reload data\n' \
        '\n' \
        'player controls\n' \
        '---------------\n' \
        '<Pos1>: go to start\n' \
        '<End>: go to end\n' \
        '<Up>: play forward\n' \
        '<space>: stop playback\n' \
        '<return>: toggle record movement\n' \
        '<Down>: play backward\n' \
        '<Right>: play next step\n' \
        '<Left>: play previous step\n' \
        '\n' \
        'animation controls\n' \
        '---------------\n' \
        'a: toggle record animation on/off\n' \
        'c: next animation step\n' \
        'x: previous animation step\n' \
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


    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = Toplevel(
        bd=10
    )
    info_window.title('Help')
    info_window.configure(background=myGlobals.BGCOLOR)

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
        bg=myGlobals.BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(END, message)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=DISABLED)

    FRAME_PADX = 10
    FRAME_PADY = 10

    #button
    button = Button(
        frame_left,
        bg=myGlobals.BGCOLOR,
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


