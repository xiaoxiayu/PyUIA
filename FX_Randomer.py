import os
import platform
import random
import string

##special_control_key = [91,  27,  92]

class FX_Randomer:
    def __init__(self):
        self.element_map = {}
        pass

    def AppendElement(self, deep_index, element):
        if len(self.element_map) == 0:
            self.element_map[deep_index] = []
            self.element_map[deep_index].append(element)
            return
        if element in self.element_map[deep_index]:
            return
        else:
            self.element_map[deep_index].append(element)
        

    def SetElements(self, deep_index, element_list):
        self.element_map[deep_index] = element_list

    def SetRange(self):
        pass

    def GetElement(self, deep_index):
        try:
            return random.choice(self.element_map[deep_index])
        except:
            return None

    def GetAllElements(self, deep_index):
        return self.element_map[deep_index]

    def ClearElements(self):
        self.element_map = {}

    def GetInt(max_val, min_val=0):
        return random.randint(min_val, max_val)

    def GetString(str_len):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(str_len)])

    def _byte_range(first, last):
        return list(range(first, last+1))

    def _random_utf8_seq(first_values, traiiling_values):
        first = random.choice(first_values)
        if first <= 0x7F:
            return bytes([first])
        elif first <= 0xDF:
            return bytes([first, random.choice(traiiling_values)])
        elif first == 0xE0:
            return bytes([first, random.choice(FX_Randomer._byte_range(0xA0, 0xBF)), random.choice(traiiling_values)])
        elif first == 0xED:
            return bytes([first, random.choice(FX_Randomer._byte_range(0x80, 0x9F)), random.choice(traiiling_values)])
        elif first <= 0xEF:
            return bytes([first, random.choice(traiiling_values), random.choice(traiiling_values)])
        elif first == 0xF0:
            return bytes([first, random.choice(FX_Randomer._byte_range(0x90, 0xBF)), random.choice(traiiling_values), random.choice(traiiling_values)])
        elif first <= 0xF3:
            return bytes([first, random.choice(traiiling_values), random.choice(traiiling_values), random.choice(traiiling_values)])
        elif first == 0xF4:
            return bytes([first, random.choice(FX_Randomer._byte_range(0x80, 0x8F)), random.choice(traiiling_values), random.choice(traiiling_values)])

    def GetUTF8Bytes(str_len):
        utf8_first_values = FX_Randomer._byte_range(0x30, 0x5A) + FX_Randomer._byte_range(0xC2, 0xF4)
##        for sk in special_control_key:
##            utf8_first_values.remove(sk)
##        print(utf8_first_values)
##        ff
        utf8_trailing_values = FX_Randomer._byte_range(0x80, 0xBF)
        ustr = b''
        for i in range(str_len):
            ustr += FX_Randomer._random_utf8_seq(utf8_first_values, utf8_trailing_values)
        return ustr


def FX_CreateRandomer():
    return FX_Randomer()



