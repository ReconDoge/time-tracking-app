
'''an app that tracks how much time you are spending on a task. Each task is presented as a selectable button. When pressed, the timer begins'''

from win32api import GetSystemMetrics

import threading
import time

from datetime import timedelta

try:
    import dearpygui.dearpygui as dpg
except ImportError:
    import pip
    if hasattr(pip, 'main'):
        pip.main(['install', "dearpygui"])
    else:
        pip._internal.main(['install', "dearpygui"])
    try:
        import dearpygui.dearpygui as dpg
    except:
        raise ImportError

import timerAppController

#list of things you wanna keep track of time for
schedule_items = ["Item A", "Item B", "Item C"]


#simple class that does loops to increment numbers every 1 second
#all of the non widget related stuff probably belongs in timerAppController.py instead of here
class Timer:
    def __init__(self):
        self.count = 0          #keeps track of the total number of seconds that has elapsed
        self.running = False
        self.item_being_timed = None

    def tick(self):

        while self.running:
            self.count += 1

            count_formatted = str(timedelta(seconds=self.count))        #converts total seconds into hour:minute:second format

            dpg.set_value(item=1, value=count_formatted)

            time.sleep(1)


timer = Timer()

task_and_time = {item: 0 for item in schedule_items}



def get_previous_task_time(task, time):
    global task_and_time
    
    for item in schedule_items:
        if task == item:
            if time != 0:
                task_and_time[item] = task_and_time[item] + time
                print(task_and_time)


def start_timer_loop(sender=None, app_data=None, user_data=None):
    
    get_previous_task_time(timer.item_being_timed, timer.count)

    df = timerAppController.convert_into_df(task_and_time)
    timerAppController.save_df(df)

    timer.item_being_timed = user_data
    
    timer.running = True

    if sender is not None:          #checks if the call came from a button input or a script call. If it doesn't have a sender, it's not from a  button
        timer.count = 0

    for i in range(4, len(schedule_items)+4):       #ensures that only one selectable is selected
        if i != sender and sender is not None:
            dpg.set_value(i, False)
    
    thread1 = threading.Thread(target=timer.tick)   #uses the threading module to create a separate thread for the timer loop so the main app can still work without waiting for the loop to finish
    thread1.daemon = True
    
    if threading.active_count() <= 3:               #ensures that new threads aren't created every time the buttons are pressed if there is already a timing thread
        thread1.start()

    print("Active threads:", threading.enumerate())


def pause_timer_loop(sender, app_data, user_data):

    if timer.running:
        timer.running = False
    else:
        start_timer_loop()


def configure_viewport(sender, app_data, user_data):

    vp_width, vp_height = 250, 300
    
    mouse_pos = dpg.get_mouse_pos()

    #remember to make it so that relative coordinates are used instead of absolute 
    if mouse_pos[0] < vp_width and mouse_pos[0] > 0:
        if mouse_pos[1] < vp_height and mouse_pos[1] > 0:
            dpg.set_viewport_pos([1117, 120])
    else:
        dpg.set_viewport_pos([1320, 120])


with dpg.font_registry():
    heading_font = dpg.add_font(r"timerapp\Roboto-Bold.ttf",25)       #adds a font from a font file that looks nicer than the default one


#this is the root window
with dpg.window(width=250, height=300, autosize=False,pos=[0,0],
                no_resize=True, no_move=True, no_title_bar=True):

    #draw menu bar background
    dpg.draw_line((0, 1), (0, 285), color=(5, 64, 136, 255), thickness=60)
    
    dpg.add_separator()
    dpg.add_spacing(count=10)

    #a parent table for all the main widgets
    with dpg.table(header_row=False, pos=[45,10], borders_outerV=True,
                   borders_outerH=True):
        dpg.add_table_column(init_width_or_weight=10)
        dpg.add_spacing(count=3)
        dpg.add_text("0:00:00", id=1)     #timer text label
        dpg.add_same_line()
        with dpg.table(header_row=False, pos=[170,10]):     #two buttons next to timer
            
            dpg.add_table_column()
            dpg.add_spacing(count=3)
            dpg.add_button(label="Pause", id=2, width=50, height=20, callback=pause_timer_loop)
            dpg.add_button(label="Reset", id=3, width=50, height=20)
        dpg.add_same_line()
        dpg.set_item_font(item=1,font=heading_font)
        dpg.add_spacing(count=3)
        dpg.add_separator()
        dpg.add_spacing(count=3)

        for count, item in enumerate(schedule_items, start=4):              #loops through the schedule_items list and makes them all into selectable widgets
            dpg.add_selectable(id=count, label=item, callback=start_timer_loop, user_data=item)

    with dpg.handler_registry():
        dpg.add_mouse_move_handler(callback=configure_viewport)


if __name__ == "__main__":

    vp = dpg.create_viewport()

    dpg.set_viewport_pos([1110, 120])

    #create a viewport (the system window) and disables resizing and the default windows title bar, which looks ugly
    dpg.set_viewport_decorated(False)
    dpg.set_viewport_resizable(False)

    dpg.set_viewport_width(250)
    dpg.set_viewport_height(300)

    dpg.setup_dearpygui(viewport=vp)
    dpg.show_viewport(vp)

    dpg.start_dearpygui() 
