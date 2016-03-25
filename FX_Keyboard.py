# -*- coding:utf-8 -*-

import time
from ctypes import *
import win32gui, win32con

PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),      #virtual-key code
                ("wScan", c_ushort),    #hardware scan code
                ("dwFlags", c_ulong),   #keystroke
                ("time", c_ulong),      #time stamp
                ("dwExtraInfo", PUL)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time",c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class Input_I(Union):
    _fields_ = [("mi", MouseInput),
                ("ki", KeyBdInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


class SendKey(object):
    def __init__(self):
        self.EXTENDED_KEYS = [win32con.VK_LEFT, win32con.VK_DOWN, win32con.VK_UP, win32con.VK_RIGHT]

    def generateVirtualKey(self, key):
        keyMap = {
            "left": win32con.VK_LEFT,
            "down": win32con.VK_DOWN,
            "tab" : win32con.VK_TAB,
            "up": win32con.VK_UP,
            "right": win32con.VK_RIGHT,
            "ctrl" : win32con.VK_CONTROL,
            "esc" : win32con.VK_ESCAPE,
            "enter" : win32con.VK_RETURN,
            "alt" : win32con.VK_MENU,
            ";:" : 0xBA,
            "\\|" : 0xDC,
            ".>" : 0xBE,
            "-_" : 0xBD,
            "win" : 0x5B,
            "shift" : win32con.VK_SHIFT
        }
        if key in keyMap:
            return keyMap[key]
        else:
            return ord(key.upper())

    def sendKey(self, key, keyStroke):
        if key == ':':
            self.sendKey('shift', 'down')
            self.sendKey(';:', keyStroke)
            self.sendKey('shift', 'up')
            return
        elif key == ';':
            self.sendKey(';:', keyStroke)
            return

        elif key == '\\':
            self.sendKey('\\|', keyStroke)
            return
        elif key == '|':
            self.sendKey('shift', 'down')
            self.sendKey('\\|', keyStroke)
            self.sendKey('shift', 'up')
            return
        elif key == '.':
            self.sendKey('.>', keyStroke)
            return
        elif key == '>':
            self.sendKey('shift', 'down')
            self.sendKey('.>', keyStroke)
            self.sendKey('shift', 'up')
            return
        elif key == '-':
            self.sendKey('-_', keyStroke)
            return
        elif key == '_':
            self.sendKey('shift', 'down')
            self.sendKey('-_', keyStroke)
            self.sendKey('shift', 'up')
            return
        virtualKey = self.generateVirtualKey(key)
        
        scanCode = windll.user32.MapVirtualKeyA(virtualKey, 0)
        dwFlags = win32con.KEYEVENTF_EXTENDEDKEY if virtualKey in self.EXTENDED_KEYS else 0        

        if keyStroke == 'down':
            pass
        elif keyStroke == 'up':
            if virtualKey > 254:
                dwFlags = 0x0004 #KEYEVENTF_UNICODE
            else:
                dwFlags = dwFlags | win32con.KEYEVENTF_KEYUP
        else:
            print(u'keyStroke Error')

        if virtualKey > 254:
            scanCode = virtualKey
            virtualKey = 0

        dwExtraInfo = c_ulong(0)

        ii_ = Input_I()
        ii_.ki = KeyBdInput(virtualKey, scanCode, dwFlags, 0, pointer(dwExtraInfo))

        nInputs = 1
        pInputs = Input(win32con.INPUT_KEYBOARD, ii_)
        
        windll.user32.SendInput(nInputs, pointer(pInputs), sizeof(pInputs))

##import win32clipboard as wincb
##import win32con
## 
##wincb.OpenClipboard()
##wincb.EmptyClipboard()
##wincb.SetClipboardData(win32con.CF_TEXT, b"Hello World!")  #复制文本内容到剪贴板，系统后台会返回内存地址
##print(wincb.GetClipboardData(win32con.CF_TEXT).decode('utf8') ) #'Hello World!'
##wincb.CloseClipboard()
##if __name__ == '__main__':
####    print(StrToHex('中'))
####    pppppp
##    time.sleep(2)
##    sk = SendKey()
##    sk.sendKey('中', 'down')
##    time.sleep(0.1)
##    sk.sendKey('中', 'up')
##    sk.sendKey('文', 'down')
##    time.sleep(0.1)
##    sk.sendKey('文', 'up')


