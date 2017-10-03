
# -*- coding: utf-8 -*-

import os
from WatchDog import Sentinel
from ReportHandler import Parser
from threading import Thread
from datetime import datetime
from time import sleep
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
$Source: Starter.py
$Revision: 1.1 $
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
Revision 0.8:
- Added Configurator Class.
- Removing TESTLIST MAPPER Dictionary.
- Added Exception Handling for more functions.

Revision 0.9 :
-Added more System Messages
-Added Logger Functions
-Removed TestConfig Attribute getter from the Parser because it was redundant

Revision 1.0:
- Added new property to configurator Class
- Instrument Init now works with parameters not /w template mathcing
- Hard coded String Removed. Now Configurator Class parse and XML

- Added new property for Moushandler Class Failsafe and delay time
- Redundance improvements
- More better GUI
- Now Installer Is Available
- Timestamp now appear after every action on the console window
- Added Exceptions(No Config file, No Valid Path, Screen Grab failed)
- Console String Messages has been moved to Logger as Class variables
- All Threads are Daemon now (If main application quit all threads die)
- New Exception Handled: object Reference not set to an instance of an object
- Logger Improved Now(After test finish creates summary about number of freezes and cause of freezes)


BUGFIXES REQUIRED:

·    Detect If Test has been completed and rerun the Failed Testcases.
·    Move Freezedetect.Console_log to other folder


IMPROVEMENTS NEEDED:
·    Develop more smart picture recognition scheme
·    Duplicated stuff  report = Parser.XmlParser(self.testlist_sample)
            report.get_all_tests(self.testlist_sample)
"""


class Configurator(object):

    console_message = Queue()

    def _init_(self):
        try:
            self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._co_fw_dir_path = Parser.XmlParser.XML_CONFIG['COFWDIRPATH']
            self._co_fw_path = Parser.XmlParser.XML_CONFIG['COFWPATH']
            self._co_fw_exe = Parser.XmlParser.XML_CONFIG['COFWEXE']
            self._report_path = Parser.XmlParser.XML_CONFIG['REPORT']
            self._testlistpath = Parser.XmlParser.XML_CONFIG['TESTLISTPATH']
            self._testlist_sample = Parser.XmlParser.XML_CONFIG['TESTLISTSAMPLE']
            self._process_name = self._co_fw_exe.split('\\')[-1]
            self._bslash_modifier = Parser.XmlParser.XML_CONFIG['BSLASHMODIFIER']
            self._bslash_btn = Parser.XmlParser.XML_CONFIG['BSLASHBUTTON']
            self._isc_framework = Parser.XmlParser.XML_CONFIG['ISCFRAMEWORK']
            self._finish_detection = True
            Configurator.console_message.put('[CONSOLE]: Init Success')
        except Exception:
            Configurator.console_message.put('[CONSOLE]: Init Failed. Config Error !')
            sleep(5)
            os._exit(0)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def co_fw_dir_path(self):
        return self._co_fw_dir_path

    @property
    def co_fw_path(self):
        return self._co_fw_path

    @property
    def co_fw_exe(self):
        return self._co_fw_exe

    @property
    def report_path(self):
        return self._report_path

    @property
    def testlistpath(self):
        return self._testlistpath

    @property
    def testlist_sample(self):
        return self._testlist_sample

    @property
    def process_name(self):
        return self._process_name

    @property
    def isc_framework(self):
        return self._isc_framework

    @property
    def finish_detection(self):
        return self._finish_detection

    @co_fw_dir_path.setter
    def co_fw_dir_path(self, value):
        self._co_fw_dir_path = value

    @co_fw_path.setter
    def co_fw_path(self, value):
        self._co_fw_path = value

    @co_fw_exe.setter
    def co_fw_exe(self, value):
        self._co_fw_exe = value

    @report_path.setter
    def report_path(self, value):
        self._report_path = value

    @testlistpath.setter
    def testlistpath(self, value):
        self._testlistpath = value

    @testlist_sample.setter
    def testlist_sample(self, value):
        self._testlist_sample = value

    @process_name.setter
    def process_name(self, value):
        self._PROCES_NAME = value

    @finish_detection.setter
    def finish_detection(self, value):
        self._co_fw_dir_path = value

    @property
    def bslash_modifier(self):
        return self._bslash_modifier

    @property
    def bslash_btn(self):
        return self._bslash_btn


def worker():
    run = Sentinel.FreezeDetect()
    try:
        run.watchdogTimer()
    except ag.FailSafeException:
        App.GUI.failSafeHandler()

if _name_ == "_main_":
    try:
        config_source = os.path.dirname(os.path.realpath(__file__)) + '\\Config\CoFW_Wathcdog.xml'
    except NameError:  # We are the main CX_Freeze script not the module
        import sys
        config_source = os.path.dirname(
            os.path.realpath(
                (sys.argv[0]))) + '\\Config\CoFW_Wathcdog.xml'
    try:
        Parser.XmlParser(config_source).get_config()
    except AttributeError:
        App.GUI.errorHandler('The Configuration file corrupted or not exist.')
        os._exit(0)
    init = Configurator()
    try:
        os.chdir(init.co_fw_dir_path)
    except FileNotFoundError:
        App.GUI.errorHandler(
            'The PATH not exist what defined in ' +
            sys.executable +
            '\Config\WathcDog.xml\nPlease Check the settings in that file.')
        os._exit(0)
    workerThread = Thread(target=worker)
    workerThread.daemon = True
    workerThread.start()
    App.GUI()
