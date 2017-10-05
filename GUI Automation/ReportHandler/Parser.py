'''
==============================================================================
Main modules for parsing and modifying Xml Files for BMW ACSM5 Project
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5
$Source: Parser.py
$Revision: 1.1 $
$Author: David Szurovecz $
$Date: 2017/07/14 16:05:32CEST $

============================================================================
'''

from lxml import etree


class XmlParser(object):

    XML_ATTRS = {}
    XML_FAILED = []
    XML_CONFIG = {}

    def __init__(self, source):
        try:
            INFILE = etree.parse(source)
            self.INFILE_ROOT = INFILE.getroot()
        except OSError:
            print('Cannot Parse FILE')
            return None  # If File not exist or directory not exist
        except TypeError:
            print('Cannot Parse FILE')
            return False  # If Directory exist bu

        # self.get_allfailedobject()

    def get_config(self):
        XmlParser.XML_CONFIG['COFWDIRPATH'] = self.INFILE_ROOT.xpath(
            "//Configuration//COFWDIRPATH/text()")[0]
        XmlParser.XML_CONFIG['COFWPATH'] = self.INFILE_ROOT.xpath(
            "//Configuration//COFWPATH/text()")[0]
        XmlParser.XML_CONFIG['COFWEXE'] = self.INFILE_ROOT.xpath(
            "//Configuration//COFWEXE/text()")[0]
        XmlParser.XML_CONFIG['REPORT'] = self.INFILE_ROOT.xpath("//Configuration//REPORT/text()")[0]
        XmlParser.XML_CONFIG['TESTLISTPATH'] = self.INFILE_ROOT.xpath(
            "//Configuration//TESTLISTPATH/text()")[0]
        XmlParser.XML_CONFIG['TESTLISTSAMPLE'] = self.INFILE_ROOT.xpath(
            "//Configuration//TESTLISTSAMPLE/text()")[0]
        XmlParser.XML_CONFIG['BSLASHMODIFIER'] = self.INFILE_ROOT.xpath(
            "//Configuration//BSLASHMODIFIER/text()")[0]
        XmlParser.XML_CONFIG['BSLASHBUTTON'] = self.INFILE_ROOT.xpath(
            "//Configuration//BSLASHBUTTON/text()")[0]
        XmlParser.XML_CONFIG['ISCFRAMEWORK'] = self.INFILE_ROOT.xpath(
            "//Configuration//ISCFRAMEWORK/text()")[0]

    def get_testnames(self):
        try:
            XmlParser.XML_ATTRS['name'] = [element[7].attrib['val'] for element in self.INFILE_ROOT.xpath(
                "//COMPA-REPORT//SEQ[@TestVariationIndex]")]
        except IndexError:
            XmlParser.XML_ATTRS['name'] = ''

    def get_failedtestnames(self):
        ''' Parsing all the nodes with all data where FailedMeasurements > 0'''
        try:
            XmlParser.XML_FAILED = [element[7].attrib['val'] for element in self.INFILE_ROOT.xpath(
                "//COMPA-REPORT//SEQ[@TestVariationIndex]") if int(element[13].attrib['val']) > 0]
        except IndexError:
            XmlParser.XML_FAILED = []

    def get_all_tests(self, testlist):
        self.TESTLIST = etree.parse(testlist)
        self.TESTLIST_ROOT = self.TESTLIST.getroot()
        try:
            XmlParser.XML_ATTRS['all'] = [element.text for element in self.TESTLIST_ROOT.xpath(
                "//COMPA-FRAMEWORK//VARIATION-TESTLIST//TESTCONFIG//VARIATION//DISABLED")]
        except IndexError:
            XmlParser.XML_ATTRS['all'] = ''

    def get_testconfig(self):
        try:
            XmlParser.XML_ATTRS['testconfig'] = (
                self.INFILE_ROOT[-1][8].attrib['val']).split('\\')[-1]
        except IndexError:
            XmlParser.XML_ATTRS['testconfig'] = ''

    @staticmethod
    def delete_failedtest(source, listofFailed, output):
        '''
        :param: list of failed tests
        :return: number of failed tests and the removed failed tests
        '''
        tree = etree.parse(source)
        root = tree.getroot()
        counter = 0
        removed_tests = []
        for elem in root:
            if elem[7].attrib['val'] in listofFailed:
                root.remove(elem)
                removed_tests.append(elem[7].attrib['val'])
                counter += 1
        tree.write(output, xml_declaration=True)
        return counter, removed_tests


class ListCreator(object):

    @staticmethod
    def testlist_creator(listofFailed, output, inlist):
        inlist = etree.parse(inlist)
        '''if listofFailed is None or True or False:
            inlist.write(str(output) + '\Example.tl')
            return'''
        row_counter, set_counter = 0, 0
        inlist_root = inlist.getroot()
        for test_sets in range(1, len(inlist_root[0]), 2):
            elem = inlist_root[0][test_sets][0]
            for test_cases in range(0, len(elem)):
                if elem[test_cases].tag == 'ENABLED':
                    row_counter = 0
                    numof_testcases = int(1 + len(elem[test_cases].text) / 2)
                    test_states = numof_testcases * [0]
                    test_status = elem[test_cases]
                row_counter += 1
                set_counter += 1
                if elem[test_cases].text in listofFailed:
                    test_states[row_counter - 2] = 1
                    test_status.text = str(test_states)[1:-1:]
                    inlist.write(str(output) + '\Example.tl')

    @staticmethod
    def check_equal(iterator):
        '''Check If duplicated element in a list
        :param: list
        :return: True if unique
        :return: False if duplicated element found
        '''
        return len(set(iterator)) == len(iterator)

if __name__ == "__main__":
    p = XmlParser(r'd:\temp\ISC_Sensor_Emulation_Unknown_XmlReport.xml')
    p.get_failedtestnames()
    listofFailed = XmlParser.XML_FAILED
    # executed_tests = (XmlParser.XML_ATTRS['name'])
    # skipped_tests = [i for i in all_test if i not in executed_tests]
    # ListCreator.testlist_creator(skipped_tests, 'd:', etree.parse(
    #     r'd:\10_Development\Python\TL_Creater\DataBase\TestLists\System_Behav_at_UnderVoltage_HW6_28FL\System_Behaviour_Undervoltage_HW6.xml'))
    #===========================================================================
    print (
        XmlParser.delete_failedtest(
            r'd:\temp\ISC_Sensor_Emulation_Unknown_XmlReport.xml',
            listofFailed,
            r'd:\temp\ISC_Sensor_Emulation_Unknown_XmlReport.xml'))
