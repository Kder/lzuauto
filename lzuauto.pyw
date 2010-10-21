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
        tcl和tk
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        python-2.5.4.msi
        PIL-1.1.7.win32-py2.5.exe
        
    以上软件请到分别下列地址下载：
    
        http://www.python.org
        http://www.pythonware.com/products/pil/
        
'''


import Tkinter
import tkMessageBox 
from idlelib import textView
import py_compile
py_compile.compile('main.pyw','main.pyc')

import main


rev = "$Revision$"
__version__ = '1.1.0' + ('.%s' % rev.split(':')[1][:-1].strip())


class Application(Tkinter.Frame):

    def login(self):
        result = main.login()
        if result is 1 or u'可用流量' in result:
            self.Dialog('登录成功', u"登录成功^_^ %s" % result)
        else:
            self.Dialog('错误', result, 'error')
 
    def logout(self):
        if main.logout():
            self.Dialog("退出外网", '您已经成功退出:-)\n')
        else :
            self.logout

    def checkflow(self):
        flow = main.checkflow()
#        print flow
        if type(flow) is type(tuple()):
            self.Dialog('流量查询', '您本月已经使用的流量为 %s MB\n您本月已经上网 %s 小时' % flow)
        elif flow is 1:
            self.Dialog('错误', '请检查conf.txt中的邮箱和密码是否正确', 'error')
            sys.exit(4)
        elif flow is None:
            self.Dialog('错误', '发生错误，请稍候再试', 'error')

    def Dialog(self, title=None, data=None, icon='info'):
        tkMessageBox.showinfo(title, data, icon=icon)
        
    def About(self, event=None):
        self.Dialog('关于', "lzuauto %s\n作者： ysjdxcn & Kder\n项目主页： http://code.google.com/p/lzuauto/ \nLicense : GPLv3" % __version__)
        
    def Usage(self, event=None):
        textView.view_text(self, '用法', __doc__)

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
    if main.IOERR:
        app.Dialog('错误', '无法打开配置文件conf.txt，请确认文件存在并有访问权限', 'error')
        sys.exit(3)
    app.mainloop()
    # root.destroy()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
