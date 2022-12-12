#This is script for build and deploy our game

import sys
from cx_Freeze import setup, Executable


exe = {"packages": ["os","sys","random","math","pygame","sys"],"excludes": ["tkinter"]}

build = dict(include_files = ['Asset/','sound effect/'])

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Demon's Tower",
    options = dict(build_exe = build),
    executables=[Executable("main.py", base=base,shortcut_name = "Demon's Tower",shortcut_dir="DesktopFolder")],
)