'''
Created on 2017. szept. 7.

@author: SzuroveczD
'''
import tkinter as tk
import pyautogui as ag
import os
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


class GUI():

    def __init__(self):
        self.GUI = tk.Tk()
        self.GUI.geometry("600x200+200+200")
        self.scrollbar = tk.Scrollbar(self.GUI)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.GUI.minsize(50, 50)
        self.GUI.bind('<KeyPress>', self.onKeyPress)
        self.display_text = tk.Text(self.GUI, background='white', foreground='black',
                                    font=('Comic Sans MS', 12), yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.display_text.yview)
        self.GUI.title('CoFW WatchDog')
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
            data = Transfer_Msg.CONSOLE_MESSAGE.get(False)
            #-- If `False`, the program is not blocked. `Queue.Empty` is thrown if
            #-- the queue is empty
        except Empty:
            data = None
        if data:
            self.display_text.insert('end', chars=data + '\n')
            self.display_text.see(tk.END)
        self.GUI.after(1000, self.Write_Console)


class Transfer_Msg():
    CONSOLE_MESSAGE = Queue()


if __name__ == '__main__':
    Transfer_Msg.CONSOLE_MESSAGE.put(
        "----------------------------------------------------------------------------------")
    Transfer_Msg.CONSOLE_MESSAGE.put("  Compa Framework WathcDog is not an offical tool.")
    Transfer_Msg.CONSOLE_MESSAGE.put("  It helps to execute tests automatically after CoFW crashes")
    Transfer_Msg.CONSOLE_MESSAGE.put("  To Close Click On GUI Window and Press Escape")
    Transfer_Msg.CONSOLE_MESSAGE.put(
        "--------------------------------------------------------------------")
    GUI()
