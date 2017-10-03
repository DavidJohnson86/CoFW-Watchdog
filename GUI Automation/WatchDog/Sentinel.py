
# -*- coding: utf-8 -*-
import pyautogui as ag
from os import _exit
from psutil import process_iter
from time import sleep
from subprocess import Popen, PIPE, check_output
from threading import Thread, Timer
from Automater import Automating_System
from ReportHandler.ReportHandler import ReportHandler
from ReportHandler import Parser
from ReportHandler.ReportHandler import Logger
from Starter import Configurator
from WatchDog.InterruptHandlerGUI import Transfer_Msg as GUI
from datetime import datetime
datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
try:
    import pyautogui as ag
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('PyautoGUI is not installed')


class FreezeDetect(Configurator, Thread):

    __WELCOME = '''----------------------------------------------------------------------------------
Compa Framework WathcDog is a helper tool
It helps to execute tests automatically after CoFW crashes
To Close Click On GUI Window and Press Escape
----------------------------------------------------------------------------------'''

    def __init__(self):
        Configurator.__init__(self)
        GUI.CONSOLE_MESSAGE.put(FreezeDetect.__WELCOME)
        self.MAX_WAIT_TIME = 10

    def is_it_running(self, program_name):
        '''This Function is check if the Current Process Exist in the Task Manager.
        :return: True if process is alive
        :return: False if process is not exist
        :param: name of the program.
        '''
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
        if self.is_it_running(self.process_name) == False:
            #-- If the The Framework not exist in the process execute the following steps.
            #-- Create a thread to reopen the Framework and run the Automated Processes with PyautoGUI
            FreezeDetect.console_log(Logger.FR_CLOSED)
            work = Thread(target=self.do_after_freeze, args=())
            work.daemon = True
            work.start()
            self.runprocesses()
        elif Automating_System.MouseHandler.is_it_freezed('Freezed') == True:
            #-- This part is checking if window pop up what shows : Compa Framework Stopped working execution
            #-- Afterwards window will be closed
            FreezeDetect.console_log(Logger.FR_FR1)
            obj = Automating_System.MouseHandler()
            obj.click_to('close')
        elif Automating_System.MouseHandler.is_it_freezed('ObjRefErr') == True:
            FreezeDetect.console_log(Logger.FR_FR2)
            self.kill_process()
        try:
            ag.hotkey('numlock')
        except ag.FailSafeException:
            pass
        cyclicThread = Timer(self.MAX_WAIT_TIME, self.watchdogTimer)
        cyclicThread.start()

    def kill_prcess(self):
        for proc in process_iter():
                # check whether the process name matches
            if proc.name() == self.process_name:
                proc.kill()

    @staticmethod
    def console_log(message):
        '''This function send the message to the console & save to the log file at the same time'''
        GUI.CONSOLE_MESSAGE.put(message + str(Logger.current_time()))
        Logger.logging(message + str(Logger.current_time()))

    def get_remaining_tests(self):
        '''
        This function is parsing the report and return the skipped tests
        :return: lisst about the remaining tests
        :return: False if the directory is empty
        :return: True if all test finished '''
        # --Determine what is the latest report
        latest_report = ReportHandler(self.report_path).latest_creation_date()
        if latest_report is None:
            return False
        Parser.XmlParser(latest_report).get_all_tests(self.testlist_sample)
        # --Getting the test's names from the testlist_sample
        self.all_test = Parser.XmlParser.XML_ATTRS['all']
        Parser.XmlParser(latest_report).get_testnames()
        #-- Check which tests are executed
        executed_tests = Parser.XmlParser.XML_ATTRS['name']
        skipped_tests = [i for i in self.all_test if i not in executed_tests]
        #-- If no skipped tests it means no remaining test
        if not skipped_tests:
            return True
        # --Getting the already executed tests name
        # -- Return the names of the remaining
        return skipped_tests

    def is_it_finished(self):
        '''Check if the tests are finished or just starting it '''
        if self.get_remaining_tests() is False:
            #-- There are no any report in the Report Folder so we initalize the testlist
            FreezeDetect.console_log(Logger.NO_REPORT)
            return False
        if self.get_remaining_tests() is True:
            #-- If all test finished parse for stats...
            FreezeDetect.console_log(Logger.TEST_FINISH)
            Logger.parse_stats()
            sleep(10)
            _exit(0)

    def do_after_freeze(self):
        '''Open The requested Program'''
        if self.isc_framework is True:
            command = 'start ./Framework/CoFramework.exe /u developer /InstrumentRegistry.OpenInstruments FXR1,FXR2,CAN1,CAN2,Colibri1,MFSAT0,PS1'
            self.process = Popen(command, shell=True, stdout=PIPE)
            self.process.wait()
        elif self.isc_framework is False:
            os.system(os.system('Compa Framework \\- for LIN.cmd'))

    def runprocesses(self):
        '''The function is looking for XML files in the directory. If found the Parser
        get the information from report and compare which tests has not runned yet.
        '''
        GUI.CONSOLE_MESSAGE.put(Logger.PARSE_REPORT + str(Logger.current_time()))
        skipped_tests = self.get_remaining_tests()
        GUI.CONSOLE_MESSAGE.put(Logger.GET_REPORT + str(Logger.current_time()))
        if self.is_it_finished() is False:
            report = Parser.XmlParser(self.testlist_sample)
            report.get_all_tests(self.testlist_sample)
            skipped_tests = Parser.XmlParser.XML_ATTRS['all']
        Parser.ListCreator().testlist_creator(
            skipped_tests,
            self.testlistpath,
            self.testlist_sample)
        GUI.CONSOLE_MESSAGE.put(Logger.TL_DONE + str(Logger.current_time()))
        sleep(15)  # Let time for the FW to init
        if self.is_it_running(self.process_name) == True:
            cottonpicker = Automating_System.Process_Container(self.testlist_sample)
            cottonpicker.runTest('\Example.tl')


if __name__ == '__main__':
    os.chdir(r"d:\01_Documents\01_BMW_ACSM5\30_CompaFramework")
    file_loc = r"d:\01_Documents\01_BMW_ACSM5\30_CompaFramework\Compa Framework \-\ for LIN.cmd"
    t.watchdogTimer()
