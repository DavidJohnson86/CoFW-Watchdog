
# -*- coding: utf-8 -*-

import sys
import os
from time import sleep
from subprocess import Popen, PIPE, check_output
from threading import Thread, Timer
from Automater import Automating_System
from FileHandler import FileHandler, Parser
from Starter import Configurator
from WatchDog import InterruptHandlerGUI


try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
try:
    import pyautogui as ag
except ImportError:
    print ('PyautoGUI is not installed')


ON_POSIX = 'posix' in sys.builtin_module_names


class FreezeDetect(Configurator):

    console_message = Queue()
    console_message.put('[CONSOLE]: Framework Init Success')

    def __init__(self):
        Configurator.__init__(self)
        self.MAX_WAIT_TIME = 3
        #Console = InterruptHandlerGUI.GUI()

    def is_it_running(self, program_name):
        '''This Function is check if the Current Process Exist in the Task Manager.'''
        n = 0  # number of instances of the program running
        prog = [line.split() for line in check_output("tasklist").splitlines()]
        [prog.pop(e) for e in [0, 1, 2]]  # useless
        for task in prog:
            if task[0] == bytes(program_name, encoding='utf-8'):
                n = n + 1
        if n > 0:
            return True
        else:
            return False

    def watchdogTimer(self):
        '''We have to monitor 2 events: 1. the program running & 2. the program freezed.
        If the program not running its necessary to open it. Anyway opening the program
        will halt the program flow so this should be done on other thread.
        Timer is responsible to run the watchdogTimer Function in every x seconds
        where x == self.MAX_WAIT_TIME.'''
        if (self.is_it_running('CoFramework.exe')) == False:
            #-- If the The Framework not exist in the process execute the following steps.
            #-- Create a thread to reopen the Framework and run the Automated Processes with PyautoGUI
            #FreezeDetect.console_message.put("[CONSOLE]:Framework has been closed restarting it.")
            print("[CONSOLE]:Framework has been closed restarting it.")
            FileHandler.Logger.logging('Framework has been closed restarting it')
            work = Thread(target=self.doafterFreeze, args=())
            work.start()
            self.runprocesses()
        elif (Automating_System.MouseHandler.is_it_freezed('Freeze')) == True:
            #-- This part is checking if window pop up what shows : Compa Framework Stopped working
            #-- Afterwards window will be closed
            obj = Automating_System.MouseHandler()
            obj.click_to('close')
        ag.hotkey('numlock')
        t = Timer(self.MAX_WAIT_TIME, self.watchdogTimer)
        t.start()

    def doafterFreeze(self):
        '''Open The requested Program'''
        if (self.ISC_FRAMEWORK is True):
            command = 'start ./Framework/CoFramework.exe /u developer /InstrumentRegistry.OpenInstruments FXR1,FXR2,CAN1,CAN2,Colibri1,MFSAT0,PS1'
        process = Popen(command, shell=True, stdout=PIPE)
        process.wait()

    def runprocesses(self):
        '''The function is looking for XML files in the directory. If found the Parser
        get the information from report and compare which tests has not runned yet.
        And Create a testlist with the remaining tests. The Automater open the testlist.
         '''
        #--Determine what is the latest report
        print ("[CONSOLE]:Getting Latest Report")
        #FreezeDetect.console_message.put("[CONSOLE]:Getting Latest Report")
        fh = FileHandler.FileHandler(self.REPORT_PATH)
        latest_report = fh.latest_creation_date()
        #--Parsing the Report
        #FreezeDetect.console_message.put("[CONSOLE]:Parsing Latest Report")
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
        #FreezeDetect.console_message.put("[CONSOLE]:TestList has been created Succesfully")
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
