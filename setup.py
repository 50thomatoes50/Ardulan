import sys
from cx_Freeze import setup, Executable

"""includefiles=["ardulan.ico",
              "html/favicon.ico",
              "html/index_footer.html",
              "html/index_header.html",
              "html/mega.js",
              "html/test.html",
              "html/img/Arduino_MEGA_2560-Rev3_breadboard.svg"]"""
includefiles=[]
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": [""], 'init_script':'Console', 'include_files':includefiles}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
"""if sys.platform == "win32":
    base = "Win32GUI"""

setup(  name = "Ardulan",
        version = "0.1",
        description = "Ardulan server",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base,icon = "ardulan.ico" )])