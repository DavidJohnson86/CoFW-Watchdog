import os
import time
import ntpath
ntpath.basename("a/b/c")


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


class Logger(object):

    @staticmethod
    def logging(message):

        timestamp = str(time.strftime('%Y_%m_%d_%H_%M'))
        pathdir = os.path.dirname(os.path.dirname(__file__))
        logfilename = pathdir + '\\Logs\\' + 'ErrorLog'
        logfile = open(pathdir + '\\Logs\\' + 'ErrorLog', "a")
        logfile.write('Event: ' + str(message))
        logfile.write(str(time.strftime('\n' + 'Date: ' '%Y-%m-%d:%H:%M')) + '\n')
        logfile.write('\n' + '-' * 60 + '\n')
        logfile.close()
        return logfilename

    @staticmethod
    def path_leaf(path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

if __name__ == "__main__":
    Logger.logging('Error Framework frezzed')