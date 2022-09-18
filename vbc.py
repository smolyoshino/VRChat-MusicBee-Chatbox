from re import A
from pythonosc.udp_client import SimpleUDPClient
import win32gui
import win32process
import psutil
import ctypes
import time

mbName = ""
a = ["", True]
b = [f"{mbName}", True]
ip = "127.0.0.1"
port = 9000
client = SimpleUDPClient(ip, port)
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
def getProcessIDByName():
    mb_pids = []
    process_name = "MusicBee.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            mb_pids.append(proc.pid)

    return mb_pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def getWindowTitleByHandle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def getmbHandle():
    pids = getProcessIDByName()

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd


mb_handle = getmbHandle()

while(True):
    if(getWindowTitleByHandle(mb_handle) == "MusicBee"):
        client.send_message("/chatbox/input", a)
        print(a)
        print('play music')
    else:
        if(getWindowTitleByHandle(mb_handle) != mbName):
            mbName = "Playing: "
            mbName += getWindowTitleByHandle(mb_handle)
            b[0] = f"{mbName}"
            size = len(mbName)
            b[0] = mbName[:size - 11]
            client.send_message("/chatbox/input", b)
            print("sent!")
            # print(b[0])
        else:
            client.send_message("/chatbox/input", b)
            print("we already had it but sending it again :D")
            # print(b[0])
    time.sleep(5)
