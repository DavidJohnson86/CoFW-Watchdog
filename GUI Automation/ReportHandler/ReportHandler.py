import os
import ntpath
import sys
ntpath.basename("a/b/c")
from datetime import datetime


class ReportHandler(object):
    """Responsible for searching latest report file in a specific directory"""

    def __init__(self, report_path):
        self.report_path = report_path

    def latest_creation_date(self):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        """
        latest_report = None
        max_value = 0
        for fileName in os.listdir(self.report_path):
            if fileName.endswith(".xml"):
                if not fileName.endswith("_.xml"):
                    if (os.path.getctime(self.report_path + fileName)) > max_value:
                        max_value = os.path.getctime(self.report_path + fileName)
                        latest_report = self.report_path + fileName
        return latest_report

    def getfiles_dir(self):
        fileNames = [fileName for fileName in os.listdir(co_fw_path) if fileName.endswith(".xml")]
        return fileNames


class Logger():

    FR_CLOSED = "[CONSOLE]: Framework has been closed restarting it "
    NO_REPORT = "[CONSOLE]: No existing report has been found "
    TEST_FINISH = "[CONSOLE]: All test finished. Quitting..."
    PARSE_REPORT = "[CONSOLE] :Parsing Latest Report "
    GET_REPORT = "[CONSOLE]: Found Latest Report "
    TL_DONE = "[CONSOLE]: TestList has been created Succesfully "
    FR_FR1 = "[CONSOLE]: Compa Framework Stopped working execution "
    FR_FR2 = "[CONSOLE]: Object Reference has not set to an instance object "
    DUPLICATE = "[CONSOLE]: Duplicated testcases found rerun not possible "
    _start_date = None
    _end_date = None
    _freeze_counter1 = 0
    _freeze_counter2 = 0
    _sum_freeze_counter = 0
    _restart_counter = 0

    @staticmethod
    def logging(message):

        if getattr(sys, 'frozen', False):
            pathdir = os.path.dirname(sys.executable)
        else:
            pathdir = os.path.dirname(os.path.dirname(__file__))
        logfilename = pathdir + '\\Logs\\' + 'ErrorLog'
        logfile = open(pathdir + '\\Logs\\' + 'ErrorLog', "a")
        logfile.write(str(message) + '\n')
        logfile.close()
        return logfilename

    @staticmethod
    def parse_stats():
        if getattr(sys, 'frozen', False):
            pathdir = os.path.dirname(sys.executable)
        else:
            pathdir = os.path.dirname(os.path.dirname(__file__))
        logfile = open(pathdir + '\\Logs\\' + 'ErrorLog', "r")
        Logger._start_date = ' '.join(logfile.readline().strip().split(' ')[-2:])
        for row in logfile.readlines():
            if 'Compa Framework Stopped working execution' in row:
                Logger._freeze_counter1 += 1
            if 'Object Reference has not set to an instance object':
                Logger._freeze_counter2 += 1
            if 'Framework has been closed restarting it' in row:
                Logger._restart_counter += 1
                Logger._end_date = ' '.join(row.strip().split(' ')[-2:])
        logfile.close()
        logfile = open(pathdir + '\\Logs\\' + 'ErrorLog', "a")
        logfile.write('Summary:\n')
        logfile.write('Compa Framework Stopped working execution freeze occured ' +
                      str(Logger._freeze_counter1) +
                      ' times.\n')
        logfile.write('Object Reference has not set to an instance object freeze occured ' +
                      str(Logger._freeze_counter2) +
                      ' times.\n')
        Logger._sum_freeze_counter = Logger._freeze_counter1 + Logger._freeze_counter2
        logfile.write('Compa Framework Freezed totally ' +
                      str(Logger._sum_freeze_counter) +
                      ' times during execution.\n')
        logfile.write('From Date: ' +
                      str(Logger._start_date) + ' until ' + str(Logger._end_date))
        logfile.close()

    @staticmethod
    def current_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def path_leaf(path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

if __name__ == "__main__":
    Logger.parse_stats()
