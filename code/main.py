import code.myGlobals as myGlobals
import code.gui as gui
import code.action as action
import code.gui_info as gui_info

from tkinter import *
import argparse




def play_thread():
    if (myGlobals.command_play == 'play forward'): action.play_next()
    if (myGlobals.command_play == 'play backward'): action.play_prev()
    myGlobals.root.after(myGlobals.PLAYER_SPEED_MAX+1-int(myGlobals.player_speed.get()), play_thread)






def _main_procedure() :
    #writes args
    
    print('%s v%s [%s] *** by fieserWolF' % (myGlobals.PROGNAME, myGlobals.VERSION, myGlobals.LAST_EDITED))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This records mouse movements and writes them to binary data files. Press F1 for help in the program.',
        epilog='Example: ./mousetrap.py -b image.png -p ball.png -g ghost.png -xl posx-low.bin -xh posx-high.bin -y posy.bin -ml marker_lo.bin -mh marker_hi.bin'
    )
    parser.add_argument('-b', '--background_file', dest='background_file', help='background image file ('+str(myGlobals.IMAGE_WIDTH)+'x'+str(myGlobals.IMAGE_HEIGHT)+' pixel)')
    parser.add_argument('-p', '--pointer_file', dest='pointer_file', help='optional pointer image file ('+str(myGlobals.OBJ_WIDTH)+'x'+str(myGlobals.OBJ_HEIGHT)+' pixel): it follows the mousepointer')
    parser.add_argument('-g', '--ghost_file', dest='ghost_file', help='optional ghost pointer image file ('+str(myGlobals.GHOST_WIDTH)+'x'+str(myGlobals.GHOST_HEIGHT)+' pixel): it follows the recorded data')
    parser.add_argument('-xl', '--posx_lo_file', dest='posx_lo_file', help='posx low file (default="posx_lo.bin")', default='posx_lo.bin')
    parser.add_argument('-xh', '--posx_hi_file', dest='posx_hi_file', help='posx high file (default="posx_hi.bin")', default='posx_hi.bin')
    parser.add_argument('-y', '--posy_file', dest='posy_file', help='posy file (default="posy.bin")', default='posy.bin')
    parser.add_argument('-ml', '--marker_lo_file', dest='marker_lo_file', help='marker file (default="marker_lo.bin")', default='marker_lo.bin')
    parser.add_argument('-mh', '--marker_hi_file', dest='marker_hi_file', help='marker file (default="marker_hi.bin")', default='marker_hi.bin')
    myGlobals.args = parser.parse_args()
 
    #main procedure
    title_string = myGlobals.PROGNAME+' v'+myGlobals.VERSION+' ['+myGlobals.LAST_EDITED+'] *** by fieserWolF'
    myGlobals.root.title(title_string)
    gui.create_drop_down_menu(myGlobals.root)

    myGlobals.root.configure(
        background=myGlobals.BGCOLOR
    )
    gui.create_main(
        myGlobals.root,
        0,  #row
        0   #column
    )
    
    gui.create_timeline(
        myGlobals.root,
        1,  #row
        0   #column
    )
    gui.create_image(
        myGlobals.root,
        2,  #row
        0   #column
    )

           
    myGlobals.root.bind_all('<Alt-q>', lambda event: gui.quit_application())
#    root.bind_all('<Alt-o>', lambda event: gui.OpenFile_Data())
    myGlobals.root.bind_all('<Alt-i>', lambda event: gui.OpenFile_Image())
    myGlobals.root.bind_all('<Alt-p>', lambda event: gui.OpenFile_Pointer())
    myGlobals.root.bind_all('<Alt-g>', lambda event: gui.OpenFile_Ghost())
    myGlobals.root.bind_all('<Alt-s>', lambda event: action.save_data())
    myGlobals.root.bind_all('<Alt-r>', lambda event: action.load_data())
    myGlobals.root.bind_all('<F1>', lambda event: gui_info.show_info_window())
    myGlobals.root.bind_all('r', lambda event: action.play_reset())
    myGlobals.root.bind_all('f', lambda event: action.play_forward())
    myGlobals.root.bind_all('<space>', lambda event: action.play_stop())
    myGlobals.root.bind_all('b', lambda event: action.play_backward())
    myGlobals.root.bind_all('n', lambda event: action.play_next())
    myGlobals.root.bind_all('v', lambda event: action.play_prev())
    myGlobals.root.bind_all('m', lambda event: action.marker_set())
    myGlobals.root.bind_all('n', lambda event: action.marker_next())
    myGlobals.root.bind_all('p', lambda event: action.marker_previous())
    myGlobals.root.bind_all('g', lambda event: action.marker_goto())

    myGlobals.root.protocol('WM_DELETE_WINDOW', gui.quit_application)
    myGlobals.root.after(10, play_thread)

    action.load_image_marker(myGlobals.GFX_TIMELINE_MARKER)
    action.load_image_cursor(myGlobals.GFX_TIMELINE_CURSOR)

    if (myGlobals.args.background_file) :
        action.load_background_image(myGlobals.args.background_file)

    if (myGlobals.args.pointer_file) :
        action.load_image_ball(myGlobals.args.pointer_file)

    if (myGlobals.args.ghost_file) :
        action.load_image_ghost(myGlobals.args.ghost_file)

    action.load_data()
    action.update_timeline()
    action.refresh_image()


    #https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    #t1 = threading.Thread(target = play_thread)
    #t1.start()

    mainloop()

    #t1.join()   #kill thread
