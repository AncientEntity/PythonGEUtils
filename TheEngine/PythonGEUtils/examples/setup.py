import sys, os
from cx_Freeze import setup, Executable

__version__ = "1.1.0"

include_files = []
excludes = []
packages = ["PythonGEUtils","PythonGEUtils.engine"]

setup(
    name = "Test",
    description='App Description',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("FlappyBirdTest.py",base="Win32GUI")]
)
