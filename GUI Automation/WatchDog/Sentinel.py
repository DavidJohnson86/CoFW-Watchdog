
# -*- coding: utf-8 -*-

import sys
import os
from time import sleep
import subprocess
from time import gmtime, strftime
from threading import Thread, Timer
from Automater import Automating_System
from FileHandler import FileHandler, Parser
from Starter import Configurator

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
try:
    import cv2
except ImportError:
    print ('Cv2 not installed')
try:
    import numpy as np
except ImportError:
    print ('Numpy Is not installed.')
try:
    import pyautogui as ag
except ImportError:
    print ('PyautoGUI is not installed')


ON_POSIX = 'posix' in sys.builtin_module_names


class FreezeDetect(Configurator):

    def __init__(self, program, file_loc, MAX_WAIT_TIME):
        Configurator.__init__(self)
        self.program = program
        self.file_loc = file_loc
        self.MAX_WAIT_TIME = MAX_WAIT_TIME

    def is_it_running(self, program_name):
        '''This Function is check if the Current Process Exist in the Task Manager.'''
        n = 0  # number of instances of the program running
        prog = [line.split() for line in subprocess.check_output("tasklist").splitlines()]
        [prog.pop(e) for e in [0, 1, 2]]  # useless
        for task in prog:
            if task[0] == bytes(program_name, encoding='utf-8'):
                n = n + 1
        if n > 0:
            return True
        else:
            return False

    def is_it_freezed(self, pattern, treshold=0.8):
        '''This Function is Detecting if the Compa Framewok stopped working window pops up. '''
        obj = Automating_System.MouseHandler()
        obj.takeScreenShot()
        '''FIX THIS PART
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        image = cv2.imread(r"d:\Development\GUI Automation\Automater\tmp\screenshot.jpg", 0)
        pattern = cv2.imread(r"d:\Development\GUI Automation\Automater\patterns\Freezed.jpg", 0)
        res = cv2.matchTemplate(image, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= treshold)
        loc = list(zip(*loc[::-1]))
        if(len(loc) >= 1):
            return True
        else:
            return False

    def watchdogTimer(self):
        '''We have to montor 2 events: 1. the program running & 2. the program freezed.
        If the program not running its necessary to open it. Anyway opening the program
        will halt the program flow so this should be done on other thread.

        Timer is responsible to run the watchdogTimer Function in every x seconds
        where x == self.MAX_WAIT_TIME.'''
        if (self.is_it_running(self.program)) == False:
            #-- If the The Framework not exist in the process execute the following steps.
                #-- Create a thread to reopen the Framework and run the Automated Processes with PyautoGUI
            print("[CONSOLE]:Framework has been closed restarting it.")
            FileHandler.Logger.logging('Framework has been closed restarting it')
            work = Thread(target=self.doafterFreeze, args=())
            work.start()
            self.runprocesses()
        if (self.is_it_freezed('Freeze')) == True:
            obj = Automating_System.MouseHandler()
            obj.click_to('close')
        ag.hotkey('numlock')
        t = Timer(self.MAX_WAIT_TIME, self.watchdogTimer)
        t.start()

    def doafterFreeze(self):
        '''Open The requested Program'''
        os.system(self.file_loc + self.program)

    def runprocesses(self):
        '''The function is looking for XML files in the directory. If found the Parser
        get the information from report and compare which tests has not runned yet.
        And Create a testlist with the remaining tests. The Automater open the testlist.
         '''
        #--Determine what is the latest report
        print ("[CONSOLE]:Getting Latest Report")
        fh = FileHandler.FileHandler(self.REPORT_PATH)
        latest_report = fh.latest_creation_date()
        #--Parsing the Report
        print ("[CONSOLE]:Parsing Latest Report")
        Report = Parser.XmlParser(latest_report)
        #--Getting the test's names from the TESTLIST_SAMPLE
        Report.get_all_tests(self.TESTLIST_SAMPLE)
        #--Getting the already executed tests name
        all_test = Parser.XmlParser.XML_ATTRS['all']
        Report.get_testnames()
        executed_tests = (Parser.XmlParser.XML_ATTRS['name'])
        skipped_tests = [i for i in all_test if i not in executed_tests]
        Parser.ListCreator().testlist_creator(
            skipped_tests,
            self.TESTLISTPATH,
            self.TESTLIST_SAMPLE)
        print ("[CONSOLE]:TestList has been created Succesfully")
        FileHandler.Logger.logging('TestList has been created Succesfully')
        #===============================================================================
        # # 3. The Framework crashed pick the Cotton then.
        #===============================================================================
        sleep(10)
        cottonpicker = Automating_System.Process_Container(self.TESTLIST_SAMPLE)
        cottonpicker.runTest('\Example.tl')


if __name__ == '__main__':
    os.chdir(r"d:\01_Documents\01_BMW_ACSM5\30_CompaFramework")
    file_loc = r"d:\01_Documents\01_BMW_ACSM5\30_CompaFramework\Compa Framework \-\ for LIN.cmd"
    t.watchdogTimer()
