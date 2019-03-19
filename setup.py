#setup.py
import sys, os
from cx_Freeze import setup, Executable

__version__ = "1.0.0"

excludes = ["tkinter"]
packages = ["os"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Pong",
    description='Simple Pong game made in python with pygame',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("main.py", base=base)]
)