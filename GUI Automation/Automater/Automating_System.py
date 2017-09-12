
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
from time import sleep
from FileHandler import FileHandler
from Starter import Configurator


try:
    import numpy as np
except ImportError:
    print ('Numpy Is not installed.')
try:
    import matplotlib.pyplot as plt
except ImportError:
    print('Matplotlib is not installed')
try:
    from PIL import Image
except ImportError:
    print ('PIL is not installed')
try:
    import cv2
except ImportError:
    print ('Cv2 not installed')
try:
    from PIL import ImageGrab
except ImportError:
    print ('ImageGrab is not installed')
try:
    import pyautogui as ag
except ImportError:
    print ('PyautoGUI is not installed')


class MouseHandler():

    def __init__(self):
        self.fail_safe = True
        self.delay_time = 0.2

    @property
    def delay_time(self):
        return self.__delay_time

    @delay_time.setter
    def delay_time(self, value):
        ag.PAUSE = value

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
            print("[CONSOLE]:" + str(e))
            FileHandler.Logger.logging(str(e))

    def click_to(self, pattern, double=False):
        """
        :param pattern: The picture what are you looking for
        This Function is looking for a subimage from a Whole screenshot
        And clicking there where the subimage found"""

        MouseHandler.takeScreenShot()
        image = cv2.imread(
            os.path.dirname(
                os.path.realpath(__file__)) +
            "\\" +
            "tmp\screenshot.jpg",
            0)
        pattern = cv2.imread(
            os.path.dirname(
                os.path.realpath(__file__)) +
            "\\" +
            "patterns/" +
            pattern +
            ".jpg",
            0)
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
        image = cv2.imread(
            os.path.dirname(
                os.path.realpath(__file__)) +
            "\\" +
            "tmp\screenshot.jpg",
            0)
        pattern = cv2.imread(
            os.path.dirname(
                os.path.realpath(__file__)) +
            "\\" +
            "patterns\\" +
            pattern +
            ".jpg",
            0)
        res = cv2.matchTemplate(image, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= treshold)
        loc = list(zip(*loc[::-1]))
        if(len(loc) >= 1):
            return True
        else:
            return False


class Process_Container(object):
    """This class is containing all of the important processes
    what is required to deal with CoFw. Mostly related to test execution.
    """

    def __init__(self, TESTLISTPATH):
        self.TESTLISTPATH = TESTLISTPATH
        self.moveto = MouseHandler()

    def runTest(self, testname):
        ag.hotkey('enter')
        self.moveto.click_to('Plugin_Panel')
        self.moveto.click_to('Variation_Plugin')
        ag.hotkey('enter')
        self.moveto.click_to('Add_Testlist')
        self.path_converter(Configurator().TESTLISTPATH + testname)
        ag.hotkey('enter')
        ag.hotkey('enter')
        self.moveto.click_to('run')
        self.moveto.click_to('Run_List')

    def path_converter(self, path):
        '''PyautoGUI typewriter functions is not working well with Compa Framework on any
        other app is fine. This function helps to solve it.'''
        ag.PAUSE = 0
        testname = path.split('\\')[-1]
        for i in path.split('\\'):
            sleep(1.0)
            ag.typewrite(i)
            if (i == testname):
                break
            ag.keyDown('altright')
            ag.hotkey('q')
            ag.keyUp('altright')
        ag.PAUSE = 2.5
