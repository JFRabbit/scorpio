import win32api
import win32con


def ctrl_v():
    win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    win32api.keybd_event(86, 0, 0, 0)  # V
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)


def ent():
    win32api.keybd_event(13, 0, 0, 0)  # Enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)