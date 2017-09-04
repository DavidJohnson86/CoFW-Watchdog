
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
$Date: 2017/07/11 12:04:32CEST $
============================================================================

Purpose : The aim of this tool to restarting the CoFW if any freezing occurs.

Process:

1. Detect if the Framework is freezed.
2. Open the program.
3. Take Screeshot
4. Detect Icons to to click on. See more at : http://docs.opencv.org/3.2.0/d4/dc6/tutorial_py_template_matching.html
5. Determine

"""
import os
import time
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


class MouseHandler(object):

    def __init__(self):
        pass

    def takeScreenShot(self):
        """Calling this function will make a screenshot from your desktop"""
        try:
            image = ImageGrab.grab()
            if(not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp")):
                os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp")
            image.save(os.path.dirname(os.path.realpath(__file__)) + "\\" + "tmp/screenshot.jpg")
            del(image)
        except Exception as e:
            print("[CONSOLE]:" + str(e))
            FileHandler.Logger.logging(str(e))

    def click_to(self, pattern, double=False):
        """
        :param pattern: The picture what are you looking for
        This Function is looking for a subimage from a Whole screenshot
        And clicking there where the subimage found"""

        self.takeScreenShot()
        image = cv2.imread(
            os.path.dirname(
                os.path.realpath(__file__)) +
            "\\" +
            "tmp/screenshot.jpg",
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


class Process_Container(object):
    """This class is containing all of the important processes
    what is required to deal with CoFw. Mostly related to test execution.
    """

    def __init__(self, TESTLISTPATH):
        self.TESTLISTPATH = TESTLISTPATH
        self.moveto = MouseHandler()

    def runTest(self, testname):
        time.sleep(1)
        ag.hotkey('enter')
        self.moveto.click_to('Plugin_Panel')
        time.sleep(2)
        self.moveto.click_to('Variation_Plugin')
        time.sleep(2)
        ag.hotkey('enter')
        time.sleep(2)
        self.moveto.click_to('Add_Testlist')
        self.path_converter(Configurator().TESTLISTPATH + testname)
        time.sleep(2)
        ag.hotkey('enter')
        time.sleep(2)
        ag.hotkey('enter')
        time.sleep(2)
        self.moveto.click_to('run')
        time.sleep(3)
        self.moveto.click_to('Run_List')

    def path_converter(self, path):
        '''PyautoGUI typewriter functions is not working well with Compa Framework on any
        other app is fine. This function helps to solve it.'''
        testname = path.split('\\')[-1]
        ag.typewrite(
            path[0])  # Typewriter behaviour only in Compa Framework Starting listing from 1 not 0
        for i in path.split('\\'):
            time.sleep(1.0)
            ag.typewrite(i)
            if (i == testname):
                break
            ag.keyDown('altright')
            ag.hotkey('q')
            ag.keyUp('altright')

    def preprocess(self, text):
        """Pyautogui typewrite function have a bug this function prevent the bug."""
        text = text
        output = []
        for x in range(len(text)):
            output.append(str(text)[x])
        return output


if __name__ == "__main__":
    p = Process_Container(
        r'd:\01_Documents\01_BMW_ACSM5\30_CompaFramework\Framework\CoFramework.exe')
    p.preprocess(r'd:\01_Documents\01_BMW_ACSM5\30_CompaFramework\Framework\CoFramework.exe')
    pass
