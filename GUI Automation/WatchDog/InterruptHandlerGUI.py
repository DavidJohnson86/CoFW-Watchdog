'''
Created on 2017. szept. 7.

@author: SzuroveczD
'''
from threading import Thread
import tkinter as tk
import pyautogui as ag
import WatchDog


class GUI():

    def __init__(self):
        self.console_thread = Thread(target=self.IO_Interrupt, name='console')
        self.console_thread.start()

    def onKeyPress(self, event):
        if (event.keysym) == 'Escape':
            ag.moveTo(0, 0)

    def IO_Interrupt(self):
        self.GUI = tk.Tk()
        self.GUI.bind('<KeyPress>', self.onKeyPress)
        self.display_text = tk.Text(
            self.GUI,
            background='white',
            foreground='black',
            font=(
                'Comic Sans MS',
                12))
        self.display_text.pack()
        self.GUI.after(1000, self.Write_Console)
        self.GUI.mainloop()

    def Write_Console(self):
        self.display_text.insert(
            'end',
            chars=WatchDog.Sentinel.FreezeDetect.console_message.get() +
            '\n')
        self.GUI.after(1000, self.Write_Console)
