#!/usr/bin/env python
#-*-coding=utf-8-*
from pytesser import *
import urllib, httplib, time, re, sys


try:
	import pygtk
	pygtk.require('2.0')
except:
	print 'pygtk 2.0 needed'
	sys.exit(1)

try:
	import gtk
except:
	print 'gtk needed'




############################################################################################################################
f = open('conf.txt')
userid, passwd = f.readline().split()
f.close()

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


############################################################################################################################




class Interface:
	'''interface:
	The interface of this.'''
	def login(self, widget, data=None):
		#print 'login'
		result = login()
		if result == 1 :
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


	def getMenu(self, window):
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		window.add_accel_group(accel_group)
		self.item_factory = item_factory
		return item_factory.get_widget("<main>")
	
	def Dialog(self, widget, data=None):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, data)
		dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
		dialog.run()
		dialog.destroy()

	def DestroyAll(self, widget, data=None):
		gtk.main_quit()

	def About(self, widget, data=None):
		dialog = gtk.Dialog('关于', None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_OK))
		label = gtk.Label()
		data = "欢迎使用此工具，如果您有任何意见或者建议\n请访问项目主页<a href='http://code.google.com/p/lzuauto/'>http://lzuauto.googlecode.com</a>\n"
		label.set_markup(data)
		dialog.vbox.pack_start(label)
		label.show()
		dialog.run()
		dialog.destroy()
	def __init__(self):
		win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		win.connect('destroy', lambda wid: gtk.main_quit())
		win.connect('delete_event', lambda a1,a2:gtk.main_quit())
		win.set_title('兰州大学校园网工具')
		win.set_size_request(160, 120)
		win.set_position(gtk.WIN_POS_CENTER)
		
		self.menu_items=(
				("/_File", None, None, 0, "<Branch>"),
				("/File/_Quit","<control>Q", self.DestroyAll, 0, None),
				("/_Help", None, None, 0, "<Branch>"),
				("/Help/_About", None, self.About, 0, None)
				)
		menubar = self.getMenu(win)
		
		button1 = gtk.Button("登录外网")
		button1.connect("clicked", self.login, "登录")

		button2 = gtk.Button("退出外网")
		button2.connect("clicked", self.logout, "登出")

		button3 = gtk.Button("查询流量")
		button3.connect("clicked", self.checkflow, "查询流量")
		
		button4 = gtk.Button("退出程序")
		button4.connect("clicked", self.DestroyAll)

		main_vbox = gtk.VBox(False, 0)
		main_vbox.pack_start(menubar, False, False, 0)
		main_vbox.pack_start(button1, True, True, 0)
		main_vbox.pack_start(button2, True, True, 0)
		main_vbox.pack_start(button3, True, True, 0)
		main_vbox.pack_start(button4, True, True, 0)
		
		
		win.add(main_vbox)
		win.show_all()


if __name__ == "__main__":
	start = Interface()
	gtk.main()
