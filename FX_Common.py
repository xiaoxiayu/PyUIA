import os
import platform
import winreg
import win32api, win32con

def FX_CloseProcess(pid):
    if platform.system() == 'Windows':
        os.popen('taskkill /F /PID %d' % pid)
    else:
        os.kill(pid, 0)


def FX_Exit():
    pid = os.getpid()
    FX_CloseProcess(pid)


def FX_GetDefaultEmailClient():
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, \
                              'mailto\\shell\\open\\command', \
                              0, \
                              win32con.KEY_READ)
    client_str = win32api.RegQueryValue(key, '')
    if client_str.find('OUTLOOK') != -1:
        return 'OUTLOOK'
    return 'FX_UNKNOW'


    
