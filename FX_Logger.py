import os
import platform
import random
import lxml
import codecs
import time
import datetime
from lxml import etree, objectify

class FX_Logger:
    def __init__(self, logpath):
        self.fp = None
        self.doc = None
        self.cur = None
        self._root = None
        self.logpath = logpath
        self.start_ele_list = []
        pass

    def Create(self):
        time_now = datetime.datetime.now()
        time_now = str(time_now.strftime('%Y-%m-%d'))
        xml = b'''<?xml version="1.0" encoding="UTF-8"?>
        <Log time="%s">\n
        ''' % bytes(time_now, 'utf8')

        self.fp = open(self.logpath, 'wb')
        self.fp.write(xml)
        
##        self._root = objectify.fromstring(xml)
##

##        self._root.set("time", time_now)
##        self.cur = self._root
##        return self._root

    def Close(self):
        self.fp.write(b'</Log>\n')
        self.fp.close()

    def StartElement(self, tag, attri_dic={}):
        atti_str = ''
        for atti_key in attri_dic.keys():
            atti_str += atti_key + '='
            atti_str = atti_str + '"%s"'%attri_dic[atti_key] + ' '
            
        self.fp.write(b'<%s %s>\n' % (bytes(tag, 'utf8'), bytes(atti_str, 'utf8')))
        self.start_ele_list.append(tag)
##        appt = objectify.Element(tag)
##        return appt

    def EndElement(self):
        tag = self.start_ele_list.pop()
        self.fp.write(b'</%s>\n' % bytes(tag, 'utf8'))

    def Append(self, cur, ele):
        cur.append(ele)
        self.cur = ele

    def SubElement(self, cur, tag):
        objectify.SubElement(cur, tag)

    def Set(self, cur, data):
        for key in data.keys():
            cur.set(key, data[key])

    def Flush(self):
        # remove lxml annotation
        objectify.deannotate(self._root)
        etree.cleanup_namespaces(self._root)
     
        # create the xml string
        obj_xml = etree.tostring(self._root,
                                 pretty_print=True,
                                 xml_declaration=True)
     
        try:
            with open(self.logpath, "wb") as xml_writer:
                xml_writer.write(obj_xml)
        except IOError:
            pass

    def Init(self):
        time_now = datetime.datetime.now()
        time_now = str(time_now.strftime('%Y-%m-%d'))

        self.cur = etree.Element('Log')
    
        self.doc = etree.ElementTree(self.cur)
        self.cur = etree.SubElement(self.cur, 'MonkeyTest', 
                                      time=time_now)


    def AddChild(self, tag):
        self.cur = etree.SubElement(self.cur, tag)
        
##    def Flush(self):
##        self.fp.flush()

    def Log(self):
        pass

    def Parse(self):
        pass

    @property
    def root(self):
        return self._root

    @property
    def current(self):
        return self.cur

def FX_CreateLogger(logpath):
    logger = FX_Logger(logpath)
##    logger.Init()
    return logger
##
logger = FX_CreateLogger('logtest.xml')
logger.Create()
for i in range(100):
    logger.StartElement('a'+str(i))
    logger.EndElement()
##    ele.a = 'aaa'
##    logger.Append(root, ele)

print('===========================')
logger.Close()

##logger.AddChild('MainWindow')
##logger.AddChild('Layer')
##logger.AddChild('ControlElement')
##logger.Close()

##def create_appt(data):
##    """
##    Create an appointment XML element
##    """
##    appt = objectify.Element("appointment")
##    appt.begin = data["begin"]
##    appt.uid = data["uid"]
##    appt.alarmTime = data["alarmTime"]
##    appt.state = data["state"]
##    appt.location = data["location"]
##    appt.duration = data["duration"]
##    appt.subject = data["subject"]
##    return appt
## 
###----------------------------------------------------------------------
##def create_xml():
##    """
##    Create an XML file
##    """
## 
##    xml = b'''<?xml version="1.0" encoding="UTF-8"?>
##    <zAppointments>
##    </zAppointments>
##    '''
## 
##    root = objectify.fromstring(xml)
##    root.set("reminder", "15")
## 
##    appt = create_appt({"begin":1181251680,
##                        "uid":"040000008200E000",
##                        "alarmTime":1181572063,
##                        "state":"",
##                        "location":"",
##                        "duration":1800,
##                        "subject":"Bring pizza home"}
##                       )
##    root.append(appt)
## 
##    uid = "604f4792-eb89-478b-a14f-dd34d3cc6c21-1234360800"
##    appt = create_appt({"begin":1234360800,
##                        "uid":uid,
##                        "alarmTime":1181572063,
##                        "state":"dismissed",
##                        "location":"",
##                        "duration":1800,
##                        "subject":"Check MS Office website for updates"}
##                       )
##    root.append(appt)
## 
##    # remove lxml annotation
##    objectify.deannotate(root)
##    etree.cleanup_namespaces(root)
## 
##    # create the xml string
##    obj_xml = etree.tostring(root,
##                             pretty_print=True,
##                             xml_declaration=True)
## 
##    try:
##        with open("example.xml", "wb") as xml_writer:
##            xml_writer.write(obj_xml)
##    except IOError:
##        pass
## 
###----------------------------------------------------------------------
##if __name__ == "__main__":
##    create_xml()
##    
