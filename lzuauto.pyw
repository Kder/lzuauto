#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''lzuauto - 兰大上网认证系统自动登录工具。
    
主要功能
    
    一键登录/退出、流量查询（支持验证码识别）
    
使用方法
    
    解压后，第一次运行 lzuauto.exe（或lzuauto.pyw），会弹出对话框，
    把自己的账号密码填入，确定，然后点击“登录外网”即可。
    
运行源码版的系统要求
    
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
import tkFont
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

    def login(self, event=None):
        # if main.loadconf() is 8:
            # self.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        userpass = main.loadconf(getUserpass)
        # print(type(userpass))
        result = main.login(userpass)
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
        # if main.loadconf() is 8:
            # self.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        userpass = main.loadconf(getUserpass)
        flow = main.checkflow(userpass)
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
        self.Dialog(main.TITLE_ABOUT, "lzuauto %s.%s\n作者： ysjdxcn & Kder\n\
项目主页： http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % \
        (__version__, __revision__.split(':')[1][:-1].strip()))
        
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
#                self.bind('<Return>',self.Ok) #dismiss dialog
                self.bind('<Escape>',self.Ok) #dismiss dialog
                self.textView.insert(0.0, text)
#                self.textView.config(state=Tkinter.DISABLED)
                self.withdraw()
                self.update()
#                x, y = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2, (self.winfo_screenheight() - self.winfo_reqheight()) / 2
                x, y = (self.winfo_screenwidth() - self.winfo_width()) / 2, \
                (self.winfo_screenheight() - self.winfo_height()) / 2
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
        ft = tkFont.Font(family = '宋体',size = 9,weight = tkFont.NORMAL)
        self.menuBar = Tkinter.Menu(self)
        self.master["menu"] = self.menuBar
        self.subMenu1 = Tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu2 = Tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu3 = Tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.menuBar.add_cascade(label="文件(F)", menu=self.subMenu1, underline =3)
        self.subMenu1.add_command(label="退出(X)", command=self.quit, accelerator='Ctrl+Q', underline =3)
        self.menuBar.add_cascade(label="设置(S)", menu=self.subMenu2, underline =3)
        self.subMenu2.add_command(label="账号(A)", command=getUserpass, underline =3)
        self.menuBar.add_cascade(label="帮助(H)", menu=self.subMenu3, underline =3)
        self.subMenu3.add_command(label="关于(A)", command=self.About, underline =3)
        self.subMenu3.add_command(label="用法(U)", command=self.Usage, accelerator='F1', underline =3)

        buttons = list()
        button_label = ["登录外网", "查询流量", "退出外网", "退出程序"]
        actions = [self.login, self.checkflow, self.logout, self.Quit]
        idx = 0
        for bdw in range(2):
            setattr(self, 'of%d' % bdw, Tkinter.Frame(self, borderwidth=0))
            Tkinter.Label(getattr(self, 'of%d' % bdw), text=None).pack(side=Tkinter.LEFT)
            for i in range(2):
                buttons.append(Tkinter.Button(getattr(self, 'of%d' % bdw),
                 text=button_label[idx], width=10, command=actions[idx], font=ft))
                buttons[idx].pack(side=Tkinter.LEFT, padx=7, pady=7)
                idx += 1
            getattr(self, 'of%d' % bdw).pack()
        buttons[0].focus_set()
        for i in range(4):
            buttons[i].bind('<Key-Return>',actions[i])
        # buttons[0].bind('<Enter>',actions[0])

    def Quit(self, event=None):
        self.destroy()
        # root.destroy()
        self.master.destroy()
        sys.exit()
        
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        global userpass

        self.pack()
        self.createWidgets()
        self.master.title('兰大上网认证登录工具')
#        self.master.withdraw()
#        self.master.Popup()
        self.master.withdraw()
        self.master.update()
#        self.master.overrideredirect(1)
        self.x, self.y = (self.master.winfo_screenwidth() - self.master.winfo_width()) / 2, \
        (self.master.winfo_screenheight() - self.master.winfo_height()) / 2
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

class MyDialog(Tkinter.Frame):
    def __init__(self, master=None):
        global userpass
        Tkinter.Frame.__init__(self, master)
        self.v1 = Tkinter.StringVar()
        self.v2 = Tkinter.StringVar()
        l1=Tkinter.Label(self,text="账号:")
        l1.grid(row=0,column=0)
        self.e1=Tkinter.Entry(self, textvariable=self.v1)
        self.e1.grid(row=0,column=1)
        l2=Tkinter.Label(self,text="密码:")
        l2.grid(row=1,column=0)
        self.e2=Tkinter.Entry(self,show="*", textvariable=self.v2)
        self.e2.grid(row=1,column=1)
        self.e2.bind('<Key-Return>', self.Ok)
        self.e1.focus_set()
        b1=Tkinter.Button(self,text='确定', command=self.Ok)
        b1.grid(row=2,column=0)
        b2=Tkinter.Button(self,text='取消', command=self.Cancel)
        b2.grid(row=2,column=1)
        
        self.userpass = main.readconf()
        if self.userpass is not 8:
            # self.v1.set(self.userpass[0])
            # self.v2.set(self.userpass[1])
            self.e1.insert(0,self.userpass[0])
            self.e1.select_range(0,Tkinter.END)
            self.e2.insert(0,self.userpass[1])
        userpass = self.userpass

        self.master.withdraw()
        self.master.update()
#        self.master.overrideredirect(1)
        self.x, self.y = (self.master.winfo_screenwidth() - self.master.winfo_width()) / 2, \
        (self.master.winfo_screenheight() - self.master.winfo_height()) / 2
#        sys.stdout.write(str((x, y)))
        self.master.geometry('+%d+%d' % (self.x, self.y))
        self.master.deiconify()
        self.master.update()
        
        self.pack()

    def Ok(self,evt=None):
        global userpass
        self.userpass = (self.e1.get(), self.e2.get())
        if '' not in self.userpass:
            with open(main.CONF,'w') as f:
                f.write('%s %s' % self.userpass)
            userpass = self.userpass
        self.destroy()
        self.master.destroy()
        self.quit()

    def Cancel(self):
        self.destroy()
        self.master.destroy()
        self.quit()
        
def getUserpass(evt=None):
    global userpass
    root2=Tkinter.Tk()
    myapp = MyDialog(root2)
    myapp.master.title("请输入账号密码：")
    # myapp.master.maxsize(1000, 400)
    myapp.mainloop()
    # print(userpass,'g')
    return userpass
        
if __name__ == "__main__":
    root = Tkinter.Tk()
    app = Application(master=root)
    # if main.loadconf() is 8:
        # app.Dialog(main.TITLE_ERR, main.ERR_CONF, 'error')
        # sys.exit(3)
    userpass = main.loadconf(getUserpass)
    app.mainloop()
    
    # root.destroy()

#$Id$
#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
