# A simple setup script to create an executable using cx_freeze. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# Run the build process by running the command 'python setup.py bdist_msi'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application and installer.

from cx_Freeze import setup, Executable
import os
import sys
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = "c:\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "c:\\Python36\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
	
if not os.path.exists('Config'):
    os.makedirs('Config')

setup(name='CoFW WatchDog',
      version ='1.1',
      description='Co Fw WatchDog',
      options={"build_exe": {"includes":["numpy","cv2","matplotlib","WatchDog","lxml.etree","lxml._elementpath","pyautogui","numpy.lib.format"],
      'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
			os.path.dirname(os.path.realpath(__file__))+'\\Config',
			os.path.dirname(os.path.realpath(__file__))+'\\Doku'],"packages": ["numpy"]}},
      executables = [Executable("Starter.py",base=base)])