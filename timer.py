from threading import Thread
import time
import datetime
from graphics import *

class ChessTimer(Thread):
    def __init__(self,max_time):
        Thread.__init__(self)
        self.game_over = False
        self.alive = False
        self.current_time = max_time

    def run(self):
        while(not self.game_over):
            print(self.time_to_string_representation())
            if(self.current_time == 0):
                self.timeout()
            time.sleep(1)
            if self.alive:
                self.current_time -= 1

    def time_to_string_representation(self):
        result = ""
        minutes = (int)(self.current_time/60)
        if(minutes < 10):
            result += "0"
        result += str(minutes)
        result += ":"
        sec = (int)(self.current_time%60)
        if(sec < 10):
            result += "0"
        result += str(sec)
        return result

    def timeout(self):
        print("Time is up.")
        self.game_over = True

    def start_timer(self):
        self.alive = True
        self.start()

    def stop_timer(self):
        self.alive = False

    def continue_timer(self):
        self.alive = True

    def is_timer_up(self):
        return self.game_over

mytimer = ChessTimer(10)
mytimer.start_timer()