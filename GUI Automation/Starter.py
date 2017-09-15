
# -*- coding: utf-8 -*-

from WatchDog import Sentinel
import os
from FileHandler import Parser
from threading import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
from WatchDog import InterruptHandlerGUI as App
import pyautogui as ag

"""
=============================================================================================
COMPA FRAMEWORK WATCHDOG
=============================================================================================
                            OBJECT SPECIFICATION
=============================================================================================
$ProjectName: BMW ACSM5 $
$Source: Application.py
$Revision: 0.3 $
$Author: David Szurovecz $
$Date: 2017/08/24 08:24:32CEST $

Purpose : : Program should sense that the test has been stopped and realize the actual
progress has been made before the collision and restart it from the correct point.

Approach: Due to the Internal AD-Hoc Frameworks closed property there is no
any API to use. So GUI Automation is required with a mix of Picture Recoginiton.

Requirements:

- Detect any type Of Compa Framework collision during Testing.
- Determine the Test completeness rate. Which tests are executed and which not.
- Create a New Testlist what contains the not completed tests.
- Setup the Framework and Execute the Tests by running the Testlist.

1 Detect if the Framework is stopped working.
    A Watchdog Timer Cycles through every 5 seconds with a polling technique and checks
    if the Framework Freezed.

    There is three types of Freezes:
        - The CoFW Just closing without any error message. And the Process also terminated.
        - The CoFW Throwing an error message (Compa Framework stopped working )
          but the process still alive. Tests has been terminated.
        - The CoFW Throwing an error message (object Reference not set to an instance of an object)
          The Process is alive and tests is running. This is the worst All the test results will be failed.
          (This type of Problem not solved yet.)

2. If the Framework is freezed Restart it.

    Before reopening the Framework the tool is parsing the report to determine where
    the program has been freezed. Afterwards it Creates a Testlist.

    The program will Start CoFW and Opening the Required Instruments Channels.
    CAN1,CAN2,FlexRay1,FlexRay2,Colibri,PS1 and Opening the Testlist and Run the Test.

    Approach: Take a screenshot from the desktop and match template with the requred image.
    See more at : http://docs.opencv.org/3.2.0/d4/dc6/tutorial_py_template_matching.html
    IMPORTANT: If You're using Remote Desktop and Leaving the Machine might be not works.
    Thats why the tests Every X seconds pushing the Num Lock button.

3. Used Third Party Libraries:
    -PyAutoGUI
    -NumPy
    -CV2
    -Lxml etree




HISTORY:
Revision 0.3:
- Added Configurator Class.
- Removing TESTLIST MAPPER Dictionary.
- Added Exception Handling for more functions.

Revision 0.4 :
-Added more System Messages
-Added Logger Functions
-Removed TestConfig Attribute getter from the Parser because it was redundant

Revision 0.5:
- Added new property to configurator Class
- Instrument Init now works with parameters not /w template mathcing
- Hard coded String Removed. Now Configurator Class parse and XML

Revision 0.6:
- Added new property for Moushandler Class Failsafe and delay time
- Redundance improvements
- More better GUI


BUGFIXES REQUIRED:

·    Detect If Test has been completed and rerun the Failed Testcases.
·    Before Automation Process Start check if Framework is running.


IMPROVEMENTS NEEDED:
https://pyautogui.readthedocs.io/en/latest/introduction.html#dependencies
·    Develop more smart picture recognition scheme
-    ThreadPool ???
·    Develop more detailed logger with the following attributes: Cause of Freeze, Status Percent, DTC-s of failed testcases.
·    Wait Time Flexibility
·    Redundance lot of places Configurator imports are available
·    When Closing GUI windows Destroy all threads. Create Dameon Thread
-  Duplicated stuff  report = Parser.XmlParser(self.testlist_sample)
            report.get_all_tests(self.testlist_sample)
=============================================================================================
"""


class Configurator(object):

    console_message = Queue()
    console_message.put('[CONSOLE]: Init Success')

    def __init__(self):
        self.__co_fw_dir_path = Parser.XmlParser.XML_CONFIG['COFWDIRPATH']
        self.__co_fw_path = Parser.XmlParser.XML_CONFIG['COFWPATH']
        self.__co_fw_exe = Parser.XmlParser.XML_CONFIG['COFWEXE']
        self.__report_path = Parser.XmlParser.XML_CONFIG['REPORT']
        self.__testlistpath = Parser.XmlParser.XML_CONFIG['TESTLISTPATH']
        self.__testlist_sample = Parser.XmlParser.XML_CONFIG['TESTLISTSAMPLE']
        self.__process_name = self.__co_fw_exe.split('\\')[-1]
        self.__isc_framework = True
        self.__finish_detection = True

    @property
    def co_fw_dir_path(self):
        return self.__co_fw_dir_path

    @property
    def co_fw_path(self):
        return self.__co_fw_path

    @property
    def co_fw_exe(self):
        return self.__co_fw_exe

    @property
    def report_path(self):
        return self.__report_path

    @property
    def testlistpath(self):
        return self.__testlistpath

    @property
    def testlist_sample(self):
        return self.__testlist_sample

    @property
    def process_name(self):
        return self.__process_name

    @property
    def isc_framework(self):
        return self.__isc_framework

    @property
    def finish_detection(self):
        return self.__finish_detection

    @co_fw_dir_path.setter
    def co_fw_dir_path(self, value):
        self.__co_fw_dir_path = value

    @co_fw_path.setter
    def co_fw_path(self, value):
        self.__co_fw_path = value

    @co_fw_exe.setter
    def co_fw_exe(self, value):
        self.__co_fw_exe = value

    @report_path.setter
    def report_path(self, value):
        self.__report_path = value

    @testlistpath.setter
    def testlistpath(self, value):
        self.__testlistpath = value

    @testlist_sample.setter
    def testlist_sample(self, value):
        self.__testlist_sample = value

    @process_name.setter
    def process_name(self, value):
        self.__PROCES_NAME = value

    @finish_detection.setter
    def finish_detection(self, value):
        self.__co_fw_dir_path = value


def worker():
    run = Sentinel.FreezeDetect()
    try:
        run.watchdogTimer()
    except ag.FailSafeException:
        App.GUI.failSafeHandler()

if __name__ == "__main__":
    try:
        config_source = os.path.dirname(os.path.realpath(__file__)) + '\\Config\CoFW_Wathcdog.xml'
    except NameError:  # We are the main CX_Freeze script not the module
        import sys
        config_source = os.path.dirname(
            os.path.realpath(
                (sys.argv[0]))) + '\\Config\CoFW_Wathcdog.xml'
    Parser.XmlParser(config_source).get_config()
    init = Configurator()
    os.chdir(init.co_fw_dir_path)
    workerThread = Thread(target=worker)
    workerThread.start()
    App.GUI()
