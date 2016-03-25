import os
from FX_WindowsAutomation import *
from FX_Randomer import *
from collections import defaultdict

def tree():
    return defaultdict(tree)

def add(t, keys):
    for key in keys:
        t = t[key]

class SkipWindow:
    window_title_list = ['打开', \
                         '浏览文件夹', \
                         '打印成PDF文件-福昕PDF打印机', \
                         '另存为', \
                         'Save PDF File As', \
                         'Save Adobe PDF Settings As', \
                         '保存福昕PDF设置']

class SpeciallyWindow:
    window_title_list = ['进度', '安全警告'] # Close save as window.

class FXReader_PopupWindow:
    def __init__(self, ReaderWindow, FXWorkWindow, ActionFXElement, FatherFXWindow):
        self.ActionFXElement = ActionFXElement
        self.FatherWindow = FatherFXWindow
        self.work_window = FXWorkWindow
        self.TabArray = []
        self.AllElements = []
        self.ChildWindow = None
        self.ElementArray = None
        self.WindowType = -1
        self.RandomManager = FX_CreateRandomer()
        self.ReaderWindow = ReaderWindow

    def Init(self, condition=None):
        window_title = FX_GetWindowTitle(self.work_window)
        if window_title in SkipWindow.window_title_list:
            print('Close Window: %s' % FX_GetWindowTitle(self.work_window))
            self.Close()
            return False
        if window_title in SpeciallyWindow.window_title_list:
            if window_title == '进度':
                finder = FX_Window(None)
                saveas_window = finder.FindWindowByName('Save PDF File As')
                if saveas_window != None:
                    FX_SetForegroundWindow(saveas_window)
            if windows_title == '安全警告':
                FX_SendKey('y')
                    
        self.Update(condition)
        return True

    def Update(self, condition=None):
        self.RandomManager.ClearElements()
        self.TabArray = []
        self.AllElements = []
        root_element = FX_GetElementFromWindow(self.work_window)
        self.WindowType = root_element.GetType()

        if condition == None:
            condition = FX_Condition()
            find_condition = condition.CreateTrueCondition()
        else:
            find_condition = condition
            
        tree_scope = FX_TREE_SCOPE()
        cur_element_child = root_element.FindAll(tree_scope.Descendants, find_condition)
        print('Update cnt:%d' % cur_element_child.GetCount())
        for i in range (cur_element_child.GetCount()):
            ele = cur_element_child.GetElementByIndex(i)
            if ele.GetType() == 50019: # Tab
                self.TabArray.append(ele)    
            else:
                if ele not in self.AllElements:
                    self.AllElements.append(ele)
                    self.RandomManager.AppendElement(0, ele)
##                    print('append: %d' % i)

    def GetAllElement(self):
        return self.AllElements

    
    def DoAction(self, ele, select_item=0):
##        if ele.IsVisible == False:
##            return
        ele.SetFocus()
        ele_type = ele.GetType()
        print('Element Name:%s, Type:%s' % (ele.GetName(), ele.GetType()))
        if ele_type == 50003:
            lc = FX_ComboBox(ele)
            lc.SelectItem(select_item)
        elif ele_type == 50008:
            lc = FX_ListControl(ele)
            lc.SelectItem(select_item)
            self.Update()
        elif ele_type == 50031: # SplitButton
            GetPoupupMenu()
        elif ele_type == 50019: # TabItem
            if ele.MouseLButtonClick() == False:
                pos = FX_GetCursorPos()
                FX_MouseLClick(pos[0], pos[1])
##                aaaaaaaa
            self.Update()
        elif ele_type == 50004: # Edit
            if ele.MouseLButtonClick() == False:
                pass
##                asciistr = FX_Randomer.GetString(FX_Randomer.GetInt(300))
##                FX_SendString(asciistr, 0.1)
##                bbbbbbb
        else:
            if ele.MouseLButtonClick() == False:
                pass
##                pos = FX_GetCursorPos()
##                print('Force Press: %d, %d' % (pos[0], pos[1]))
##                FX_MouseLClick(pos[0], pos[1])
##                cccccccccccc
                
        time.sleep(0.5)
        
    def DoElement(self):
        window_return_type = -1
        print('Current Window: %s, count: %d' % (FX_GetWindowTitle(self.work_window), len(self.AllElements)))
        #for i in range(0, len(self.AllElements)):
        do_cnt = 10000
        if self.WindowType == 50033:
            do_cnt = len(self.AllElements)
            
        for i in range(do_cnt):
##            try:
##                ele = self.AllElements[i]
            if window_return_type >= 0:
                break
            print('PopupWindow i:%d, return type:%d' % (i, window_return_type))
            ele = self.RandomManager.GetElement(0)
            print('Current Window: %s,  Name: %s, Type:%d' \
                  % (FX_GetWindowTitle(self.work_window), ele.GetName(), ele.GetType()))

            
            self.DoAction(ele)
##            except:
##                pass

            current_window = FX_GetForegroundWindow()
            print('CurrentWindow Title: %s' % current_window.processid)
            print('WorkWindow Title: %s' % self.work_window.processid)
            
            if current_window.GetWin32Window() != self.work_window.GetWin32Window():
                print('Different Window. Current:%d-%s, Father:%d-%s.'\
                      %(current_window.GetProcessID(), current_window.GetTitle(), self.FatherWindow.GetProcessID(), self.FatherWindow.GetTitle()))
                time.sleep(1.5)
                current_window = FX_GetForegroundWindow()
##                if sec_current_window.GetWin32Window() != current_window.GetWin32Window():
                
                if current_window.GetWin32Window() == self.ReaderWindow.GetWin32Window():
                    print('Windows: %s, Return window already close.' % FX_GetWindowTitle(self.work_window))
                    return 1 # Window already close.
                window_ele = FX_GetElementFromWindow(current_window)
                if window_ele.GetClassName() != '#32770':
                    if current_window.GetProcessID() != self.FatherWindow.GetProcessID():
                        print('1taskkill /F /PID %d, %s' % (current_window.GetProcessID(), current_window.GetTitle()))
                        time.sleep(0.5)
                        os.popen('taskkill /F /PID %d' % current_window.GetProcessID())
                        if not FX_SetForegroundWindow(self.work_window):
                            return 2 # Can not find window, Maybe close automation.
                else:
                    if current_window.GetProcessID() != self.FatherWindow.GetProcessID() \
                       or current_window.GetTitle() != self.FatherWindow.GetTitle():
                        pop_win = FXReader_PopupWindow(self.ReaderWindow, current_window, ele, self.work_window)
                        if pop_win.Init():
                            try:
                                window_return_type = pop_win.DoElement()
                            except:
                                print('FXReader_PopupWindow-%s-ERROR.' % current_window.GetTitle())
                                return 3
                    else:
                        print('Windows: %s, Return' % FX_GetWindowTitle(self.work_window))
                        return 3 # Window is close and return to father.
        print('Windows: %s, Close' % FX_GetWindowTitle(self.work_window))
        self.Close()
        return 0

    def Close(self):
        FX_KeybdPress(27)
        FX_KeybdRelease(27)
        
def FXAPP_GetAllElementInView(element_array, save_tree, father_element=None):
    children_dic = {}
    final_element_list = []
    element_count = element_array.GetCount()
    for i in range(0, element_count):
        cur_element = element_array.GetElementByIndex(i)
##        print(cur_element.GetClassName())

        condition = FX_Condition()
        tree_scope = FX_TREE_SCOPE()
        cur_element_child = cur_element.FindAll(tree_scope.Children, condition.CreateTrueCondition())
##        print(cur_element)
        ele_info = FX_GetElementInfo(cur_element)
        ele_info.Father = father_element
        ele_info.FXElement = cur_element
        if (cur_element_child.GetCount() > 0):
            ele_info.Children = cur_element_child
            children_dic[ele_info] = cur_element_child
            save_tree[father_element] = cur_element_child
        else:
            ele_info.Children = None
            final_element_list.append(ele_info)

    for ele in children_dic:
##        print(ele)
        final_element_list.append(ele)

    if len(final_element_list) > 0:
        save_tree[father_element] = final_element_list
    else:
        save_tree[father_element] = None

    for ele in children_dic:
        FXAPP_GetAllElementInView(children_dic[ele], save_tree, ele)
            
    return save_tree

def FXAPP_Reader_GetMainWindows(reader_window):
    FXAPP_CheckWindow(reader_window)
    tree_walker = FX_CreateTreeWalker()
    return tree_walker.GetChildrenArray(reader_window.GetFXElement())

def FXAPP_CheckWindow(reader_window):
    current_window = FX_GetForegroundWindow()
    if current_window.GetWin32Window() != reader_window.GetWin32Window():
        window_ele = FX_GetElementFromWindow(current_window)
        if window_ele == None:
            print('** GetElement From Window Failed. **')
            return
        time.sleep(1.5)
        current_window = FX_GetForegroundWindow()
        if window_ele.GetClassName() != '#32770':
            if current_window.GetProcessID() != reader_window.GetProcessID():
                print('7taskkill /F /PID %d, Title:%s' % (current_window.GetProcessID(), current_window.GetTitle()))
                time.sleep(0.5)
                os.popen('taskkill /F /PID %d' % current_window.GetProcessID())
                FX_SetForegroundWindow(reader_window)
        else:
            pop_win = FXReader_PopupWindow(reader_window, current_window, None, reader_window)
            if pop_win.Init():
                pop_win.DoElement()

def FXAPP_Wait_InternalWindowByTitle(reader_window, title_name, timeout=10):
    time_id = 0
    while 1:
        if time_id >= timeout:
            return -1
        
        current_window = FX_GetForegroundWindow()
        if current_window.GetWin32Window() != reader_window.GetWin32Window():
            window_ele = FX_GetElementFromWindow(current_window)
            if window_ele == None:
                print('** GetElement From Window Failed. **')
                return -1
            time.sleep(0.5)
            current_window = FX_GetForegroundWindow()
##            if window_ele.GetClassName() != '#32770':
##                pass
##                if current_window.GetProcessID() != reader_window.GetProcessID():
##                    print('7taskkill /F /PID %d, Title:%s' % (current_window.GetProcessID(), current_window.GetTitle()))
##                    time.sleep(0.5)
##                    os.popen('taskkill /F /PID %d' % current_window.GetProcessID())
##                    FX_SetForegroundWindow(reader_window)
##            else:
            print(window_ele.GetName())
            if window_ele.GetName() == title_name:
                return window_ele
            time_id += 1
            time.sleep(1)


def FXAPP_Reader_GetPoupupMenuRect(reader_element):
    tree_walker = FX_CreateTreeWalker()

    ele_1 = tree_walker.GetFirstChild(reader_element)
    if ele_1 == None:
        return None
    if ele_1.GetType() == 50033:
        if ele_1.GetClassName().find('Afx:') != -1:
            print(ele_1.GetRect())
            rect = ele_1.GetRect()
            print('%d,%d,%d,%d' % (rect.left, rect.top, rect.right, rect.bottom))
            return ele_1.GetRect()
    while 1:
        ele_1 = tree_walker.GetNextSibling(ele_1)
        if ele_1 == None:
            return None
        if ele_1.GetType() == 50033:
            if ele_1.GetClassName().find('Afx:') != -1:
                rect = ele_1.GetRect()
                print(ele_1.GetRect())
                print('%d,%d,%d,%d' % (rect.left, rect.top, rect.right, rect.bottom))
                return ele_1.GetRect()


def FXAPP_Reader_GetToolBar(label=''):
    pass

def FXAPP_Reader_GetToolBarElement(eleinfo=''):
    pass

def FXAPP_Html_GetAllElement(eletype=''):
    pass

def FXAPP_Html_GetElement(eleinfo=''):
    pass


