#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''
lzuauto - 兰大上网认证系统自动登录工具。
    
主要功能
    
    一键登录/退出、流量查询（支持验证码识别）
    
使用方法
    
    解压后，修改conf.txt，把自己的用户名密码填入。 运行 main.exe或main.pyw 即可。
    
系统要求
    
    Linux下需要的依赖：
    
        python(py2.5以上，支持python3)
        pygtk
        tesseract(ocr工具，主页 http://code.google.com/p/tesseract-ocr/ )
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
        
    Windows下需要的依赖：
    
        python-2.5.4.msi
        pycairo-1.4.12-2.win32-py2.5.exe
        pygobject-2.14.2-2.win32-py2.5.exe
        pygtk-2.12.1-1.win32-py2.5.exe
        
    以上软件请到分别下列地址下载：
    
        http://www.python.org/
        http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/
        http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/
        http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/
        
'''

__author__= 'ysjdxcn'
__copyright__ = 'Copyright 2010 ysjdxcn & Kder'
__credits__ = ['ysjdxcn','Kder']

__maintainer__ = ['ysjdxcn','Kder']
__email__ = ['ysjdxcn (#)gmail dot com', 'kderlin (#)gmail dot com']
__url__ = ['http://ranhouzenyang.com/', 'http://www.kder.info']
__license__ = 'GNU General Public License v3'
__status__ = 'Release'
__projecturl__ = 'http://code.google.com/p/lzuauto/'

__revision__ = "$Revision$"
__version__ = '1.1.2'
__date__ = '$Date: 2010-10-22 17:53:48 +0800 (星期五, 2010-10-22)$'

import os
import sys
import subprocess
import time
import urllib.parse
import http.client
import string
import re


########################################################################


CHK_COUNT = 0

ERR_CONF = '无法打开配置文件conf.txt或者文件格式错误，请确认文件存在，且格式为 邮箱 密码'
ERR_AUTH = '请检查conf.txt中的邮箱和密码是否正确(格式为"邮箱 密码"，不含引号)'
ERR_OCR = '请检查conf.txt中的邮箱和密码是否正确；如果设置正确，请稍候再试一次'
ERR_TESSERACT = 'tesseract错误，请确认tesseract是否正确安装'
ERR_DJPEG = 'djpeg错误，请确认libjpeg是否正确安装且djpeg命令可用'
ERR_IO = '文件写入错误，请确认程序所在目录有读写权限'
MSG_FLOW = '您本月已经使用的流量为 %s MB\n您本月已经上网 %s 小时'
MSG_LOGIN = "登录成功^_^ %s"
MSG_LOGOUT = '您已经成功退出:-)\n'
TITLE_LOGIN = '登录成功'
TITLE_LOGOUT = "退出外网"
TITLE_ABOUT = '关于'
TITLE_USAGE = '用法'
TITLE_ERR = '错误'
TITLE_FLOW = '流量查询'

option = 'alert(.*?);'
option1 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)MB'
option2 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)Hours'
option3 = '<font color=red>(.*?)</font>'

def loadconf():
    try:
        f = open('conf.txt')
        userid, passwd = re.split('\s+', f.readline().strip(), maxsplit=1)
#        print((userid,passwd))
        f.close()
    except:
        return 8
    return userid, passwd

def login(userpass):
    (userid, passwd) = userpass
    params = urllib.parse.urlencode({'userid':userid,'password':passwd,
    'serivce':'intenet','chap':'0','random':'internet','x':'25','y':'12'})
    headers = {"Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/plain"}
    conn = http.client.HTTPConnection("1.1.1.1")
    conn.request("POST", "/passwd.magi", params, headers)
    response = conn.getresponse()
    data = response.read().decode('gb2312')
    conn.close()
    #print data
    result = re.findall(option, data)
    if len(result)>0:
        return result[0].split('\"')[1]
    else :
        return 1

def logout():
    params = urllib.parse.urlencode({'imageField.x':'44','imageField.y':'27'})
    headers = {"Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/plain"}
    conn = http.client.HTTPConnection("1.1.1.1")
    conn.request("POST", "/userout.magi", params, headers)
    response = conn.getresponse()
    conn.close()
    if response.status == 200:
        return 1
    else :
        return 0

def ocr(data):
    '''input: jpeg image string stream
       output: ocr result string
    '''
    try:
        img_name = 'code.jpg'
        img_file = open(img_name, 'wb')
        img_file.write(data)
        img_file.close()
    except:
        return 5

    #~ s = image_to_string(image)[:4]
#    image = Image.fromstring('RGB',(60,20),data,'jpeg','RGB','RGB')#
#    print image.info
#    enhancer = ImageEnhance.Sharpness(image)
#    enhancer = ImageEnhance.Color(image)
#    for i in range(8):
#        factor = i / 4.0
#        enhancer.enhance(factor).show("Sharpness %f" % factor)

#    from StringIO import StringIO
#    import Image
#    import ImageEnhance
#    f = StringIO(data)
#    image = Image.open(f)
#    enhancer = ImageEnhance.Contrast(image)
#    image = enhancer.enhance(2.0)
#    img_name = 'code.bmp'
#    image.save(img_name,format = 'bmp')

    if os.name == 'posix':
        try:
            subprocess.Popen('djpeg -bmp code.jpg > code.bmp', shell=True)
            img_name = 'code.bmp'
        except:
            return 6
    args = ['tesseract %s ocr' % img_name]
    #~ print os.getcwd(),args
    proc = subprocess.Popen(args, shell=True)
    retcode = proc.wait()
    if retcode!=0:
        return 7
    f = open('ocr.txt','r')
    s = f.read().strip()
    f.close()
#    sys.exit(-1)
    try:
        os.remove(img_name)
        os.remove('ocr.txt')
    except:
        pass
    
    return s
    

def verify(userpass, headers):

    (userid, passwd) = userpass
    conn1 = http.client.HTTPConnection("a.lzu.edu.cn")
    conn1.request('GET', '/servlet/AuthenCodeImage', headers = headers)
    response1 = conn1.getresponse()
    #print response1.getheaders()
    data = response1.read()
    conn1.close()
    s = ocr(data)
    if type(s) is not type(str()):
        return s
    conn2 = http.client.HTTPConnection("a.lzu.edu.cn")
    params = urllib.parse.urlencode({'user_id':userid,'passwd':passwd,'validateCode':s})
    #print params
    conn2.request('POST', '/selfLogonAction.do', params, headers = headers)
    response2 = conn2.getresponse()
    data = response2.read().decode('gb2312')
    conn2.close()
    
    err = re.findall(option3, data)
#    if 'selfLogon' in response2.getheaders()[3][1]:
    print(err)
    return err
#    sys.exit()

def checkflow(userpass):
    (userid, passwd) = userpass
    headers = {"User-Agetn":"Mozilla/5.0 (X11; U; Linux i686; en-US; \
rv:1.9.2.10)Gecko/20101020 Firefox/3.6.11",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
*/*;q=0.8",
    "Keep-Alive":"115",
    "Connection":"keep-alive"}
    
    conn = http.client.HTTPConnection("a.lzu.edu.cn")
    conn.request('GET', '/', headers = headers)
    response = conn.getresponse()
    #print response.getheaders()
    cookie = response.getheader('set-cookie').split()[0]
    temp = {'Cookie':cookie}
    headers.update(temp)
    conn.close()

    conn0 = http.client.HTTPConnection("a.lzu.edu.cn")
    conn0.request('GET', '/selfLogon.do', headers = headers)
    response0 = conn0.getresponse()
    #print response0.getheaders()
    conn0.close()

    for i in range(5):
        res = verify((userid, passwd), headers)
        if res == []:
            break
        elif res[0] == '验证码错误，请重新提交。':
            time.sleep(0.2)
            continue
        else:
            return res[0] + '\n' + str(ERR_AUTH, 'utf-8')

    conn3 = http.client.HTTPConnection("a.lzu.edu.cn")
    conn3.request('GET', '/selfIndexAction.do',headers = headers)
    response3 = conn3.getresponse()
    data = response3.read()
#    print data
    conn3.close()

    conn4 = http.client.HTTPConnection("a.lzu.edu.cn")
    conn4.request('GET', '/userQueryAction.do',headers = headers)
    response4 = conn4.getresponse()
    data = response4.read().decode('gb2312')
    conn4.close()
#    print data[0]
    mb = re.findall(option1,data)
    hour = re.findall(option2,data)

    if len(mb)>0:
        MB = mb[0].split('&nbsp')[0][1:]
        HOUR = hour[0].split('&nbsp')[0]
#        print MB,HOUR
        return (MB, HOUR)


def checkstatus():
    pass

#######################################################################

if __name__ == "__main__":
    try:
        import pygtk
        import pango
        pygtk.require('2.0')
    except:
        sys.stdout.write('pygtk 2.0 needed')
        sys.exit(1)

    try:
        import gtk
    except Exception as e:
        #print e
        sys.stdout.write('gtk needed')
        sys.exit(2)


    class Interface:
        '''interface:
        The interface of this.'''
        
        ui = '''<ui>
        <menubar name="MenuBar">
          <menu action="File">
            <menuitem action="Quit"/>
          </menu>
          <menu action="Help">
            <menuitem action="About"/>
            <menuitem action="Usage"/>
          </menu>
        </menubar>
        </ui>'''
        
        def login(self, widget, data=None):
            #print 'login'
            if loadconf()== 8:
                start.Dialog(TITLE_ERR, ERR_CONF, icon = gtk.MESSAGE_ERROR)
            result = login(loadconf())
            if result is 1 or 'M)' in result:
                self.Dialog(TITLE_LOGIN, MSG_LOGIN % result)
            else:
                self.Dialog(TITLE_ERR, result, icon = gtk.MESSAGE_ERROR)
        
        def logout(self, widget, data=None):
            #print 'logout'
            if logout():
                self.Dialog(TITLE_LOGOUT, MSG_LOGOUT)
            else :
                self.logout

        def checkflow(self, widget, data=None):
            if loadconf()== 8:
                start.Dialog(TITLE_ERR, ERR_CONF, icon = gtk.MESSAGE_ERROR)
            flow = checkflow(loadconf())
            if type(flow)is type(tuple()):
                self.Dialog(TITLE_FLOW, MSG_FLOW % flow)
            elif type(flow)is type(str()):
                self.Dialog(TITLE_ERR, flow, icon = gtk.MESSAGE_ERROR)
            elif flow is 1:
                self.Dialog(TITLE_ERR, ERR_OCR, icon = gtk.MESSAGE_ERROR)
                sys.exit(4)
            elif flow is 5:
                self.Dialog(TITLE_ERR, ERROR_IO, icon = gtk.MESSAGE_ERROR)
            elif flow is 6:
                self.Dialog(TITLE_ERR, ERR_DJPEG, icon = gtk.MESSAGE_ERROR)
            elif flow is 7:
                self.Dialog(TITLE_ERR, ERR_TESSERACT, icon = gtk.MESSAGE_ERROR)
                        
        def Dialog(self, title, data=None, icon = gtk.MESSAGE_INFO):
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, icon, 
                                       gtk.BUTTONS_NONE, data)
            dialog.set_position(gtk.WIN_POS_CENTER)
            dialog.set_title(title)
            #dialog.format_secondary_text('comments')
            dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
            dialog.run()
            dialog.destroy()

        def DestroyAll(self, widget, data=None):
            gtk.main_quit()

        def About(self, widget):
            about = gtk.AboutDialog()
            about.set_program_name("lzuauto")
            about.set_version('%s.%s' % (__version__, 
            __revision__.split(':')[1][:-1].strip()))
            about.set_copyright("(c)ysjdxcn & Kder")
            about.set_license('GNU General Public License v3')
    #        about.set_wrap_license(1)
            about.set_authors(['ysjdxcn <ysjdxcn (#)gmail dot com>',
            'Kder <kderlin (#)gmail dot com>'])
            about.set_comments("兰大上网认证系统自动登录工具\n欢迎使用此工具，\
如果您有任何意见或者建议，请访问项目主页")
            about.set_website("http://code.google.com/p/lzuauto/")
            about.set_website_label("项目主页：http://lzuauto.googlecode.com")
    #        about.set_logo(gtk.gdk.pixbuf_new_from_file("code.jpg"))
            about.set_position(gtk.WIN_POS_CENTER)
            about.run()
            about.destroy()
        
        def Usage(self, widget):
            dialog = gtk.Dialog(TITLE_USAGE, None, 
            gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK))
            data = "%s" % __doc__
            buffer = gtk.TextBuffer()
            buffer.set_text(data)
            textview = gtk.TextView(buffer)
            textview.set_editable(False)
            dialog.vbox.pack_start(textview)
    #        textview.modify_font(pango.FontDescription("sans 10"))
            textview.show()
            dialog.run()
            dialog.destroy()
            
        def __init__(self):
            win = gtk.Window(gtk.WINDOW_TOPLEVEL)
            win.connect('destroy', lambda wid: gtk.main_quit())
            win.connect('delete_event', lambda a1,a2:gtk.main_quit())
            win.set_title('兰州大学校园网工具')
            win.set_size_request(200, 100)
            win.set_position(gtk.WIN_POS_CENTER)

            main_vbox = gtk.VBox(False, 0)
            main_hbox1 = gtk.HBox(False, 0)
            main_hbox2 = gtk.HBox(False, 0)

            uimanager = gtk.UIManager()
            accelgroup = uimanager.get_accel_group()
            win.add_accel_group(accelgroup)
            actiongroup = gtk.ActionGroup('UIManagerExample')
            self.actiongroup = actiongroup
            actiongroup.add_actions([('Quit', gtk.STOCK_QUIT, '退出(_Q)',
                                       None, '退出', self.DestroyAll),
                                      ('About', gtk.STOCK_ABOUT, '关于(_A)',
                                       None, TITLE_ABOUT, self.About),
                                      ('Usage', gtk.STOCK_INFO, '用法(_U)',
                                       None, TITLE_USAGE, self.Usage),
                                     ('File', gtk.STOCK_FILE, '文件(_F)'),
                                     ('Help', gtk.STOCK_HELP, '帮助(_H)'),
                                     ])
            actiongroup.get_action('Quit').set_property('short-label', '_Quit')

            uimanager.insert_action_group(actiongroup, 0)
            uimanager.add_ui_from_string(self.ui)
            menubar = uimanager.get_widget('/MenuBar')
            main_vbox.pack_start(menubar, False)

            image = []
            stocks = [gtk.STOCK_CONNECT, gtk.STOCK_DISCONNECT, gtk.STOCK_INFO, 
                      gtk.STOCK_QUIT]
            button = []
            button_label = ["登录外网", "退出外网", "查询流量", "退出程序"]
            actions = [self.login, self.logout, self.checkflow, self.DestroyAll]
            for i in range(4):
                image.append(gtk.Image())
                button.append(gtk.Button(button_label[i]))
                button[i].connect("clicked", actions[i], button_label[i])
                image[i].set_from_stock(stocks[i], gtk.ICON_SIZE_BUTTON)
                button[i].set_image(image[i])

    #        main_vbox.pack_start(button1, True, True, 0)
    #        main_vbox.pack_start(button2, True, True, 3)
    #        main_vbox.pack_start(button3, True, True, 0)
    #        main_vbox.pack_start(button4, True, True, 0)

            main_hbox1.pack_start(button[0], True, True, 3)
            main_hbox1.pack_start(button[2], True, True, 3)
            main_hbox2.pack_start(button[1], True, True, 3)
            main_hbox2.pack_start(button[3], True, True, 3)
            
            main_vbox.pack_start(main_hbox1, True, True, 3)
            main_vbox.pack_start(main_hbox2, True, True, 3)
            
    #        table = gtk.Table(2, 2, True)
    #        table.set_size_request(190, 110)
    #        table.attach(button1,0,1,0,1,gtk.FILL, gtk.FILL, 0, 0)
    #        table.attach(button2,0,1,1,2,gtk.FILL, gtk.FILL, 0, 0)
    #        table.attach(button3,1,2,0,1,gtk.FILL, gtk.FILL, 0, 0)
    #        table.attach(button4,1,2,1,2,gtk.FILL, gtk.FILL, 0, 0)
    #        win.add(table)
            
            win.add(main_vbox)
            win.modify_font(pango.FontDescription("sans 9"))
            win.show_all()


    start = Interface()
    if loadconf()is 8:
        start.Dialog(TITLE_ERR, ERR_CONF, icon = gtk.MESSAGE_ERROR)
        sys.exit(3)
    gtk.main()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4