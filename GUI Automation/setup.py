from cx_Freeze import setup, Executable
setup(name='TOOL11',
      version ='0.1',
      description='Co Fw WatchDog',
      options={"build_exe": {"includes":["Numpy","Cv2","Matplotlib","WatchDog","lxml.etree","lxml._elementpath"]}},
      executables = [Executable("Starter.py")])