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
        tcl和tk
        tesseract(一个ocr工具，项目主页 http://code.google.com/p/tesseract-ocr/ ）
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        Python2.5以上，下载地址：http://www.python.org
    
'''


import sys
import os
import Tkinter
import tkMessageBox 
from idlelib import textView

if os.name == 'posix':
    import py_compile
    py_compile.compile('main.pyw','main.pyc')

import main


__version__ = '1.1.1'
__revision__ = "$Revision$"
__date__ = '$Date$'
__author__= '$Author$'


class Application(Tkinter.Frame):

    def login(self):
        if main.loadconf() is 8:
            self.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        result = main.login(main.loadconf())
        if result is 1 or 'M)' in result:
            self.Dialog(main.TITLE_LOGIN, main.MSG_LOGIN.decode('utf-8')
             % result)
        else:
            self.Dialog(main.TITLE_ERR, result, 'error')
 
    def logout(self):
        if main.logout():
            self.Dialog(main.TITLE_LOGOUT, main.MSG_LOGOUT)
        else :
            self.logout

    def checkflow(self):
        if main.loadconf() is 8:
            self.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        flow = main.checkflow(main.loadconf())
        if type(flow) is type(tuple()):
            self.Dialog(main.TITLE_FLOW, main.MSG_FLOW % flow)
        elif type(flow) is type(unicode()):
            self.Dialog(main.TITLE_ERR, flow, 'error')
        elif flow is 1:
            self.Dialog(main.TITLE_ERR, main.ERR_OCR, 'error')
            sys.exit(4)
        elif flow is 5:
            self.Dialog(main.TITLE_ERR, main.ERROR_IO, 'error')
        elif flow is 6:
            self.Dialog(main.TITLE_ERR, main.ERR_DJPEG, 'error')
        elif flow is 7:
            self.Dialog(main.TITLE_ERR, main.ERR_TESSERACT, 'error')

    def Dialog(self, title=None, data=None, icon='info'):
        tkMessageBox.showinfo(title, data, icon=icon)
        
    def About(self, event=None):
        self.Dialog(main.TITLE_ABOUT, "lzuauto %s.%s\n作者： ysjdxcn & Kder\n项目主页： http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % (__version__, __revision__.split(':')[1][:-1].strip()))
        
    def Usage(self, event=None):
        textView.view_text(self, main.TITLE_USAGE, __doc__)

    def createWidgets(self):

        # top = self.winfo_toplevel()
        # self.menuBar = Tkinter.Menu(top)
        # top["menu"] = self.menuBar
        self.menuBar = Tkinter.Menu(self)
        self.master["menu"] = self.menuBar
        self.subMenu1 = Tkinter.Menu(self.menuBar, tearoff=0)
        self.subMenu2 = Tkinter.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="文件(F)", menu=self.subMenu1, underline =3)
        self.subMenu1.add_command(label="退出(X)", command=self.quit, accelerator='Ctrl+Q', underline =3)
        self.menuBar.add_cascade(label="帮助(H)", menu=self.subMenu2, underline =3)
        self.subMenu2.add_command(label="关于(A)", command=self.About, accelerator='Ctrl+A', underline =3)
        self.subMenu2.add_command(label="用法(U)", command=self.Usage, accelerator='F1', underline =3)

        buttons = list()
        button_label = ["登录外网", "查询流量", "退出外网", "退出程序"]
        actions = [self.login, self.checkflow, self.logout, self.quit]
        idx = 0
        for bdw in range(2):
            setattr(self, 'of%d' % bdw, Tkinter.Frame(self, borderwidth=0))
            Tkinter.Label(getattr(self, 'of%d' % bdw), text=None).pack(side=Tkinter.LEFT)
            for i in range(2):
                buttons.append(Tkinter.Button(getattr(self, 'of%d' % bdw), text=button_label[idx], width=10,
                       command=actions[idx]))
                buttons[idx].pack(side=Tkinter.LEFT, padx=7, pady=7)
                idx += 1
            getattr(self, 'of%d' % bdw).pack()
        buttons[0].focus_set()
            
    def Quit(self, event=None):
        self.destroy()
        root.destroy()
        
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.master.title('兰大上网认证系统自动登录工具')
        # root.bind('<Escape>', self.Ok)
        root.bind('<Control-q>', self.Quit)
        root.bind('<F1>', self.Usage)
        root.bind('<Control-a>', self.About)
        # self.transient(parent)
        # self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.Ok)
        # self.wait_window()
        
if __name__ == "__main__":
    root = Tkinter.Tk()
    app = Application(master=root)
    #~ app.Dialog('hi','welcome')
    if main.loadconf() is 8:
        app.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        sys.exit(3)
    app.mainloop()
    # root.destroy()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
