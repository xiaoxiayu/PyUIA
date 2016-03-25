#coding=utf-8
import ctypes
from ctypes import *
import win32api, win32con, win32gui, win32process
from comtypes import GUID  
from comtypes.client import CreateObject, GetModule
import time
import random
import win32clipboard
from FX_Keyboard import *


UIAutomationClient = GetModule("UIAutomationCore.dll")  
IUIAutomation = CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}", interface=UIAutomationClient.IUIAutomation)

ELEMENT_CONTROL_TYPE = {
    50040 : 'UIA_AppBarControlTypeId',
    50000 : 'UIA_ButtonControlTypeId',
    50001 : 'UIA_CalendarControlTypeId',
    50002 : 'UIA_CheckBoxControlTypeId',
    50003 : 'UIA_ComboBoxControlTypeId',
    50025 : 'UIA_CustomControlTypeId',
    50029 : 'UIA_DataItemControlTypeId',
    50030 : 'UIA_DocumentControlTypeId',
    50004 : 'UIA_EditControlTypeId',
    50026 : 'UIA_GroupControlTypeId',
    50034 : 'UIA_HeaderControlTypeId',
    50035 : 'UIA_HeaderItemControlTypeId',
    50005 : 'UIA_HyperlinkControlTypeId',
    50006 : 'UIA_ImageControlTypeId',
    50008 : 'UIA_ListControlTypeId',
    50007 : 'UIA_ListItemControlTypeId',
    50010 : 'UIA_MenuBarControlTypeId',
    50009 : 'UIA_MenuControlTypeId',
    50011 : 'UIA_MenuItemControlTypeId',
    50033 : 'UIA_PaneControlTypeId',
    50012 : 'UIA_ProgressBarControlTypeId',
    50013 : 'UIA_RadioButtonControlTypeId',
    50014 : 'UIA_ScrollBarControlTypeId',
    50039 : 'UIA_SemanticZoomControlTypeId',
    50038 : 'UIA_SeparatorControlTypeId',
    50015 : 'UIA_SliderControlTypeId',
    50016 : 'UIA_SpinnerControlTypeId',
    50031 : 'UIA_SplitButtonControlTypeId',
    50017 : 'UIA_StatusBarControlTypeId',
    50018 : 'UIA_TabControlTypeId',
    50019 : 'UIA_TabItemControlTypeId',
    50036 : 'UIA_TableControlTypeId',
    50020 : 'UIA_TextControlTypeId',
    50027 : 'UIA_ThumbControlTypeId',
    50037 : 'UIA_TitleBarControlTypeId',
    50021 : 'UIA_ToolBarControlTypeId',
    50022 : 'UIA_ToolTipControlTypeId',
    50023 : 'UIA_TreeControlTypeId',
    50024 : 'UIA_TreeItemControlTypeId',
    50032 : 'UIA_WindowControlTypeId'    
    }

class FX_RECT:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

##print(UIAutomationClient.IUIAutomationValuePattern)
class FX_CONDITION_TYPE:
    def __init__(self):
        self.TrueCondition = 'True'
        self.FalseCondition = 'False'
        self.PropertyCondition = 'Property'

class FX_ELEMENT_INFO:
    def __init__(self):
##        self.FXID = -1
        self.FXElement = None
        self.ID = ''
        self.ClassName = ''
        self.Name = ''
        self.Type = ''
        self.AccessKey = ''
        self.Rect = None

        self.Father = None # ELEMENT_INFO
        self.Children = None # FX_ElementArray

class FX_PROPERTY_IDERTIFIER:
    def __init__(self):
        self.ClassName = UIAutomationClient.UIA_ClassNamePropertyId
        self.Name = UIAutomationClient.UIA_NamePropertyId

class FX_TREE_SCOPE:
    def __init__(self):
        # The scope includes the element itself.
        self.Element = UIAutomationClient.TreeScope_Element

        # The scope includes children of the element.
        self.Children = UIAutomationClient.TreeScope_Children

        # The scope includes children and more distant descendants of the element.
        self.Descendants = UIAutomationClient.TreeScope_Descendants
        
        # The scope includes the parent of the element.
        self.Parent = UIAutomationClient.TreeScope_Parent
        
        # The scope includes the parent and more distant ancestors of the element.
        self.Ancestors = UIAutomationClient.TreeScope_Ancestors
        
        # The scope includes the element and all its descendants.
        # This flag is a combination of the TreeScope_Element and TreeScope_Descendants values.
        self.Subtree = UIAutomationClient.TreeScope_Subtree


class FX_PATTERN_DEF:
    Value = UIAutomationClient.UIA_ValuePatternId
    Text = UIAutomationClient.UIA_TextPatternId
    SelectionItem = UIAutomationClient.UIA_SelectionItemPatternId
    LegacyIAccessible = UIAutomationClient.UIA_LegacyIAccessiblePatternId

    InterfaceMap = {UIAutomationClient.UIA_ValuePatternId : UIAutomationClient.IUIAutomationValuePattern,\
                    UIAutomationClient.UIA_TextPatternId : UIAutomationClient.IUIAutomationTextPattern, \
                    UIAutomationClient.UIA_SelectionItemPatternId : UIAutomationClient.IUIAutomationSelectionItemPattern, \
                    UIAutomationClient.UIA_LegacyIAccessiblePatternId : UIAutomationClient.IUIAutomationLegacyIAccessiblePattern}

    def __init__(self):
        pass
    

class FX_Condition:
    def __init__(self):
        pass

    def CreateTrueCondition(self):
        return IUIAutomation.CreateTrueCondition()

    def CreateFalseCondition(self):
        return IUIAutomation.CreateFalseCondition()

    def CreateClassNamePropertyCondition(self, classname):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ClassNamePropertyId,\
                                                       classname,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateMenuItemTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_MenuItemControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateHyperlinkTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_HyperlinkControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateImageTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_ImageControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateButtonTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_ButtonControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateTableTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_TableControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateCheckBoxControlTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_CheckBoxControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)

    def CreateEditControlTypeCondition(self):
        return IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_EditControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)
        

def FX_GetRootElement():
    return FX_Element(IUIAutomation.GetRootElement())

def FX_GetFocusedElement():
    return FX_Element(IUIAutomation.GetFocusedElement())

def FX_CreateCondition(condition_type, identifier=UIAutomationClient.UIA_ClassNamePropertyId,\
                       value='', condition_flags=UIAutomationClient.PropertyConditionFlags_None):
    if condition_type == 'True':
        return IUIAutomation.CreateTrueCondition()
    elif condition_type == 'Property':
        return IUIAutomation.CreatePropertyConditionEx(identifier, value, condition_flags)


def FX_CreateElementInfo(element, element_id, class_name, name, ele_type, access_key, rect):
    element_info = FX_ELEMENT_INFO()
    element_info.element = element
    element_info.ClassName = class_name
    element_info.Name = name
    element_info.ProcessId = element_id
    element_info.Type = ele_type
    element_info.AccessKey = access_key
    element_info.Rect = rect
    return element_info

def FX_GetElementInfo(element):
    element_info = FX_ELEMENT_INFO()
    element_info.element = element
    element_info.ClassName = element.CurrentClassName
    element_info.Name = element.CurrentName
    element_info.ProcessId = element.CurrentProcessId
    element_info.Type = element.CurrentControlType
    element_info.Rect = element.CurrentBoundingRectangle
    element_info.AccessKey = element.CurrentAccessKey
    return element_info


    
def FX_GetElementFromPoint(x, y):
    pt = ctypes.wintypes.POINT(c_long(int(x)), c_long(int(y)))
    return FX_Element(IUIAutomation.ElementFromPoint(pt))

def FX_GetSupportPattern(element):
    return IUIAutomation.PollForPotentialSupportedPatterns(pageview_elm_child)

def FX_GetCurrentPattern(element, pattern_type):
    pattern = element.GetCurrentPattern(pattern_type)
    return cast(pattern, POINTER(pattern_type))

def FX_SetCursorPos(element):
    pos = element.GetClickablePoint()
    if pos[1] == False:
        return False
    win32api.SetCursorPos((pos[0].x, pos[0].y))
    return True

def FX_MouseLClick(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def FX_MouseRClick(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def FX_MouseLDown(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)

def FX_MouseLUp(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)

def FX_MouseMove(x, y):
    win32api.SetCursorPos((int(x),int(y)))

def FX_MouseScroll(i):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, i,0)

def FX_GetCursorPos():
    return win32api.GetCursorPos()


def FX_GetElementFromWindow(FXWindow):
    try:
        ele = FX_Element(IUIAutomation.ElementFromHandle(FXWindow.GetWin32Window()))
        return ele
    except:
        return None

def FX_CreateID():
    return str(-random.randint(1, 1001))

def FX_PrintElementInfo(element):
    print('%s: %s: %s' % (element.GetID(), \
                            element.GetClassName(), \
                            element.GetName()))

def FX_GetElementInfo(element):
    info = FX_ELEMENT_INFO()
    info.ID = element.GetID()
    info.ClassName = element.GetClassName()
    info.Name = element.GetName()
    info.Type = element.GetType()
    info.Rect = element.GetRect()
    info.AccessKey = element.GetAccessKey()
    return info

def FX_KeybdPress(virtual_key_code):
    win32api.keybd_event(virtual_key_code, 0, 0, 0)

def FX_KeybdRelease(virtual_key_code):
    win32api.keybd_event(virtual_key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

def FX_SendKey(s):
    sk = SendKey()
    for c in s:
        sk.sendKey(c, 'down')
        time.sleep(0.1)
        sk.sendKey(c, 'up')

def FX_SendString(s, t=0.01):
    sk = SendKey()
    for c in s:
        sk.sendKey(c, 'down')
        time.sleep(t)
        sk.sendKey(c, 'up')


def FocusChangeCallBack(cache_request, event_id):
    print('FocusChangeCallBack')
    pass

def RegFocusChangeCallBack():
    fc_callback = CFUNCTYPE(HRESULT, \
                                POINTER(UIAutomationClient.IUIAutomationCacheRequest), \
                                POINTER(UIAutomationClient.IUIAutomationFocusChangedEventHandler))
    pDownTextInfoHandle = fc_callback(FocusChangeCallBack);
     
    IUIAutomation.AddFocusChangedEventHandler(pDownTextInfoHandle);



class FX_CacheRequest:
    def __init__(self):
         self.cache_request = IUIAutomation.CreateCacheRequest()
         print(self.cache_request.AutomationElementMode)

    def AddProperty(self):
        self.cache_request = self.cache_request.AddProperty(UIAutomationClient.UIA_ClassNamePropertyId)
        print(self.cache_request)

    def get(self):
        return self.cache_request

def FX_CompareElements(ele0, ele1):
    return IUIAutomation.CompareElements(ele0.GetUIAElement(), ele1.GetUIAElement())

def FX_FindallCacheElement(cache):
    print(cache)
    a = IUIAutomation.GetRootElementBuildCache(cache.get())
    print(a)
    print(a.CurrentName)
    pass

def FX_CreateTreeWalker():
    condition = FX_Condition()
    return FX_TreeWalker(IUIAutomation.CreateTreeWalker(condition.CreateTrueCondition()))

def FX_GetParent(FXElement):
    tree_walker = FX_CreateTreeWalker()
    return tree_walker.GetParent(FXElement)

def FX_GetWindowRect(Win32Window):
    return win32gui.GetWindowRect(Win32Window)

def FX_GetScreenWidth():
    return win32api.GetSystemMetrics(0)

def FX_GetScreenHeight():
    return win32api.GetSystemMetrics(1)

class FX_TreeWalker:
    def __init__(self, uia_walker):
        self.walker = uia_walker

    def GetFirstChild(self, FXElement):
        uiaelement = self.walker.GetFirstChildElement(FXElement.GetWin32Element())
        if uiaelement:
            return FX_Element(uiaelement)
        return None

    def GetParent(self, FXElement):
        uiaelement = self.walker.GetParentElement(FXElement.GetWin32Element())
        if uiaelement:
            return FX_Element(uiaelement)
        return None

    def GetNormalize(self, FXElement):
        uiaelement = self.walker.NormalizeElement(FXElement.GetWin32Element())
        if uiaelement:
            return FX_Element(uiaelement)
        return None

    def GetNextSibling(self, FXElement):
        uiaelement = self.walker.GetNextSiblingElement(FXElement.GetWin32Element())
        if uiaelement:
            return FX_Element(uiaelement)
        return None

    def GetChildrenArray(self, FXElement):
        children_arr = []
        ele_1 = self.GetFirstChild(FXElement)
        if ele_1 == None:
            return None
        children_arr.append(ele_1)

        while True:
            ele_1 = self.GetNextSibling(ele_1)
            if ele_1 == None:
                break
            children_arr.append(ele_1)
        return children_arr

def FX_CreateElementFromPosition(pos):
    ele = FX_Element(None)
    ele.type = -1
    ele.SetPosition(pos[0], pos[1])
    return ele


class FX_Pattern:
    def __init__(self, pattern_point):
        self.pattern = pattern_point

    @property
    def IsSelected(self):
        return self.pattern.CurrentIsSelected

    @property
    def LegacyIAccessibleValue(self):
        return self.pattern.CurrentValue

    @property
    def LegacyIAccessibleName(self):
        return self.pattern.CurrnetName

    @property
    def LegacyIAccessibleRole(self):
        return self.pattern.CurrentRole

    @property
    def LegacyIAccessibleChildId(self):
        return self.pattern.CurrentChildId

    @property
    def LegacyIAccessibleDefaultAction(self):
        return self.pattern.CurrentDefaultAction

    @property
    def LegacyIAccessibleDescription(self):
        return self.pattern.CurrentDescription

    @property
    def Value(self):
        return self.pattern.CurrentValue

    @Value.setter
    def Value(self, val):
        self.pattern.SetValue(val)

    @property
    def ValueIsReadOnly(self):
        return self.pattern.CurrentIsReadOnly
    
class FX_Element:
    def __init__(self, uia_element):
        self.element = uia_element
        self.pattern = None
        self.posX = -1
        self.posY = -1
        self._type = -1

    def get(self):
        return self.element

    def SetPosition(self, x, y):
        self.element = None
        self.posX = x
        self.posY = y
        

    def GetWin32Element(self):
        return self.element

    def GetClickablePoint(self):
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return (-1, -1)
        return (pos[0].x, pos[0].y)

    def GetName(self):
        try:
            return self.element.CurrentName
        except Exception as e:
            if str(e).find('AttributeError') != -1:
                return 'FXUnknownName'
            return 'FXError'
            

    def GetClassName(self):
        return self.element.CurrentClassName

    def GetFrameworkId(self):
        return self.element.CurrentFrameworkId

    def GetType(self):
        if self.element == None:
            return self._type
        return self.element.CurrentControlType

    def GetID(self):
##        try:
        return self.element.CurrentAutomationId
##        except:
##            print('------------')
##            print(self.element)
##            print(self.element.CurrentName)
##            print(self.element.CurrentClassName)
##            print('------------')
##            fffff

    def GetRuntimeId(self):
        try:
            return self.element.GetRuntimeId()
        except:
            return None

    def GetRect(self):
        return self.element.CurrentBoundingRectangle

    def GetAccessKey(self):
        return self.element.CurrentAccessKey

    def GetCacheParent(self):
        t = self.element.GetCachedPropertyValue(UIAutomationClient.UIA_ClassNamePropertyId)
        return FX_Element(t)

    def GetAncestors(self):
        condition = FX_Condition()
        ele_parent = self.element.FindAll(UIAutomationClient.TreeScope_Parent, condition.CreateTrueCondition())
        return FX_ElementArray(ele_parent)

    def GetParents(self):
        condition = FX_Condition()
        ele_parent = self.element.FindAll(UIAutomationClient.TreeScope_Parent, condition.CreateTrueCondition())
        return FX_ElementArray(ele_parent)

    def GetNativeWindowHandle(self):
        return self.element.CurrentNativeWindowHandle

    def GetChildCount(self):
        condition = FX_Condition()
        element_child = self.element.FindAll(UIAutomationClient.TreeScope_Children, condition.CreateTrueCondition())
        return element_child.GetCount()

    def GetDescendants(self, condition=None):
        if condition == None:
            find_condition = FX_Condition()
            condition = find_condition.CreateTrueCondition()

        element_childs = self.element.FindAll(UIAutomationClient.TreeScope_Descendants, condition)
        return FX_ElementArray(element_childs)
        
        #add by qinjuan
    def GetNextSiblingEle(self):
        tree_walker = FX_CreateTreeWalker()
        return tree_walker.GetNextSibling(self)

    def GetFirstChild(self):
        tree_walker = FX_CreateTreeWalker()
        return tree_walker.GetFirstChild(self)

    def GetPattern(self, pattern_type):
        self.pattern = self.element.GetCurrentPattern(pattern_type)
        if self.pattern:
            return FX_Pattern(cast(self.pattern, POINTER(FX_PATTERN_DEF.InterfaceMap[pattern_type])))
        return None

    def GetPotentialSupportedPatterns(self):
        support_pattern = IUIAutomation.PollForPotentialSupportedPatterns(self.element)
        return support_pattern

    def GetValuePattern(self):
        return self.GetPattern(FX_PATTERN_DEF.Value)

    def GetLegacyIaccessiblePattern(self):
        return self.GetPattern(FX_PATTERN_DEF.LegacyIAccessible)

    def FindAll(self, tree_scope, condition):
        try:
            element_array = self.element.FindAll(tree_scope, condition)
            return FX_ElementArray(element_array)
        except:
            return None

    def MouseLButtonClick(self):
        if self.element == None:
            win32api.SetCursorPos((self.posX, self.posY))
            FX_MouseLClick(self.posX, self.posY)
            return True
        try:
            self.element.SetFocus()
        except:
            print('Focus error')
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return False
        win32api.SetCursorPos((pos[0].x, pos[0].y))
        #pos = win32api.GetCursorPos()
        FX_MouseLClick(pos[0].x, pos[0].y)
        return True

    def MouseLButtonDown(self):
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return False
        win32api.SetCursorPos((pos[0].x, pos[0].y))
        #pos = win32api.GetCursorPos()
        FX_MouseLDown(pos[0].x, pos[0].y)
        return True

    def MouseMove(self):
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return False
        win32api.SetCursorPos((pos[0].x, pos[0].y))
        return True
##
##    def MouseLButtonUp(self):
##        pos = self.element.GetClickablePoint()
##        if pos[1] == False:
##            return False
##        win32api.SetCursorPos((pos[0].x, pos[0].y))
##        #pos = win32api.GetCursorPos()
##        FX_MouseLDown(pos[0].x, pos[0].y)
##        return True

    def SetCursorPos(self):
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return False
        win32api.SetCursorPos((pos[0].x, pos[0].y))
        return True

    def SetFocus(self):
        self.element.SetFocus()

    def IsEnable(self):
        return self.element.CurrentIsEnabled

    def IsVisible(self):
        return self.element.CurrentIsOffscreen 

    def IsControlElement(self):
        return self.element.CurrentIsControlElement

    def IsKeyboardFocusable(self):
        return self.element.CurrentIsKeyboardFocusable

    def IsOffscreen(self):
        return self.element.CurrentIsOffscreen

    def IsPassword(self):
        return self.element.CurrentIsPassword

    def ItemStatus(self):
        return self.element.CurrentItemStatus

    def ItemType(self):
        return self.element.CurrentItemType

    def LabeledBy(self):
        try:
            return self.element.CurrentLabeledBy
        except:
            return 'ERROR'

    def LocalizedControlType(self):
        return self.element.CurrentLocalizedControlType

    def NativeWindowHandle(self):
        return self.element.CurrentNativeWindowHandle

    @property
    def position(self):
        pos = self.element.GetClickablePoint()
        if pos[1] == False:
            return (-1, -1)
        return (pos[0].x, pos[0].y)

    @property
    def type(self):
        return self.element.CurrentItemType

    @type.setter
    def type(self, type_id):
        if self.element == None:
            self._type = type_id
            return
        self.element.CurrentItemType = type_id

    
class FX_ElementArray:
    def __init__(self, uia_element_array):
        self.element_array = uia_element_array

    def GetElementByIndex(self, index):
        return FX_Element(self.element_array.GetElement(index))

    def GetCount(self):
        return self.element_array.Length

    @property
    def count(self):
        return self.element_array.Length

class FX_ElementFinder:
    def __init__(self, root):
        self.current_ele = root
        self.tree_scope = None
        self.control_type = UIAutomationClient.UIA_MenuItemControlTypeId
        self.fx_element = FX_Element(self.current_ele)

    def SetTreeScope(self, tree_scope):
        self.treee_scope = tree_scope

    def SetCondition(self, condition):
        self.condition = condition


    def FindFirst(self, tree_scope, condition):
        return self.current_ele.FindFirst(tree_scope, condition)

    def FindAll(self, tree_scope, condition):
        return self.current_ele.FindAll(tree_scope, condition)

    def FindElementByClassName(self, class_name):
        element_array = self.current_ele.FindAll(UIAutomationClient.TreeScope_Descendants, self.condition)
        return self.GetElementByClassName(element_array, class_name)

    def FindElementArrayByClassName(self, class_name):
        cnd2 = IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ClassNamePropertyId,\
                                                       class_name,\
                                                       UIAutomationClient.PropertyConditionFlags_None)
        element_array = self.current_ele.FindAll(UIAutomationClient.TreeScope_Descendants, cnd2)
        return element_array

    def FindElementArrayByName(self, class_name):
        cnd2 = IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_NamePropertyId,\
                                                       class_name,\
                                                       UIAutomationClient.PropertyConditionFlags_None)
        element_array = self.current_ele.FindAll(UIAutomationClient.TreeScope_Descendants, cnd2)
        return element_array

    def FindElementArrayByControlType(self, control_type):
        cnd2 = IUIAutomation.CreatePropertyConditionEx(UIAutomationClient.UIA_ControlTypePropertyId,\
                                                       UIAutomationClient.UIA_MenuItemControlTypeId,\
                                                       UIAutomationClient.PropertyConditionFlags_None)
        self.current_ele.FindAll(UIAutomationClient.TreeScope_Descendants, cnd2)
        pass
    
    def GetElement(self, index):
        return element_array.GetElement(index)

    def GetElementByName(self, element_array, name):
        element_count = element_array.Length
        for i in range(0, element_count):
            element = element_array.GetElement(i)
            if element.CurrentName == name:
                self.current_ele = element
                return FX_Element(element)
        return None

    def GetElementByClassName(self, element_array, class_name):
        element_count = element_array.Length
        for i in range(0, element_count):
            element = element_array.GetElement(i)
            if element.CurrentClassName == class_name:
                self.current_ele = element
                return FX_Element(element)
        return None

    def FindChildElementByName(self, tree_scope, condition, class_name):
        element_array = FX_FindAll(element, tree_scope, condition)
        return FX_GetElementByName(element_array, class_name)

    def FindChildElementByClassName(self, tree_scope, condition, class_name):
        element_array = FX_FindAll(element, tree_scope, condition)
        print(element_array)
        return FX_GetElementByClassName(element_array, class_name)


class FX_WINDOW_INFO:
    def __init__(self):
        # FX_Window HND
        self.Win32Window = ''
        self.ProcessID = ''
        self.ThreadID = ''
        self.Title = ''

        
##def FX_CompareWindow(window0, window1):
##    if (window0.Window.GetWin32Window() != window1.Window.GetWin32Window()):
##        if (window0.ProcessID != window1.ProcessID):
##            return 1
##        else:
##            return -1    
##    return 0

##def FX_CloseWindow(window):
##    win32gui.CloseWindow(window.GetWin32Window())
##
##def FX_DestoryWindow(window):
##    win32gui.DestroyWindow(window.GetWin32Window())
##
##    
def FX_GetForegroundWindow():
    window_info = FX_WINDOW_INFO()

    window_info.Win32Window = win32gui.GetForegroundWindow()
    
    thread_process = win32process.GetWindowThreadProcessId(window_info.Win32Window)
    
    window_info.ProcessID = thread_process[1]
    window_info.ThreadID = thread_process[0]
    window_info.Title = win32gui.GetWindowText(window_info.Win32Window)
    return FX_Window(window_info)

def FX_CloseWindow(FXWindow):
    win32gui.SendMessage(FXWindow.win32window, win32con.WM_CLOSE)

def FX_FindWindow(window_title):
    pass

def FX_SetForegroundWindow(FXWindow):
    try:
        win32gui.SetForegroundWindow(FXWindow.GetWin32Window())
        return True
    except:
        return False

def FX_ShowWindow(Win32Window):
    win32gui.SetForegroundWindow(Win32Window) 
    win32gui.SetWindowPos(Win32Window, \
                          win32con.HWND_TOP, \
                          0,0,0,0, \
                          win32con.SWP_SHOWWINDOW)
    
def FX_ShowWindowMax(Win32Window):
    win32gui.SetForegroundWindow(Win32Window) 
##    win32gui.SetWindowPos(Win32Window, \
##                          win32con.HWND_TOP, \
##                          0,0,0,0, \
##                          win32con.SWP_SHOWWINDOW)
    win32gui.ShowWindow(Win32Window, win32con.SW_MAXIMIZE)

def FX_GetWindowTitle(FXWindow):
    return win32gui.GetWindowText(FXWindow.GetWin32Window())

def FX_IsWindowEnabled(Win32Window):
    return win32gui.IsWindowEnabled(Win32Window)

def FX_CreateWindowFromElement(FXElement):
    win_info = FX_WINDOW_INFO()
    win_info.Win32Window = FXElement.GetNativeWindowHandle()
    if win_info.Win32Window == 0:
        return None
    thread_process = win32process.GetWindowThreadProcessId(win_info.Win32Window)
    
    win_info.ProcessID = thread_process[1]
    win_info.ThreadID = thread_process[0]
    win_info.Title = win32gui.GetWindowText(win_info.Win32Window)
    return FX_Window(win_info, FXElement)
    
class FX_Window:
    def __init__(self, FXWindow, FXElement=None):
        self.FXWindow = FXWindow
        self.ProcessID = ''
        self.ThreadID = ''
        self.FXElement = FXElement

    def GetFXElement(self):
        return self.FXElement

    def GetWindowText(self):
        return win32gui.GetWindowText(self.Window)

    def GetWin32Window(self):
        return self.FXWindow.Win32Window

    def GetProcessID(self):
        return self.FXWindow.ProcessID

    def GetThreadID(self):
        return self.FXWindow.ThreadID

    def GetTitle(self):
        return self.FXWindow.Title

    def GetWindowElement(self):
        ele = FX_Element(IUIAutomation.ElementFromHandle(self.FXWindow.Win32Window))
        return ele

    def FindWindowByClassName(self, class_name):
        win_info = FX_WINDOW_INFO()
        win_info.Win32Window = win32gui.FindWindowEx(None, None, class_name, None)
        print(win_info.Win32Window)
        if win_info.Win32Window == 0:
            return None
        thread_process = win32process.GetWindowThreadProcessId(win_info.Win32Window)
        
        win_info.ProcessID = thread_process[1]
        win_info.ThreadID = thread_process[0]
        win_info.Title = win32gui.GetWindowText(win_info.Win32Window)
        return FX_Window(win_info)

    def FindWindowByName(self, title_name):
        win_info = FX_WINDOW_INFO()
        win_info.Win32Window = win32gui.FindWindowEx(None, None, None, title_name)
        if win_info.Win32Window == 0:
            return None
        thread_process = win32process.GetWindowThreadProcessId(win_info.Win32Window)
        
        win_info.ProcessID = thread_process[1]
        win_info.ThreadID = thread_process[0]
        win_info.Title = win32gui.GetWindowText(win_info.Win32Window)
        return FX_Window(win_info)

    def GetForegroundWindow(self):
        win_info = FX_WINDOW_INFO()
        win_info.Window = win32gui.GetForegroundWindow()
        
        thread_process = win32process.GetWindowThreadProcessId(win_info.Window)
        
        self.ProcessID = thread_process[1]
        self.ThreadID = thread_process[0]
        win_info.Title = win32gui.GetWindowText(win_info.Win32Window)
        return FX_Window(win_info)

    def Close(self):
        win32gui.SendMessage(self.FXWindow.Win32Window, win32con.WM_CLOSE)

    @property
    def title(self):
        return self.FXWindow.Title

    @property
    def processid(self):
        return self.FXWindow.ProcessID

    @property
    def win32window(self):
        return self.FXWindow.Win32Window


class FX_ComboBox:
    def __init__(self, combobox_ele):
        self.ComboBox = combobox_ele
        self.ele_list = []
        self.tree_walker = FX_CreateTreeWalker()
        self.Init()


    def GetElements(self):
##        for ele in self.ele_list:
##            print(ele.GetName())
        return self.ele_list

    def SelectItem(self, item_index=0):
        list_item = self.GetListItems()
        if len(list_item) == 0 \
           or item_index < 0 \
           or item_index >= len(list_item):
            return
        ele = list_item[item_index]
        ele.MouseLButtonClick()

    def SelectItemByName(self, item_name=''):
        list_item = self.GetListItems()
        if len(list_item) == 0:
            return
        for ele in list_item:
            if ele.GetName() == item_name:
                ele.MouseLButtonClick()

    def GetListItems(self):
        self.OpenList()
        listitem_list = []
        for ele in self.ele_list:
            if ele.GetType() == 50007:
                listitem_list.append(ele)
        return listitem_list

    def OpenList(self):
        for ele in self.ele_list:
            # Button
            if ele.GetType() == 50000:
                ele.MouseLButtonClick()
                time.sleep(0.5)
                self.Init()

    def GetList(self, list_ele):
        ele_c = self.tree_walker.GetFirstChild(list_ele)
        if ele_c != None:
            self.ele_list.append(ele_c)
            while 1:
                ele_c = self.tree_walker.GetNextSibling(ele_c)
                if ele_c == None:
                    break
                self.ele_list.append(ele_c)
                        

    def Init(self):
        self.ele_list = []
        ele = self.tree_walker.GetFirstChild(self.ComboBox)
        if ele == None:
            return
        if ele.GetType() == 50008:
            self.GetList(ele)

        self.ele_list.append(ele)
        while 1:
            ele = self.tree_walker.GetNextSibling(ele)
            if ele == None:
                break
            if ele.GetType() == 50008:
                self.GetList(ele)
                
            self.ele_list.append(ele)

class FX_ListControl:
    def __init__(self, listcontrol_ele):
        self.ListControl = listcontrol_ele
        self.ele_list = []
        self.tree_walker = FX_CreateTreeWalker()
        self.Init()


    def GetListItems(self):
        return self.ele_list

    def SelectItem(self, item_index=0):
        if len(self.ele_list) == 0 \
           or item_index < 0 \
           or item_index >= len(self.ele_list):
            return
        ele = self.ele_list[item_index]
        ele.MouseLButtonClick()

    def SelectItemByName(self, item_name):
        print('Item lenght:%d' % len(self.ele_list))
        if len(self.ele_list) == 0:
            return
        for ele in self.ele_list:
            if ele.GetName() == item_name:
                ele.MouseLButtonClick()

    
    def Init(self):
        self.ele_list = []
        ele = self.tree_walker.GetFirstChild(self.ListControl)
        if ele == None:
            return
        self.ele_list.append(ele)
        while 1:
            ele = self.tree_walker.GetNextSibling(ele)
            if ele == None:
                break                
            self.ele_list.append(ele)

class FX_TabItem():
    def __init__(self, tabitem_ele):
        self.TabItem = tabitem_ele
        self.Init()

    def Init(self):
        pass
            

class FX_Clipboard:
    def Clear():
        win32clipboard.EmptyClipboard()

    def SetTextData(data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, data)

    def GetTextData():
        data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        return data


print(UIAutomationClient.UIA_TextControlTypeId)

    
