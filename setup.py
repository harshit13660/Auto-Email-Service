import sys
from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR=os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY']=os.path.join(PYTHON_INSTALL_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY']=os.path.join(PYTHON_INSTALL_DIR,'tcl','tk8.6')

include_files=[(os.path.join(PYTHON_INSTALL_DIR,'DLLs','tk86t.dll'),os.path.join('lib','tk86.dll')),
               (os.path.join(PYTHON_INSTALL_DIR,'DLLs','tcl86t.dll'),os.path.join('lib','tcl86.dll')),"icon_img.ico"]

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables=[Executable('auto.py',base=base,icon="icon_img.ico",shortcut_name='Email-Certificate',shortcut_dir="DesktopFolder")]

setup(  name = "Aut0-Email",
        version = "1.0",
        description = "Auto Send Email",
        options = {"build_exe": {'packages':{"tkinter","threading","PIL"},"include_files":include_files}},
        executables = executables  )