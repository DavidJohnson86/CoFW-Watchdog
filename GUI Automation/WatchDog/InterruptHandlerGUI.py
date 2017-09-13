'''
Created on 2017. szept. 7.

@author: SzuroveczD
'''
import tkinter as tk
import pyautogui as ag
import WatchDog
from queue import Empty
import os
import Starter
from time import sleep
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


class GUI():

    def __init__(self):
        self.GUI = tk.Tk()
        self.GUI.bind('<KeyPress>', self.onKeyPress)
        self.display_text = tk.Text(self.GUI, background='white', foreground='black',
                                    font=('Comic Sans MS', 12))
        self.display_text.pack()
        self.GUI.after(1000, self.Write_Console)
        self.GUI.mainloop()

    def onKeyPress(self, event):
        if (event.keysym) == 'Escape':
            try:
                ag.moveTo(0, 0)
            except ag.FailSafeException:
                GUI.failSafeHandler()

    @staticmethod
    def failSafeHandler():
        os._exit(0)

    def Write_Console(self):
        '''This function is refreshing the Console every 1 sec if any new message available'''
        try:
            data = WatchDog.Sentinel.FreezeDetect.console_message.get(False)
            #-- If `False`, the program is not blocked. `Queue.Empty` is thrown if
            #-- the queue is empty
        except Empty:
            data = None
        if data:
            self.display_text.insert(
                'end',
                chars=data +
                '\n')
        self.GUI.after(1000, self.Write_Console)
