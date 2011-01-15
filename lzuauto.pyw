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
    
        Python2.6-Python3
        tcl和tk
        tesseract(ocr工具，主页 http://code.google.com/p/tesseract-ocr/ ）
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        Python2.6-Python3，下载地址：http://www.python.org

'''


import sys
import os
try:
    import tkinter as tk
    import tkinter.messagebox as tkmsg
    import tkinter.font as tkfont
except:
    import Tkinter as tk
    import tkFont as tkfont
    import tkMessageBox  as tkmsg
if os.name == 'posix':
    import py_compile
    py_compile.compile('main.pyw','main.pyc')

import main


__version__ = main.__version__
__revision__ = main.__revision__
__date__ = '$Date: 2011-01-09 15:50:28 +0800 (星期日, 2011-01-09) $'
__author__= '$Author: kderlin $'


class Application(tk.Frame):

    def login(self, evt=None):
        userpass = main.loadconf(getUserpass)
        # print(type(userpass))
        result = main.login(userpass)
        if result is 1 or 'M)' in result:
#            print(type(main.lzuauto_text['MSG_LOGIN']),type(result))
            self.Dialog(main.lzuauto_text['TITLE_LOGIN'], main.lzuauto_text['MSG_LOGIN'] % result)
        elif main.TFMMSG['find1'] in result:
            self.Dialog(main.lzuauto_text['TITLE_LOGIN'], main.TFMMSG[15] + result)
        else:
            self.Dialog(main.lzuauto_text['TITLE_ERR'], result, 'error')
 
    def logout(self, evt=None):
        if main.logout():
            self.Dialog(main.lzuauto_text['TITLE_LOGOUT'], main.lzuauto_text['MSG_LOGOUT'])
        else:
            self.logout

    def checkflow(self, evt=None):
        userpass = main.loadconf(getUserpass)
        flow = main.checkflow(userpass)
        if type(flow) is type(tuple()):
            self.Dialog(main.lzuauto_text['TITLE_FLOW'], main.lzuauto_text['MSG_FLOW'] % flow)
        elif flow is 1:
            self.Dialog(main.lzuauto_text['TITLE_ERR'], main.lzuauto_text['ERR_OCR'], 'error')
            sys.exit(4)
        elif flow is 5:
            self.Dialog(main.lzuauto_text['TITLE_ERR'], main.lzuauto_text['ERROR_IO'], 'error')
        elif flow is 6:
            self.Dialog(main.lzuauto_text['TITLE_ERR'], main.lzuauto_text['ERR_DJPEG'], 'error')
        elif flow is 7:
            self.Dialog(main.lzuauto_text['TITLE_ERR'], main.lzuauto_text['ERR_TESSERACT'], 'error')
        else:
            try:
                if type(flow) is type(unicode()):
                    self.Dialog(main.lzuauto_text['TITLE_ERR'], flow, 'error')
            except:
                if type(flow) is type(str()):
                    self.Dialog(main.lzuauto_text['TITLE_ERR'], flow, 'error')

    def Dialog(self, title=None, data=None, icon='info'):
        tkmsg.showinfo(title, data, icon=icon)
        
    def About(self, event=None):
        self.Dialog(main.lzuauto_text['TITLE_ABOUT'], "lzuauto %s.%s\n作者： ysjdxcn & Kder\n项目主页： http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % (main.__version__, main.__revision__.split(':')[1][:-1].strip()))
        
    def Usage(self, event=None):
        #a class from idlelib
        class TextViewer(tk.Toplevel):
            """A simple text viewer dialog for IDLE

            """
            def __init__(self, parent, title, text):
                """Show the given text in a scrollable window with a 'close' button

                """
                tk.Toplevel.__init__(self, parent)
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
#                self.textView.config(state=tk.DISABLED)
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
                frameText = tk.Frame(self, relief=tk.SUNKEN, height=700)
                frameButtons = tk.Frame(self)
                self.buttonOk = tk.Button(frameButtons, text='OK',
                                       command=self.Ok, takefocus=tk.FALSE)
#                self.scrollbarView = tk.Scrollbar(frameText, orient=tk.VERTICAL,
#                                               takefocus=tk.FALSE, highlightthickness=0)
                self.textView = tk.Text(frameText, wrap=tk.WORD, highlightthickness=0,
                                     fg=self.fg, bg=self.bg)
#                self.scrollbarView.config(command=self.textView.yview)
#                self.textView.config(yscrollcommand=self.scrollbarView.set)
                self.buttonOk.pack()
#                self.scrollbarView.pack(side=tk.RIGHT,fill=tk.Y)
                self.textView.pack(side=tk.LEFT,expand=tk.TRUE,fill=tk.BOTH)
                frameButtons.pack(side=tk.BOTTOM,fill=tk.X)
                frameText.pack(side=tk.TOP,expand=tk.TRUE,fill=tk.BOTH)
     
        tv = TextViewer(self, main.lzuauto_text['TITLE_USAGE'], __doc__)

    def createWidgets(self):
        ft = tkfont.Font(family = '宋体',size = 9,weight = tkfont.NORMAL)

        # top = self.winfo_toplevel()
        # self.menuBar = tk.Menu(top)
        # top["menu"] = self.menuBar
        self.menuBar = tk.Menu(self)
        self.master["menu"] = self.menuBar
        self.subMenu1 = tk.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu2 = tk.Menu(self.menuBar, tearoff=0, font=ft)
        self.subMenu3 = tk.Menu(self.menuBar, tearoff=0, font=ft)
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
            setattr(self, 'of%d' % bdw, tk.Frame(self, borderwidth=0))
            tk.Label(getattr(self, 'of%d' % bdw), text=None).pack(side=tk.LEFT)
            for i in range(2):
                buttons.append(tk.Button(getattr(self, 'of%d' % bdw), 
                    text=button_label[idx], width=10, command=actions[idx], font=ft))
                buttons[idx].pack(side=tk.LEFT, padx=7, pady=7)
                idx += 1
            getattr(self, 'of%d' % bdw).pack()
        buttons[0].focus_set()
        buttons[1].config(state=tk.DISABLED)
        for i in range(4):
            buttons[i].bind('<Key-Return>',actions[i])

    def Quit(self, event=None):
        self.destroy()
        root.destroy()
        sys.exit()
        
    def __init__(self, master):
        tk.Frame.__init__(self, master)
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

class MyDialog(tk.Frame):
    def __init__(self, master=None):
        global userpass
        tk.Frame.__init__(self, master)
        self.v1 = tk.StringVar()
        self.v2 = tk.StringVar()
        l1=tk.Label(self,text="账号:")
        l1.grid(row=0,column=0)
        self.e1=tk.Entry(self, textvariable=self.v1)
        self.e1.grid(row=0,column=1)
        l2=tk.Label(self,text="密码:")
        l2.grid(row=1,column=0)
        self.e2=tk.Entry(self,show="*", textvariable=self.v2)
        self.e2.grid(row=1,column=1)
        self.e2.bind('<Key-Return>', self.Ok)
        self.e1.focus_set()
        b1=tk.Button(self,text='确定', command=self.Ok)
        b1.grid(row=2,column=0)
        b2=tk.Button(self,text='取消', command=self.Cancel)
        b2.grid(row=2,column=1)
        
        self.userpass = main.readconf()
        if self.userpass is not 8:
            # self.v1.set(self.userpass[0])
            # self.v2.set(self.userpass[1])
            self.e1.insert(0,self.userpass[0])
            self.e1.select_range(0,tk.END)
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
    root2=tk.Tk()
    myapp = MyDialog(root2)
    myapp.master.title("请输入账号密码：")
    # myapp.master.maxsize(1000, 400)
    myapp.mainloop()
    # print(userpass,'g')
    return userpass
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    userpass = main.loadconf(getUserpass)
    app.mainloop()
    # root.destroy()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
