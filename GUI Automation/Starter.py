
# -*- coding: utf-8 -*-

from WatchDog import Sentinel
import os
from FileHandler import Parser

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


IMPROVEMENTS NEEDED:
https://pyautogui.readthedocs.io/en/latest/introduction.html#dependencies
·    Detect If Test has been completed and rerun the Failed Testcases.
·    Develop more smart picture recognition scheme
·    Develop GUI
·    Develop better FAIL SAFE Function for Human Control
·    Develop more detailed logger with the following attributes: Cause of Freeze, Status Percent, DTC-s of failed testcases.
·    Wait Time Flexibility
=============================================================================================
"""


class Configurator(object):

    def __init__(self):
        self.__CO_FW_DIR_PATH = Parser.XmlParser.XML_CONFIG['COFWDIRPATH']
        self.__CO_FW_PATH = Parser.XmlParser.XML_CONFIG['COFWPATH']
        self.__CO_FW_EXE = Parser.XmlParser.XML_CONFIG['COFWEXE']
        self.__REPORT_PATH = Parser.XmlParser.XML_CONFIG['REPORT']
        self.__TESTLISTPATH = Parser.XmlParser.XML_CONFIG['TESTLISTPATH']
        self.__TESTLIST_SAMPLE = Parser.XmlParser.XML_CONFIG['TESTLISTSAMPLE']
        self.__ISC_FRAMEWORK = True

    def start(self):
        os.chdir(self.CO_FW_DIR_PATH)
        run = Sentinel.FreezeDetect()
        run.watchdogTimer()

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

    @property
    def ISC_FRAMEWORK(self):
        return self.__ISC_FRAMEWORK

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
    config_source = os.path.dirname(os.path.realpath(__file__)) + '\\Config\CoFW_Wathcdog.xml'
    Parser.XmlParser(config_source).get_config()
    Configurator().start()
