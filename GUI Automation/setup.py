from cx_Freeze import setup, Executable
setup(name='TOOL11',
      version ='0.1',
      description='Easily find best float combination',
      options={"build_exe": {"includes":["Numpy","Cv2","Matplotlib","WatchDog","_elementpath"]}},
      executables = [Executable("main.py")])