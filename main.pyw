#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''
lzuauto - 自动登录兰大上网认证系统。

主要功能

	一键登录/退出、流量查询（支持验证码识别）

使用方法

	解压后，修改conf.txt，把自己的用户名密码填入。 运行 main.pyw 就会出来主界面。

系统要求

	Linux下面需要的依赖：

		python(标准发行版里面的版本都应该支持，理论上不支持python3.0且未测试)
		pygtk
		python-imaging(PIL库)
		tesseract(一个ocr工具，项目主页 http://code.google.com/p/tesseract-ocr/ ）
		各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。
		
	Windows下需要的依赖：

		python-2.5.4.msi
		PIL-1.1.7.win32-py2.5.exe
		pycairo-1.4.12-2.win32-py2.5.exe
		pygobject-2.14.2-2.win32-py2.5.exe
		pygtk-2.12.1-1.win32-py2.5.exe
		
	以上软件请到分别下列地址下载：

		http://www.python.org
		http://www.pythonware.com/products/pil/
		http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/
		http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/
		http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/
'''

__author__= 'ysjdxcn'
__copyright__ = 'Copyright 2010 ysjdxcn & Kder'
__credits__ = ['ysjdxcn','Kder']
__version__ = '1.0.0'
__date__ = '2010-10-11'
__maintainer__ = ['ysjdxcn','Kder']
__email__ = ['ysjdxcn (#) gmail dot com', 'kderlin (#) gmail dot com']
__url__ = ['http://ranhouzenyang.com/', 'http://www.kder.info']
__license__ = 'GNU General Public License v3'
__status__ = 'Release'
__projecturl__ = 'http://code.google.com/p/lzuauto/'


from pytesser import *
import urllib, httplib, time, re, sys

import os

os.sys.path.append('.')
os.sys.path.append('./glib')
os.sys.path.append('./gtk')
os.sys.path.append('./gobject')

try:
	import pygtk
	pygtk.require('2.0')
except:
	print 'pygtk 2.0 needed'
	sys.exit(1)

try:
	import gtk
except Exception as e:
	print e
	print 'gtk needed'
	sys.exit(2)

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
		return re.findall(option,data)[0].split('\"')[1].decode('gb2312')
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
#	print data											  
	conn2.close()
	
	conn3 = httplib.HTTPConnection("a.lzu.edu.cn")
	conn3.request( 'GET', '/selfIndexAction.do',headers = headers)
	response3 = conn3.getresponse()
	data = response3.read()
#	print data
	conn3.close()

	conn4 = httplib.HTTPConnection("a.lzu.edu.cn")
	conn4.request( 'GET', '/userQueryAction.do',headers = headers)
	response4 = conn4.getresponse()
	data = response4.read()
	conn4.close()
	mb = re.findall(option1,data)
	hour = re.findall(option2,data)
	if len(mb)>0:
		global MB, HOUR
		MB = mb[0].split('&nbsp')[0][1:]
		HOUR = hour[0].split('&nbsp')[0]
	else :
		checkflow()

def checkstatus():
	pass

################################################################################

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
		result = login()
		if result == 1 or '0.00' in result:
			self.Dialog(None, "登录成功")
		else :
			self.Dialog(None, result)
	
	def logout(self, widget, data=None):
		#print 'logout'
		if logout():
			self.Dialog(None, data='您已经成功退出:-)\n')
		else :
			self.logout

	def checkflow(self, widget, data=None):
		#print 'checkflow'
		checkflow()
		self.Dialog(None, data='您本月已经使用的流量为 %s MB\n您本月已经上网 %s 小时' % (MB, HOUR))
	
	def Dialog(self, widget, data=None):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, data)
		dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
		dialog.run()
		dialog.destroy()

	def DestroyAll(self, widget, data=None):
		gtk.main_quit()

	def About(self, widget):
		about = gtk.AboutDialog()
		about.set_program_name("lzuauto")
		about.set_version("1.0")
		about.set_copyright("(c) ysjdxcn & Kder")
		about.set_license('GNU General Public License v3')
#		about.set_wrap_license(1)
		about.set_authors(['ysjdxcn <ysjdxcn (#) gmail dot com>','Kder <kderlin (#) gmail dot com>'])
		about.set_comments("自动登录兰大上网认证系统\n\n欢迎使用此工具，如果您有任何意见或者建议\n请访问项目主页")
		about.set_website("http://code.google.com/p/lzuauto/")
		about.set_website_label("项目主页：http://lzuauto.googlecode.com")
#		about.set_logo(gtk.gdk.pixbuf_new_from_file("code.jpg"))
		about.run()
		about.destroy()
	
	def Usage(self, widget):
		dialog = gtk.Dialog('用法', None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK))
		data = "%s" % __doc__
		buffer = gtk.TextBuffer()
		buffer.set_text(data)
		textview = gtk.TextView(buffer)
		textview.set_editable(False)
		dialog.vbox.pack_start(textview)
		textview.show()
		dialog.run()
		dialog.destroy()
		
	def __init__(self):
		win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		win.connect('destroy', lambda wid: gtk.main_quit())
		win.connect('delete_event', lambda a1,a2:gtk.main_quit())
		win.set_title('兰州大学校园网工具')
		win.set_size_request(200, 120)
		win.set_position(gtk.WIN_POS_CENTER)

		main_vbox = gtk.VBox(False, 0)

		uimanager = gtk.UIManager()
		accelgroup = uimanager.get_accel_group()
		win.add_accel_group(accelgroup)
		actiongroup = gtk.ActionGroup('UIManagerExample')
		self.actiongroup = actiongroup
		actiongroup.add_actions([('Quit', gtk.STOCK_QUIT, '退出(_Q)', None,
								  '退出', self.DestroyAll),
								  ('About', gtk.STOCK_ABOUT, '关于(_A)', None,
								  '关于', self.About),
								  ('Usage', gtk.STOCK_INFO, '用法(_U)', None,
								  '用法', self.Usage),
								 ('File', gtk.STOCK_FILE, '文件(_F)'),
								 ('Help', gtk.STOCK_HELP, '帮助(_H)'),
								 
								 ])
		actiongroup.get_action('Quit').set_property('short-label', '_Quit')

		uimanager.insert_action_group(actiongroup, 0)
		uimanager.add_ui_from_string(self.ui)
		menubar = uimanager.get_widget('/MenuBar')
		main_vbox.pack_start(menubar, False)


		button1 = gtk.Button("登录外网")
		button1.connect("clicked", self.login, "登录")

		button2 = gtk.Button("退出外网")
		button2.connect("clicked", self.logout, "登出")

		button3 = gtk.Button("查询流量")
		button3.connect("clicked", self.checkflow, "查询流量")
		
		button4 = gtk.Button("退出程序")
		button4.connect("clicked", self.DestroyAll)

		main_vbox.pack_start(button1, True, True, 0)
		main_vbox.pack_start(button2, True, True, 0)
		main_vbox.pack_start(button3, True, True, 0)
		main_vbox.pack_start(button4, True, True, 0)
		
		win.add(main_vbox)
		win.show_all()


if __name__ == "__main__":
	start = Interface()
	gtk.main()

#vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
