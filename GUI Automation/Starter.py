
# -*- coding: utf-8 -*-

from WatchDog import Sentinel
import os

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

IMPROVEMENTS NEEDED:
-https://pyautogui.readthedocs.io/en/latest/introduction.html#dependencies
-Detects if the Test is finished.
- Not always parse from Alle.tl if the test is finished. Crate a new TL with the failed ones.
-Remove Hardcodes strings
-Add Logging Functions
-Wait Time Issues Handling
-Logger Improvements.
-Be able to Detect Object Reference Error.
-Find Solution for PyAutoGUI typewriter bug Handling.
-Find Solution for Running Compa Framework with Instrument Parameters.
-Create Executable.
-Move is if freezed function from Sentinel to Automating System this will save imports
=============================================================================================
"""


class Configurator(object):

    def __init__(self):
        self.__CO_FW_DIR_PATH = r'd:\ISC_TestBench\Testplans_S20XL_BMW_ASCM5_ISC_Framework'
        self.__CO_FW_PATH = self.CO_FW_DIR_PATH + '\\' + 'Framework' + '\\'
        self.__CO_FW_EXE = self.CO_FW_PATH + 'CoFramework.exe'
        self.__REPORT_PATH = self.CO_FW_DIR_PATH + '\\' + 'Reports' + '\\'
        self.__TESTLISTPATH = self.CO_FW_DIR_PATH + '\\' + 'Testplans\BMW_ACSM5\config\TestList'
        self.__TESTLIST_SAMPLE = self.CO_FW_DIR_PATH + '\\' + \
            'Testplans\BMW_ACSM5\config\TestList\ALLE.tl'
        os.chdir(self.CO_FW_DIR_PATH)

    @property
    def CO_FW_DIR_PATH(self):
        return self.__CO_FW_DIR_PATH

    @property
    def CO_FW_PATH(self):
        return self.__CO_FW_PATH

    @property
    def CO_FW_EXE(self):
        return self.__CO_FW_EXE

    @property
    def REPORT_PATH(self):
        return self.__REPORT_PATH

    @property
    def TESTLISTPATH(self):
        return self.__TESTLISTPATH

    @property
    def TESTLIST_SAMPLE(self):
        return self.__TESTLIST_SAMPLE

    @CO_FW_DIR_PATH.setter
    def CO_FW_DIR_PATH(self, value):
        self.__CO_FW_DIR_PATH = value

    @CO_FW_PATH.setter
    def CO_FW_PATH(self, value):
        self.__CO_FW_PATH = value

    @CO_FW_EXE.setter
    def CO_FW_EXE(self, value):
        self.__CO_FW_EXE = value

    @REPORT_PATH.setter
    def REPORT_PATH(self, value):
        self.__REPORT_PATH = value

    @TESTLISTPATH.setter
    def TESTLISTPATH(self, value):
        self.__TESTLISTPATH = value

    @TESTLIST_SAMPLE.setter
    def TESTLIST_SAMPLE(self, value):
        self.__TESTLIST_SAMPLE = value


if __name__ == "__main__":
    PROGRAM_NAME, WAIT_TIME = 'CoFramework.exe', 3
    prog = Sentinel.FreezeDetect(PROGRAM_NAME, Configurator().CO_FW_PATH, WAIT_TIME)
    prog.watchdogTimer()
