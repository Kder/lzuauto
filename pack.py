import sys
import os


from main import __version__ as main_ver
from lzuauto import __version__ as lzuauto_ver


src_files = [
'main.pyw',
'lzuauto.pyw',
'conf.txt',
'tesseract.exe',
'leptonlib.dll',
'tessdata',
'setup.py',
'pack.py',
]
src_args = ' '.join(src_files)

try:
    os.system('upx lzuauto/main.exe lzuauto/tcl85.dll lzuauto/tk85.dll \
    lzuauto/python26.dll lzuauto/*.pyd')

    os.system('7z a -t7z -xr!*.svn* lzuauto-%s-src.7z %s' % \
                (main_ver, src_args))
except:
    sys.stderr.write('Please make sure upx and 7z are in system path.')
    sys.exit(-1)

os.system('7z a -t7z -xr!*.svn* lzuauto-%s-win.7z lzuauto/main.exe \
lzuauto/conf.txt lzuauto/tesseract.exe lzuauto/tessdata \
lzuauto/leptonlib.dll' % main_ver)

tk_files = [
'lzuauto/lzuauto.exe',
'lzuauto/conf.txt',
'lzuauto/python26.dll',
'lzuauto/library.zip',
'lzuauto/_socket.pyd',
'lzuauto/_tkinter.pyd',
'lzuauto/select.pyd',
'lzuauto/tcl85.dll',
'lzuauto/tk85.dll',
'lzuauto/tesseract.exe',
'lzuauto/leptonlib.dll',
'lzuauto/tessdata',
'lzuauto/tcl/tcl8.5/auto.tcl',
'lzuauto/tcl/tcl8.5/init.tcl',
'lzuauto/tcl/tcl8.5/tclIndex',
'lzuauto/tcl/tk8.5/tclIndex',
'lzuauto/tcl/tk8.5/*.tcl',
'lzuauto/tcl/tk8.5/ttk',
]

tk_args = ' '.join(tk_files)

os.system(r'7z a -t7z -xr!*.svn* lzuauto-%s-win-lite.7z %s' % \
            (lzuauto_ver, tk_args))
