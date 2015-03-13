兰大上网认证系统自动登录工具，基于Python，跨平台。

### 主要功能 ###

一键登录/退出、流量查询（支持验证码识别）

### 使用方法 ###

解压后，运行 main.pyw或main.exe（GTK界面）或者 lzuauto.pyw或lzuauto.exe（Tk界面）。会弹出对话框，把自己的账号密码填入，确定，然后点击“登录外网”即可。

### 下载 ###
> Windows版（一般用户请下载这个）：
> > http://lzuauto.googlecode.com/files/lzuauto-1.3.1.109-win-gtk.zip


> 源代码版（Linux或者其他系统用户）：
> > http://lzuauto.googlecode.com/files/lzuauto-1.3.1.109-src.zip

### 运行源码版的系统要求 ###

Windows版本可以直接双击运行，如果要运行源代码版本，请参见此说明：http://code.google.com/p/lzuauto/wiki/SystemRequirements

### 更新日志 ###
  * 2011-01-15 ：升级代码以适应最近更新的`DrCom`认证系统
  * 2011-01-11 ：合并Python2和Python3版本，使同一源码文件同时支持2和3；给生成的exe文件添加图标
  * 2011-01-09 ：增加账号密码设置对话框；首次运行时会提示输入账号信息
  * 2010-12-31 ：更新以适应认证系统升级
  * 2010-10-22 ：增加对Python3的支持
  * 2010-10-21 ：完善流量查询的验证机制；去除对PIL和pytesser的依赖；
  * 2010-10-18 ：为lzuauto增加Python原生支持的tk界面
  * 2010-10-16 ：改进打包程序
  * 2010-10-12 ：界面与布局优化
  * 2010-10-01 ：完善项目相关信息
  * 2010-09-25 ：项目建立
