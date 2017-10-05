
# -*- coding: utf-8 -*-

"""
==============================================================================
GUI Automation for CoFW
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5 $
$Source: Application.py
$Revision: 0.1 $
$Author: David Szurovecz $
$Date: 2017/08/11 12:04:32CEST $
============================================================================

"""
import os
import sys
import WatchDog
from time import sleep
from Starter import Configurator


try:
    import numpy.core.multiarray
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('numpy.core.multiarry is not found')
try:
    import numpy as np
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('Numpy is not installed')
try:
    import matplotlib.pyplot as plt
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('Matplotlib is not installed')
try:
    from PIL import Image
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('PIL.Image not found')
try:
    import cv2
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('Cv2 is not installed')
try:
    from PIL import ImageGrab
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('ImageGrab is not installed')
try:
    import pyautogui as ag
except ImportError:
    if getattr(sys, 'frozen', False):
        pass
    else:
        print ('PyautoGUI is not installed')


class MouseHandler():

    def __init__(self):
        self.__fail_safe = True

    @property
    def fail_safe(self):
        return self.__fail_safe

    @fail_safe.setter
    def fail_safe(self, value):
        ag.FAILSAFE = value

    @staticmethod
    def takeScreenShot():
        """Calling this function will make a screenshot from your desktop"""
        try:
            image = ImageGrab.grab()
            if(not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp")):
                os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp")
            image.save(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp\screenshot.jpg")
        except Exception as e:
            WatchDog.Sentinel.FreezeDetect.console_log("[CONSOLE]: " + str(e) + " ")

    def click_to(self, pattern, double=False):
        """
        :param pattern: The picture what are you looking for
        This Function is looking for a subimage from a Whole screenshot
        And clicking there where the subimage found"""

        MouseHandler.takeScreenShot()
        image = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "\\" +
                           "tmp\screenshot.jpg", 0)
        pattern = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "\\" +
                             "patterns/" + pattern + ".jpg", 0)
        res = cv2.matchTemplate(image, pattern, cv2.TM_CCOEFF_NORMED)
        y, x = np.unravel_index(res.argmax(), res.shape)
        if not double:
            ag.click(x + 5, y + 5)
        else:
            ag.doubleClick(x + 5, y + 5)

    @staticmethod
    def is_it_freezed(pattern, treshold=0.8):
        '''This Function is Detecting if the Compa Framewok stopped working window pops up. '''
        MouseHandler.takeScreenShot()
        image = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "\\" +
                           "tmp\screenshot.jpg", 0)
        pattern = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "\\" +
                             "patterns\\" + pattern + ".jpg", 0)
        res = cv2.matchTemplate(image, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= treshold)
        loc = list(zip(*loc[::-1]))
        if(len(loc) >= 1):
            return True
        else:
            return False


class Process_Container(Configurator):
    """This class is containing all of the important processes
    what is required to deal with CoFw. Mostly related to test execution.
    """

    def __init__(self, testlistpath):
        Configurator.__init__(self)
        self.testlistpath = testlistpath
        self.moveto = MouseHandler()
        self.__delay_time = 0.4
        ag.PAUSE = self.__delay_time

    @property
    def delay_time(self):
        return self.__delay_time

    @delay_time.setter
    def delay_time(self, value):
        self.__delay_time = value

    def runTest(self, testname):
        if self.isc_framework == 'True':
            ag.hotkey('enter')
        elif self.isc_framework == 'False':
            ag.hotkey('enter')
            ag.hotkey('enter')
        self.moveto.click_to('Plugin_Panel')
        self.moveto.click_to('Variation_Plugin')
        ag.hotkey('enter')
        self.moveto.click_to('Add_Testlist')
        ag.PAUSE = 0.1
        self.path_converter(Configurator().testlistpath + testname)
        ag.PAUSE = self.__delay_time
        for i in range(0, 3):
            sleep(1)
            ag.hotkey('enter')
        sleep(1)
        self.moveto.click_to('run')
        self.moveto.click_to('Run_List')

    def path_converter(self, path):
        '''PyautoGUI typewriter functions is not working well with Compa Framework
        This function helps to solve it.
        :param: str: path of the testlist'''
        testname = path.split('\\')[-1]
        for word in path.split('\\'):
            sleep(1)
            ag.typewrite(word)
            if (word == testname):
                break
            ag.keyDown(self.bslash_modifier)
            ag.hotkey(self.bslash_btn)
            ag.keyUp(self.bslash_modifier)
