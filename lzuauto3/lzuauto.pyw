#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''lzuauto - 兰大上网认证系统自动登录工具。
    
主要功能
    
    一键登录/退出、流量查询（支持验证码识别）
    
使用方法
    
    解压后，第一次运行 lzuauto.exe或lzuauto.pyw ，会弹出对话框，把自己的账号密码填入，
    确定，然后点击“登录外网”即可。
    
运行源码版的系统要求
    
    Linux下需要的依赖：
    
        python3
        tcl和tk
        tesseract(ocr工具，主页 http://code.google.com/p/tesseract-ocr/ ）
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        Python3，下载地址：http://www.python.org

'''


import sys
import os
import tkinter
import tkinter.messagebox
import tkinter.font

if os.name == 'posix':
    import py_compile
    py_compile.compile('main.pyw','main.pyc')

import main


__version__ = '1.2.0'
__revision__ = "$Revision$"
__date__ = '$Date$'
__author__= '$Author$'


class Application(tkinter.Frame):

    def login(self):
        userpass = main.loadconf(getUserpass)
        # print(type(userpass))
        result = main.login(userpass)
        if result is 1 or 'M)' in result:
            self.Dialog(main.TITLE_LOGIN, main.MSG_LOGIN % result)
        else:
            self.Dialog(main.TITLE_ERR, result, 'error')
 
    def logout(self):
        if main.logout():
            self.Dialog(main.TITLE_LOGOUT, main.MSG_LOGOUT)
        else :
            self.logout

    def checkflow(self):
        userpass = main.loadconf(getUserpass)
        flow = main.checkflow(userpass)
        if type(flow) is type(tuple()):
            self.Dialog(main.TITLE_FLOW, main.MSG_FLOW % flow)
        elif type(flow) is type(str()):
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
        tkinter.messagebox.showinfo(title, data, icon=icon)
        
    def About(self, event=None):
        self.Dialog(main.TITLE_ABOUT, "lzuauto %s.%s\n作者： ysjdxcn & Kder\n项目主页： http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % (main.__version__, main.__revision__.split(':')[1][:-1].strip()))
        
    def Usage(self, event=None):
        #a class from idlelib
        class TextViewer(tkinter.Toplevel):
            """A simple text viewer dialog for IDLE

            """
            def __init__(self, parent, title, text):
                """Show the given text in a scrollable window with a 'close' button

                """
                tkinter.Toplevel.__init__(self, parent)
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
#                self.textView.config(state=tkinter.DISABLED)
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
                frameText = tkinter.Frame(self, relief=tkinter.SUNKEN, height=700)
                frameButtons = tkinter.Frame(self)
                self.buttonOk = tkinter.Button(frameButtons, text='OK',
                                       command=self.Ok, takefocus=tkinter.FALSE)
#                self.scrollbarView = tkinter.Scrollbar(frameText, orient=tkinter.VERTICAL,
#                                               takefocus=tkinter.FALSE, highlightthickness=0)
                self.textView = tkinter.Text(frameText, wrap=tkinter.WORD, highlightthickness=0,
                                     fg=self.fg, bg=self.bg)
#                self.scrollbarView.config(command=self.textView.yview)
#                self.textView.config(yscrollcommand=self.scrollbarView.set)
                self.buttonOk.pack()
#                self.scrollbarView.pack(side=tkinter.RIGHT,fill=tkinter.Y)
                self.textView.pack(side=tkinter.LEFT,expand=tkinter.TRUE,fill=tkinter.BOTH)
                frameButtons.pack(side=tkinter.BOTTOM,fill=tkinter.X)
                frameText.pack(side=tkinter.TOP,expand=tkinter.TRUE,fill=tkinter.BOTH)
     
        tv = TextViewer(self, main.TITLE_USAGE, __doc__)

    def createWidgets(self):
        ft = tkinter.font.Font(family = '宋体',size = 9,weight = tkinter.font.NORMAL)

        # top = self.winfo_toplevel()
        # self.menuBar = tkinter.Menu(top)
        # top["menu"] = self.menuBar
        self.menuBar = tkinter.Menu(self)
        self.master["menu"] = self.menuBar
        self.subMenu1 = tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu2 = tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu3 = tkinter.Menu(self.menuBar, tearoff=0, font=ft)
        self.menuBar.add_cascade(label="文件(F)", menu=self.subMenu1, underline =3)
        self.subMenu1.add_command(label="退出(X)", command=self.quit, accelerator='Ctrl+Q', underline =3)
        self.menuBar.add_cascade(label="设置(S)", menu=self.subMenu2, underline =3)
        self.subMenu2.add_command(label="账号(A)", command=getUserpass, underline =3)
        self.menuBar.add_cascade(label="帮助(H)", menu=self.subMenu3, underline =3)
        self.subMenu3.add_command(label="关于(A)", command=self.About, underline =3)
        self.subMenu3.add_command(label="用法(U)", command=self.Usage, accelerator='F1', underline =3)

        buttons = list()
        button_label = ["登录外网", "查询流量", "退出外网", "退出程序"]
        actions = [self.login, self.checkflow, self.logout, self.quit]
        idx = 0
        for bdw in range(2):
            setattr(self, 'of%d' % bdw, tkinter.Frame(self, borderwidth=0))
            tkinter.Label(getattr(self, 'of%d' % bdw), text=None).pack(side=tkinter.LEFT)
            for i in range(2):
                buttons.append(tkinter.Button(getattr(self, 'of%d' % bdw), 
                    text=button_label[idx], width=10, command=actions[idx], font=ft))
                buttons[idx].pack(side=tkinter.LEFT, padx=7, pady=7)
                idx += 1
            getattr(self, 'of%d' % bdw).pack()
        buttons[0].focus_set()
        for i in range(4):
            buttons[i].bind('<Key-Return>',actions[i])

    def Quit(self, event=None):
        self.destroy()
        root.destroy()
        
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
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

class MyDialog(tkinter.Frame):
    def __init__(self, master=None):
        global userpass
        tkinter.Frame.__init__(self, master)
        self.v1 = tkinter.StringVar()
        self.v2 = tkinter.StringVar()
        l1=tkinter.Label(self,text="账号:")
        l1.grid(row=0,column=0)
        self.e1=tkinter.Entry(self, textvariable=self.v1)
        self.e1.grid(row=0,column=1)
        l2=tkinter.Label(self,text="密码:")
        l2.grid(row=1,column=0)
        self.e2=tkinter.Entry(self,show="*", textvariable=self.v2)
        self.e2.grid(row=1,column=1)
        self.e2.bind('<Key-Return>', self.Ok)
        self.e1.focus_set()
        b1=tkinter.Button(self,text='确定', command=self.Ok)
        b1.grid(row=2,column=0)
        b2=tkinter.Button(self,text='取消', command=self.Cancel)
        b2.grid(row=2,column=1)
        
        self.userpass = main.readconf()
        if self.userpass is not 8:
            # self.v1.set(self.userpass[0])
            # self.v2.set(self.userpass[1])
            self.e1.insert(0,self.userpass[0])
            self.e1.select_range(0,tkinter.END)
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
    root2=tkinter.Tk()
    myapp = MyDialog(root2)
    myapp.master.title("请输入账号密码：")
    # myapp.master.maxsize(1000, 400)
    myapp.mainloop()
    # print(userpass,'g')
    return userpass
        
        
if __name__ == "__main__":
    root = tkinter.Tk()
    app = Application(master=root)
    userpass = main.loadconf(getUserpass)
    app.mainloop()
    # root.destroy()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
