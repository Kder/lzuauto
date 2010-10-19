#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''
lzuauto - 兰大上网认证系统自动登录工具。
    
主要功能
    
    一键登录/退出、流量查询（支持验证码识别）
    
使用方法
    
    解压后，修改conf.txt，把自己的用户名密码填入。 运行 lzuauto.exe或lzuauto.pyw 就会出来主界面。
    
系统要求
    
    Linux下面需要的依赖：
    
        python(标准发行版里面的版本都应该支持，理论上不支持python3.0且未测试)
        python-imaging(PIL库)
        tesseract(一个ocr工具，项目主页 http://code.google.com/p/tesseract-ocr/ ）
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        python-2.5.4.msi
        PIL-1.1.7.win32-py2.5.exe
        
    以上软件请到分别下列地址下载：
    
        http://www.python.org
        http://www.pythonware.com/products/pil/
        
'''

__author__= 'ysjdxcn'
__copyright__ = 'Copyright 2010 ysjdxcn & Kder'
__credits__ = ['ysjdxcn','Kder']
__version__ = '1.0.3'
__date__ = '2010-10-17'
__maintainer__ = ['ysjdxcn','Kder']
__email__ = ['ysjdxcn (#) gmail dot com', 'kderlin (#) gmail dot com']
__url__ = ['http://ranhouzenyang.com/', 'http://www.kder.info']
__license__ = 'GNU General Public License v3'
__status__ = 'Release'
__projecturl__ = 'http://code.google.com/p/lzuauto/'


import os
import urllib, httplib, time, re, sys
from pytesser import *
from idlelib import textView


################################################################################

try:
    f = open('conf.txt')
    userid, passwd = f.readline().split()
    f.close()
except:
    print 'Error: Cannot open conf.txt, please make sure that the file exists and is accessible.'
    sys.exit(3)

option = 'alert(.*?);'
option1 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)MB'
option2 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)Hours'

def login():
    params = urllib.urlencode( {'userid':userid,'password':passwd,'serivce':'intenet','chap':'0','random':'internet','x':'25','y':'12'} )
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection( "1.1.1.1" )  
    conn.request( "POST", "/passwd.magi", params, headers )
    response = conn.getresponse()
    data = response.read() 
    conn.close()
    #print data
    result = re.findall(option, data)
    if len(result)>0:
        return result[0].split('\"')[1].decode('gb2312')
    else :
        return 1

def logout():
    params = urllib.urlencode( {'imageField.x':'44','imageField.y':'27'} )
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection( "1.1.1.1" )  
    conn.request( "POST", "/userout.magi", params, headers )
    response = conn.getresponse()
    conn.close()
    if response.status == 200:
        return 1
    else :
        return 0

def checkflow():
    headers = {"User-Agetn":"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100916 Firefox/3.6.10","Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Keep-Alive":"115","Connection":"keep-alive"}
    conn = httplib.HTTPConnection( "a.lzu.edu.cn" )  
    conn.request( 'GET', '/', headers = headers )
    response = conn.getresponse()
    #print response.getheaders()
    cookie = response.getheader('set-cookie').split()[0]
    temp = {'Cookie':cookie}
    headers.update(temp)
    conn.close()

    conn0 = httplib.HTTPConnection( "a.lzu.edu.cn" )  
    conn0.request( 'GET', '/selfLogon.do', headers = headers )
    response0 = conn0.getresponse()
    #print response0.getheaders()
    conn0.close()

    conn1 = httplib.HTTPConnection("a.lzu.edu.cn")
    conn1.request( 'GET', '/servlet/AuthenCodeImage', headers = headers)
    response1 = conn1.getresponse()
    #print response1.getheaders()
    data = response1.read()
    #print data
    img = open('code.jpg','wb')
    img.write(data)
    img.close()
    image = Image.open('code.jpg')
    s = image_to_string(image)[0:4]
    #print s[0:4]
    conn1.close()

    conn2 = httplib.HTTPConnection("a.lzu.edu.cn")
    params = urllib.urlencode( {'user_id':userid,'passwd':passwd,'validateCode':s} )
    #print params
    conn2.request( 'POST', '/selfLogonAction.do', params, headers = headers)
    response2 = conn2.getresponse()
    #print response2.getheaders()
    data = response2.read()
    f = open('result','w')
    f.write(data)
    f.close()
#    print data            
    conn2.close()
    
    conn3 = httplib.HTTPConnection("a.lzu.edu.cn")
    conn3.request( 'GET', '/selfIndexAction.do',headers = headers)
    response3 = conn3.getresponse()
    data = response3.read()
#    print data
    conn3.close()

    conn4 = httplib.HTTPConnection("a.lzu.edu.cn")
    conn4.request( 'GET', '/userQueryAction.do',headers = headers)
    response4 = conn4.getresponse()
    data = response4.read()
    conn4.close()
    mb = re.findall(option1,data)
    hour = re.findall(option2,data)
    if len(mb)>0:
        MB = mb[0].split('&nbsp')[0][1:]
        HOUR = hour[0].split('&nbsp')[0]
    else :
        checkflow()
    return MB, HOUR

def checkstatus():
    pass

################################################################################

import Tkinter
import tkMessageBox 

class Application(Tkinter.Frame):

    def login(self):
        result = login()
        if result == 1 or u'可用流量' in result:
            self.Dialog('登录成功', u"登录成功^_^%s" % result)
        else:
            self.Dialog('错误', result, 'error')
#        self.Dialog(None, data=result)
    
    def logout(self):
        #print 'logout'
        if logout():
            self.Dialog(None, '您已经成功退出:-)\n')
        else :
            self.logout

    def checkflow(self):
        #print 'checkflow'
        self.Dialog(None, '您本月已经使用的流量为 %s MB\n您本月已经上网 %s 小时' % checkflow())
    
    def Dialog(self, title=None, data=None, icon='info'):
        tkMessageBox.showinfo(title, data, icon=icon)
        
    def About(self):
        self.Dialog('关于', "lzuauto %s\n作者 ysjdxcn & Kder\n 项目主页 http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % __version__)
        
    def Usage(self):
        textView.view_text(self, '用法', __doc__)

    def createWidgets(self):
        self.button = []
        button_label = ["登录外网", "查询流量", "退出外网", "退出程序"]
        actions = [self.login, self.checkflow, self.logout, self.quit]
        # actions = [self.say_hi, self.say_hi, self.say_hi, self.say_hi]
        
        for i in range(4):
            self.button.append(Tkinter.Button(self))
            self.button[i]["text"] = button_label[i]
            self.button[i]["command"] = actions[i]
#            self.button[i].pack({"side": "left", 'expand' : 1, 'fill' : 'both', 'padx' : 5, 'pady' : 5 })
        
        self.button[0].pack({"side": "left", 'expand' : 1, 'fill' : 'both', 'padx' : 5, 'pady' : 5 })
        self.button[1].pack({"side": "left", 'expand' : 1, 'fill' : 'both', 'padx' : 5, 'pady' : 5 })
        self.button[2].pack({"side": "left", 'expand' : 1, 'fill' : 'both', 'padx' : 5, 'pady' : 5 })
        self.button[3].pack({"side": "left", 'expand' : 1, 'fill' : 'both', 'padx' : 5, 'pady' : 5 })
            
        top = self.winfo_toplevel()
        self.menuBar = Tkinter.Menu(top)
        top["menu"] = self.menuBar

        self.subMenu1 = Tkinter.Menu(self.menuBar)
        self.subMenu2 = Tkinter.Menu(self.menuBar)
        self.menuBar.add_cascade(label="文件", menu=self.subMenu1)
        self.subMenu1.add_command(label="退出", command=self.quit)
        self.menuBar.add_cascade(label="帮助", menu=self.subMenu2)
        self.subMenu2.add_command(label="关于", command=self.About)
        self.subMenu2.add_command(label="用法", command=self.Usage)
        
        # self.QUIT = Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"]   = "red"
        # self.QUIT["command"] =  self.quit

        # self.QUIT.pack({"side": "left"})      
        
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        
if __name__ == "__main__":
    root = Tkinter.Tk()
    app = Application(master=root)
    app.master.title('兰大上网认证系统自动登录工具')
    
    app.mainloop()
    root.destroy()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
