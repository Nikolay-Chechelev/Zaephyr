import thread
from Display import Screen

s = Screen()   # creating Screen Object
def new_data(*args):  # procedure of infinitive data loading
    while 1:
        s.load_data()

s.main_screen()  # Drawing main Sreen
thread.start_new(new_data, (None,))  # Start data loading
s.loop() # main cycle



