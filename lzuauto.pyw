#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''lzuauto - 兰大上网认证系统自动登录工具。
    
主要功能
    
    一键登录/退出、流量查询（支持验证码识别）
    
使用方法
    
    解压后，修改conf.txt，把自己的用户名密码填入。 运行 lzuauto.exe或lzuauto.pyw 就会出来主界面。
    
系统要求
    
    Linux下面需要的依赖：
    
        python(py2.6以上)
        tcl和tk
        tesseract(ocr工具，主页 http://code.google.com/p/tesseract-ocr/ ）
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        Python2.6以上，下载地址：http://www.python.org

'''


import sys
import os
import Tkinter
import tkMessageBox 

if os.name == 'posix':
    import py_compile
    py_compile.compile('main.pyw','main.pyc')

import main


__version__ = main.__version__
__revision__ = main.__revision__
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
        '''display a usage dialog'''
        #a class from idlelib
        class TextViewer(Tkinter.Toplevel):
            """A simple text viewer dialog for IDLE

            """
            def __init__(self, parent, title, text):
                """Show the given text in a scrollable window with a 'close' button

                """
                Tkinter.Toplevel.__init__(self, parent)
                self.configure(borderwidth=5)
                #elguavas - config placeholders til config stuff completed
                self.bg = '#ffffff'
                self.fg = '#000000'

                self.CreateWidgets()
                self.title(title)
                self.transient(parent)
                self.grab_set()
                self.protocol("WM_DELETE_WINDOW", self.Ok)
                self.parent = parent
                self.textView.focus_set()
                #key bindings for this dialog
                self.bind('<Return>',self.Ok) #dismiss dialog
                self.bind('<Escape>',self.Ok) #dismiss dialog
                self.textView.insert(0.0, text)
#                self.textView.config(state=Tkinter.DISABLED)
                self.withdraw()
                self.update()
#                x, y = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2, (self.winfo_screenheight() - self.winfo_reqheight()) / 2
                x, y = (self.winfo_screenwidth() - self.winfo_width()) / 2, (self.winfo_screenheight() - self.winfo_height()) / 2
#                sys.stdout.write(str([self.winfo_width(),self.winfo_height()]))
                self.geometry('+%d+%d' % (x, y))
                self.deiconify()
                self.update()
                self.wait_window()

            def Ok(self, event=None):
                self.destroy()

            def CreateWidgets(self):
                frameText = Tkinter.Frame(self, relief=Tkinter.SUNKEN, height=700)
                frameButtons = Tkinter.Frame(self)
                self.buttonOk = Tkinter.Button(frameButtons, text='OK',
                                       command=self.Ok, takefocus=Tkinter.FALSE)
#                self.scrollbarView = Tkinter.Scrollbar(frameText, orient=Tkinter.VERTICAL,
#                                               takefocus=Tkinter.FALSE, highlightthickness=0)
                self.textView = Tkinter.Text(frameText, wrap=Tkinter.WORD, highlightthickness=0,
                                     fg=self.fg, bg=self.bg)
#                self.scrollbarView.config(command=self.textView.yview)
#                self.textView.config(yscrollcommand=self.scrollbarView.set)
                self.buttonOk.pack()
#                self.scrollbarView.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
                self.textView.pack(side=Tkinter.LEFT,expand=Tkinter.TRUE,fill=Tkinter.BOTH)
                frameButtons.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)
                frameText.pack(side=Tkinter.TOP,expand=Tkinter.TRUE,fill=Tkinter.BOTH)

        tv = TextViewer(self, main.TITLE_USAGE, __doc__)

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
        self.subMenu2.add_command(label="关于(A)", command=self.About, underline =3)
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
#        self.master.withdraw()
#        self.master.Popup()
        self.master.withdraw()
        self.master.update()
#        self.master.overrideredirect(1)
        self.x, self.y = (self.master.winfo_screenwidth() - self.master.winfo_width()) / 2, (self.master.winfo_screenheight() - self.master.winfo_height()) / 2
#        sys.stdout.write(str((x, y)))
        self.master.geometry('+%d+%d' % (self.x, self.y))
        self.master.deiconify()
        self.master.update()
#        self.master.bind('<Escape>', self.Ok)
        self.master.bind('<Control-q>', self.Quit)
        self.master.bind('<F1>', self.Usage)
#        self.master.bind('<Control-a>', self.About)
        # self.transient(parent)
        # self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.Ok)
        # self.wait_window()
        
if __name__ == "__main__":
    root = Tkinter.Tk()
    app = Application(master=root)
    if main.loadconf() is 8:
        app.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        sys.exit(3)
    app.mainloop()
    # root.destroy()

#$Id$
#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
