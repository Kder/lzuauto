### 运行源码版的系统要求 ###

Windows版本可以直接双击运行，源码版需要以下依赖：

Linux下：
  * python(py2.6以上，支持python3)
  * pygtk（main.pyw）或tk（lzuauto.pyw）
  * tesseract (ocr工具，主页 http://code.google.com/p/tesseract-ocr/ ）

> 各大发行版的源中应该都有上面的包，在Arch Linux和Gentoo Linux下测试通过。

Windows下：
  * python2.6/2.7 【tk界面只依赖这一项】，或Python3（仅支持tk界面） http://www.python.org

> 以下4个仅GTK界面需要
    1. pycairo http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/
    1. pygobject http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/
    1. pygtk http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/
    1. GTK+(All-in-one bundles) http://www.gtk.org/download-windows.html