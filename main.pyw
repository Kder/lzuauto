#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''
lzuauto - 兰大上网认证系统自动登录工具。

主要功能

    一键登录/退出、流量查询（支持验证码识别）

使用方法

    解压后，第一次运行 main.exe（或main.pyw），会弹出对话框，把自己的账号密码填入，
    确定，然后点击“登录外网”即可。

运行源码版的系统要求

    Linux下需要的依赖：

        python(py2.6以上,支持python3)
        pygtk或者Tcl/tk
        tesseract(ocr工具，主页 http://code.google.com/p/tesseract-ocr/ )
        各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。

    Windows下需要的依赖：
        python2.6/2.7，或Python3（仅支持tk界面） http://www.python.org

        以下4个仅GTK界面需要
            pycairo http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/
            pygobject http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/
            pygtk http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/
            GTK+(All-in-one bundles) http://www.gtk.org/download-windows.html

'''

__author__ = ['ysjdxcn', 'Kder']
__copyright__ = 'Copyright 2010 ysjdxcn & Kder'
__credits__ = ['ysjdxcn', 'Kder']

__maintainer__ = ['ysjdxcn', 'Kder']
__email__ = ['ysjdxcn (#)gmail dot com', 'kderlin (#)gmail dot com']
__url__ = ['http://ranhouzenyang.com/', 'http://www.kder.info']
__license__ = 'GNU General Public License v3'
__status__ = 'Release'
__projecturl__ = 'http://code.google.com/p/lzuauto/'

__revision__ = "$Revision$"
__version__ = '1.3.1'
__date__ = '$Date: 2010-10-22 17:53:48 +0800 (星期五, 2010-10-22)$'

import os
import sys
import subprocess
import time
try:
    import urllib.parse as urlparse
    import http.client as http
except:
    import urllib as urlparse
    import httplib as http
import string
import re
import random


CHK_COUNT = 0

lzuauto_text = {
'ERR_CONF': '无法打开配置文件conf.txt或者文件格式错误，请确认文件存在，且格式为 邮箱 密码',
'ERR_AUTH': '请检查conf.txt中的邮箱和密码是否正确(格式为"邮箱 密码"，不含引号)',
'ERR_OCR': '请检查conf.txt中的邮箱和密码是否正确；如果设置正确，请稍候再试一次',
'ERR_TESSERACT': 'tesseract错误，请确认tesseract是否正确安装',
'ERR_DJPEG': 'djpeg错误，请确认libjpeg是否正确安装且djpeg命令可用',
'ERR_IO': '文件写入错误，请确认程序所在目录有读写权限',
'ERR_CODECHECK': '验证码错误，请重新提交。',
'MSG_FLOW': '您本月已经使用的流量为 %s MB\n您本月已经上网 %s 小时',
'DRCOM_MSG_TIME': '本帐号已使用时间: %d天 %d小时 %d分钟\n',
'DRCOM_MSG_FLOW':  '本帐号已使用流量: %dT %dG %.3fM Bytes\n',
'MSG_LOGIN': "登录成功^_^ %s",
'MSG_LOGOUT': '您已经成功退出:-)\n',
'TITLE_LOGIN': '登录成功',
'TITLE_LOGOUT': "退出外网",
'TITLE_ABOUT': '关于',
'TITLE_USAGE': '用法',
'TITLE_ERR': '错误',
'TITLE_FLOW': '流量查询',
}
TFMMSG = {0: '',
          2: "该账号正在使用中，请您与网管联系 !!!\n",
          3: "本帐号只能在指定地址使用\n",  # :+pp+xip
          4: "本帐号费用超支\n",
          5: "本帐号暂停使用\n",
          6: "System buffer full\n",
          #7: UT+UF+UM,
          8: "本帐号正在使用,不能修改\n",
          9: "新密码与确认新密码不匹配,不能修改\n",
          10: "密码修改成功\n",
          11: "本帐号只能在指定地址使用\n",  # :+pp+mac
          14: "注销成功 Logout successfully\n",
          15: "登录成功 Login successfully\n",
          'error0': "本 IP 不允许Web方式登录\n",
          'error1': "本帐号不允许Web方式登录\n",
          'error2': "本帐号不允许修改密码\n",
          'error_userpass': '帐号或密码不对，请重新输入\n',
          'find1': '本帐号',
}
option = "alert\((.*?)\);"
# option = "'\(.*?\)'"
option1 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)MB'
option2 = '<td bgcolor=\"FFFBF0\" align=\"center\" colspan=5>(.*?)Hours'
option3 = '<font color=red>(.*?)</font>'
# path0 = os.path.dirname(sys.path[0])
path0 = sys.path[0]
if os.path.isdir(sys.path[0]):
    PROGRAM_PATH = path0
else:
    PROGRAM_PATH = os.path.dirname(path0)
#    PROGRAM_PATH = os.path.join(path0, os.pardir)

CONF = PROGRAM_PATH + os.sep + 'conf.txt'
CONF2 = PROGRAM_PATH + os.sep + 'lzuauto.ini'
isPy2 = False
if sys.version_info.major is 2:
    isPy2 = True
    for i in lzuauto_text:
        lzuauto_text[i] = unicode(lzuauto_text[i], 'utf-8')
    for i in TFMMSG:
        TFMMSG[i] = unicode(TFMMSG[i], 'utf-8')


def readconf():
    if os.path.exists(CONF):
        f = open(CONF)
        userpass = f.readline().strip()
        userpass = re.split('\s+', userpass, maxsplit=1)
        f.close()
        # print(userpass)
        if isinstance(userpass, list) and len(userpass) > 1:
            return userpass
    else:
        return 8


def loadconf(getuserpass):
    try:
        userpass = readconf()
        if userpass is 8 or userpass[0] == 'test@lzu.cn':
            userpass = getuserpass(None)
            # print(userpass,'l')
        return userpass
    except:  # Exception as e:
#        print(e)
        return 8

#Get the IP address of local machine
#code from:
# http://hi.baidu.com/yangyingchao/blog/item/8d26b544f6059f45500ffe78.html


# for Linux
def get_ip_address(ifname):
    import socket
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#get_ip_address('lo')
#get_ip_address('eth0')


# for Windows
def getIPAddresses():
    from ctypes import Structure, windll, sizeof
    from ctypes import POINTER, byref
    from ctypes import c_ulong, c_uint, c_ubyte, c_char
    MAX_ADAPTER_DESCRIPTION_LENGTH = 128
    MAX_ADAPTER_NAME_LENGTH = 256
    MAX_ADAPTER_ADDRESS_LENGTH = 8

    class IP_ADDR_STRING(Structure):
        pass
    LP_IP_ADDR_STRING = POINTER(IP_ADDR_STRING)
    IP_ADDR_STRING._fields_ = [
        ("next", LP_IP_ADDR_STRING),
        ("ipAddress", c_char * 16),
        ("ipMask", c_char * 16),
        ("context", c_ulong)]

    class IP_ADAPTER_INFO (Structure):
        pass
    LP_IP_ADAPTER_INFO = POINTER(IP_ADAPTER_INFO)
    IP_ADAPTER_INFO._fields_ = [
        ("next", LP_IP_ADAPTER_INFO),
        ("comboIndex", c_ulong),
        ("adapterName", c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
        ("description", c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
        ("addressLength", c_uint),
        ("address", c_ubyte * MAX_ADAPTER_ADDRESS_LENGTH),
        ("index", c_ulong),
        ("type", c_uint),
        ("dhcpEnabled", c_uint),
        ("currentIpAddress", LP_IP_ADDR_STRING),
        ("ipAddressList", IP_ADDR_STRING),
        ("gatewayList", IP_ADDR_STRING),
        ("dhcpServer", IP_ADDR_STRING),
        ("haveWins", c_uint),
        ("primaryWinsServer", IP_ADDR_STRING),
        ("secondaryWinsServer", IP_ADDR_STRING),
        ("leaseObtained", c_ulong),
        ("leaseExpires", c_ulong)]
    GetAdaptersInfo = windll.iphlpapi.GetAdaptersInfo
    GetAdaptersInfo.restype = c_ulong
    GetAdaptersInfo.argtypes = [LP_IP_ADAPTER_INFO, POINTER(c_ulong)]
    adapterList = (IP_ADAPTER_INFO * 10)()
    buflen = c_ulong(sizeof(adapterList))
    rc = GetAdaptersInfo(byref(adapterList[0]), byref(buflen))
    if rc == 0:
        for a in adapterList:
            adNode = a.ipAddressList
            if isPy2:
                while True:
                    ipAddr = adNode.ipAddress
                    if ipAddr:
                        yield ipAddr
                    adNode = adNode.next
                    if not adNode:
                        break
            else:
                ipAddr = adNode.ipAddress
                if ipAddr:
                    yield ipAddr


def get_ip():
    if sys.platform == 'win32':
        return [x for x in getIPAddresses()]
    else:
        return get_ip_address('eth0')

ip = get_ip()[0]


def get_http_res(host, path, params=None, headers=None):
    conn = http.HTTPConnection(host)
    if params:
        conn.request('POST', path, params, headers)
    else:
        conn.request('GET', path, headers=headers)
    response = conn.getresponse()
    data = response.read().decode('gb2312')
    conn.close()
    return data


def DispTFM(Msg, msga):
    if int(Msg) == 1:
        if msga != '':
            try:
                return(TFMMSG[msga])
            except KeyError:
                return(msga + '\n')
        else:
            return(TFMMSG['error_userpass'])
    else:
        return(TFMMSG[int(Msg)])


def process_ret(ret):
    msg = re.findall("Msg=([\d.]+);", ret)
    msga = re.findall("msga='(.*)'", ret)
    # print msg,msga,ret
    msg1 = ''
    if msg != [] and msga != []:
        msg1 = DispTFM(msg[0], msga[0])
        if msg1 == TFMMSG['error_userpass']:
            return msg1
        # if DispTFM(msg[0], msga[0]) != 0:
            # return -1
    flow = re.findall("flow='([\d.]+)\s*'", ret)
    time = re.findall("time='([\d.]+)\s*'", ret)
    if flow != [] and time != []:
        time = int(time[0])  # unit is minute
        flow = int(flow[0])  # unit is kbyte
#        flow0=flow % 1024; flow1=flow - flow0; flow0 = flow0 * 1000;
#        flow0 = flow0 - flow0 % 1024
#        flow0 = (flow % 1024) * 1000 - ((flow % 1024) * 1000) % 1024
#        flow_kb = flow - flow % 1024
#        flow0mb = flow % 1024 / 1024.0
        days = time / 60 / 24
        hours = time / 60 % 24
        minutes = time % 60
        flow_tb = flow / 1073741824
        flow_gb = flow % 1073741824 / 1048576
        flow_mb = flow / 1024 % 1024 + flow % 1024 / 1024.0
        time_flow = lzuauto_text['DRCOM_MSG_TIME'] % (days, hours, minutes) \
         + lzuauto_text['DRCOM_MSG_FLOW'] % (flow_tb, flow_gb, flow_mb)
    else:
        time_flow = ''
    return msg1 + time_flow


def login(userpass):
    params = urlparse.urlencode({'DDDDD': userpass[0],
            'upass': userpass[1],
            '0MKKey': '登录 Login',
            'v6ip': ''})
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        'Referer': 'http://10.10.0.202/'
        }
    data = get_http_res('10.10.0.202', '/', params, headers)
    ret = process_ret(data)
    if len(ret) == 0:
        data = get_http_res('10.10.0.202', '/', headers=headers)
        ret = process_ret(data)
    return ret


def logout():
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        'Referer': 'http://10.10.0.202:9002/0'
        }
    data = get_http_res('10.10.0.202', '/F.htm', headers=headers)
    return 1


# def login(userpass):
    # (userid, passwd) = userpass
    # params = urlparse.urlencode({'wlanuserip':ip,'wlanacname':'BAS_138',
    # 'auth_type':'PAP','wlanacIp':'202.201.1.138','userid':userid,
#    'passwd':passwd,'chal_id':'','chal_vector':'','seq_id':'','req_id':''})
    # headers = {"Content-type": "application/x-www-form-urlencoded",
    # "Accept": "text/plain"}
    # data = get_http_res("202.201.1.140", "/portalAuthAction.do",
#    params, headers)
    # result = re.findall(option, data)
    # if len(result)>0:
        # if result[0] == 'temp':
            # result = re.findall("var temp=('.+?')", data)
            # usertime = re.findall('''"usertime" value='(\d+)''', data)[0]
            # try:
                # with open('lzuauto.ini','w') as f:
                    # f.write(usertime)
            # except:
                # pass
        # return result[0].strip("'")  # .split('\'')[1]
    # else:
        # return 1

# def logout():
    # usertime = None
    # try:
        # with open(CONF2,'r') as f:
            # usertime = f.readline().strip()
    # except:
        # pass
    ## x <- (0,180) y <- (0,50)
    # x = random.randrange(0,180)
    # y = random.randrange(0,50)
    # params = urlparse.urlencode({'wlanuserip':ip,'wlanacname':'BAS_138',
#   'wlanacIp':'202.201.1.138','portalUrl':'','usertime':usertime or '3146400',
    # 'imageField.x':x,'imageField.y':y})
    # headers = {"Content-type": "application/x-www-form-urlencoded",
    # "Accept": "text/plain"}
    # conn = http.HTTPConnection("202.201.1.140")
    # conn.request("POST", "/portalDisconnAction.do", params, headers)
    # response = conn.getresponse()
    # conn.close()
    # if response.status == 200:
        # return 1
    # else:
        # return 0

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
    os.environ['TESSDATA_PREFIX'] = PROGRAM_PATH + os.sep
    args = [PROGRAM_PATH + os.sep + 'tesseract', img_name,
            'ocr', 'nobatch', 'digits']
    #~ print os.getcwd(),args
    proc = subprocess.Popen(args, shell=True)
    retcode = proc.wait()
    if retcode != 0:
        return 7
    f = open('ocr.txt', 'r')
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
    data = get_http_res('a.lzu.edu.cn', '/servlet/AuthenCodeImage',
        headers=headers)
    s = ocr(data)
    if type(s) is not type(str()):
        return s
    params = urlparse.urlencode({'user_id': userid, 'passwd': passwd,
                                'validateCode': s})
    data = get_http_res('a.lzu.edu.cn', '/selfLogonAction.do', params,
                headers)
    err = re.findall(option3, data)
#    if 'selfLogon' in response2.getheaders()[3][1]:
#    print(err)
    return err
#    sys.exit()


def checkflow(userpass):
    (userid, passwd) = userpass
    headers = {"User-Agetn": "Mozilla/5.0 (X11; U; Linux i686; en-US; \
rv:1.9.2.10)Gecko/20101020 Firefox/3.6.11",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
*/*;q=0.8",
    "Keep-Alive": "115",
    "Connection": "keep-alive"}

    conn = http.HTTPConnection("a.lzu.edu.cn")
    conn.request('GET', '/', headers=headers)
    response = conn.getresponse()
    #print response.getheaders()
    cookie = response.getheader('set-cookie').split()[0]
    temp = {'Cookie': cookie}
    headers.update(temp)
    conn.close()

    get_http_res("a.lzu.edu.cn", '/selfLogon.do', headers=headers)

    for i in range(5):
        res = verify((userid, passwd), headers)
        if res == []:
            break
        elif res[0] == lzuauto_text['ERR_CODECHECK']:
            time.sleep(0.2)
            continue
        else:
            return res[0] + '\n' + lzuauto_text['ERR_AUTH']

    get_http_res("a.lzu.edu.cn", '/selfIndexAction.do', headers=headers)
    data = get_http_res("a.lzu.edu.cn", '/userQueryAction.do',
        headers=headers)

    mb = re.findall(option1, data)
    hour = re.findall(option2, data)

    if len(mb) > 0:
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
          <menu action="Settings">
            <menuitem action="Userpass"/>
          </menu>
          <menu action="Help">
            <menuitem action="About"/>
            <menuitem action="Usage"/>
          </menu>
        </menubar>
        </ui>'''

        def login(self, widget, data=None):
            #print 'login'
            userpass = loadconf(getUserpass)
            result = login(userpass)
            if result is 1 or 'M)' in result:
                self.Dialog(lzuauto_text['TITLE_LOGIN'],
                    lzuauto_text['MSG_LOGIN'] % result)
            elif TFMMSG['find1'] in result:
                self.Dialog(lzuauto_text['TITLE_LOGIN'],
                    TFMMSG[15] + result)
            else:
                self.Dialog(lzuauto_text['TITLE_ERR'], result,
                    icon=gtk.MESSAGE_ERROR)

        def logout(self, widget, data=None):
            #print 'logout'
            if logout():
                self.Dialog(lzuauto_text['TITLE_LOGOUT'],
                    lzuauto_text['MSG_LOGOUT'])
            else:
                self.logout

        def checkflow(self, widget, data=None):
            userpass = loadconf(getUserpass)
            flow = checkflow(userpass)
            if type(flow) is type(tuple()):
                self.Dialog(lzuauto_text['TITLE_FLOW'],
                    lzuauto_text['MSG_FLOW'] % flow)
            elif flow is 1:
                self.Dialog(lzuauto_text['TITLE_ERR'],
                    lzuauto_text['ERR_OCR'], icon=gtk.MESSAGE_ERROR)
                sys.exit(4)
            elif flow is 5:
                self.Dialog(lzuauto_text['TITLE_ERR'],
                    lzuauto_text['ERROR_IO'], icon=gtk.MESSAGE_ERROR)
            elif flow is 6:
                self.Dialog(lzuauto_text['TITLE_ERR'],
                    lzuauto_text['ERR_DJPEG'], icon=gtk.MESSAGE_ERROR)
            elif flow is 7:
                self.Dialog(lzuauto_text['TITLE_ERR'],
                    lzuauto_text['ERR_TESSERACT'], icon=gtk.MESSAGE_ERROR)
            else:
                try:
                    if type(flow) is type(unicode()):
                        self.Dialog(lzuauto_text['TITLE_ERR'], flow, 'error')
                except:
                    if type(flow) is type(str()):
                        self.Dialog(lzuauto_text['TITLE_ERR'], flow, 'error')

        def Dialog(self, title, data=None, icon=gtk.MESSAGE_INFO):
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
            dialog = gtk.Dialog(lzuauto_text['TITLE_USAGE'], None,
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
            win.connect('delete_event', lambda a1, a2: gtk.main_quit())
            win.set_title('兰州大学上网认证工具')
            win.set_size_request(240, 120)
            win.set_position(gtk.WIN_POS_CENTER)

            main_vbox = gtk.VBox(False, 0)
            main_hbox1 = gtk.HBox(False, 0)
            main_hbox2 = gtk.HBox(False, 0)

            uimanager = gtk.UIManager()
            accelgroup = uimanager.get_accel_group()
            win.add_accel_group(accelgroup)
            actiongroup = gtk.ActionGroup('UIManagerExample')
            self.actiongroup = actiongroup
            actiongroup.add_actions(
            [('Quit', gtk.STOCK_QUIT, '退出(_Q)',
               None, '退出', self.DestroyAll),
             ('About', gtk.STOCK_ABOUT, '关于(_A)',
               None, lzuauto_text['TITLE_ABOUT'], self.About),
             ('Usage', gtk.STOCK_INFO, '用法(_U)',
               None, lzuauto_text['TITLE_USAGE'], self.Usage),
             ('Userpass', gtk.STOCK_DIALOG_AUTHENTICATION, '账号(_U)',
               None, lzuauto_text['TITLE_USAGE'], getUserpass),
             ('File', gtk.STOCK_FILE, '文件(_F)'),
             ('Settings', gtk.STOCK_PROPERTIES, '设置(_S)'),
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
            actions = [self.login, self.logout, self.checkflow,
                        self.DestroyAll]
            for i in range(4):
                image.append(gtk.Image())
                button.append(gtk.Button(button_label[i]))
                button[i].connect("clicked", actions[i], button_label[i])
                image[i].set_from_stock(stocks[i], gtk.ICON_SIZE_BUTTON)
                button[i].set_image(image[i])
            button[2].set_sensitive(False)
    #        main_vbox.pack_start(button1, True, True, 0)
    #        main_vbox.pack_start(button2, True, True, 3)
    #        main_vbox.pack_start(button3, True, True, 0)
    #        main_vbox.pack_start(button4, True, True, 0)

            main_hbox1.pack_start(button[0], True, True, 10)
            main_hbox1.pack_start(button[2], True, True, 10)
            main_hbox2.pack_start(button[1], True, True, 10)
            main_hbox2.pack_start(button[3], True, True, 10)

            main_vbox.pack_start(main_hbox1, True, True, 10)
            main_vbox.pack_start(main_hbox2, True, True, 10)

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

    def getUserpass(widget):
        def responseToDialog(entry, dialog, response):
            dialog.response(response)
        #base this on a message dialog
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK_CANCEL,
            None)

        dialog.set_default_response(gtk.RESPONSE_OK)

        # dialog.set_markup('请输入 <b>账号和密码</b>:')
        dialog.set_markup('请输入账号和密码:')
        # dialog.format_secondary_markup("<i>只需首次运行和要修改密码时输入</i>")
        dialog.format_secondary_markup("(只需首次运行和要修改密码时输入)")
        #create the text input field
        entry = gtk.Entry()
        entry_pass = gtk.Entry()
        entry_pass.set_visibility(False)

        userpass = readconf()
        if userpass is not 8:
            entry.set_text(userpass[0])
            entry_pass.set_text(userpass[1])
        #allow the user to press enter to do ok
        entry_pass.connect("activate", responseToDialog, dialog,
                            gtk.RESPONSE_OK)
        #create a horizontal box to pack the entry and a label
        hbox1 = gtk.HBox()
        hbox2 = gtk.HBox()
        hbox1.pack_start(gtk.Label("账号:"), False, 5, 5)
        hbox1.pack_end(entry)
        hbox2.pack_start(gtk.Label("密码:"), False, 5, 5)
        hbox2.pack_end(entry_pass)
        #some secondary text
        #add it and show it
        dialog.vbox.pack_start(hbox1, True, True, 0)
        dialog.vbox.pack_start(hbox2, True, True, 0)
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.show_all()
        #go go go
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            userpass = (entry.get_text(), entry_pass.get_text())
            if '' not in userpass:
                with open(CONF, 'w') as f:
                    f.write('%s %s' % userpass)
        dialog.destroy()
        return userpass

    start = Interface()
    loadconf(getUserpass)
    gtk.main()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
