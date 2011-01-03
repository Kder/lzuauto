#encoding:utf-8

import sys
import os
from distutils.core import setup
import py2exe
import main
import lzuauto

if len(sys.argv) == 1:
    sys.argv.append('py2exe')

main_exe = {"script": "main.pyw",
#"icon_resources": [(0,'bialix.ico')],
"name": "lzuauto",
"version": '%s.%s' % (main.__version__, main.__revision__.split(':')[1][:-1].strip()),
"description": u"兰大上网认证系统客户端",
"author": ['ysjdxcn','Kder'],
"copyright": 'Copyright 2010 ysjdxcn, Kder',
"comments": u"兰大上网认证系统客户端 by ysjdxcn <ysjdxcn (at) gmail.com>, Kder <kderlin (at) gmail.com>",
"company_name": 'ysjdxcn, Kder',
}
#the dict is from http://osdir.com/ml/python.py2exe/2004-08/msg00065.html

lzuauto_exe = main_exe.copy()
lzuauto_exe["script"] = 'lzuauto.pyw'
lzuauto_exe["version"] = '%s.%s' % (lzuauto.__version__, lzuauto.__revision__.split(':')[1][:-1].strip())

options_main = {'py2exe': {'bundle_files': 3,
            'optimize': 2,
            'compressed': 1,
            'includes':['atk','dsextras','cairo','gio','pango','pangocairo'],
            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
            'pyreadline', 'logging', 'email', 'bz2', 'distutils', 'codegen',
            'inspect', 'pickle','unicodedata'],
            #'ascii' : True,
            #'dll_excludes' : ['msvcr71.dll'],
            'dist_dir':'lzuauto',
            }
}

options_lzuauto = {'py2exe': {'bundle_files': 3,
            'optimize': 2,
            'compressed': 1,
            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
            'pyreadline', 'logging', 'email', 'bz2', 'distutils', 'codegen',
            'inspect', 'pickle','unicodedata', 'gtk', 'pygtk', 'gobject', 'pygobject',
            'glib', 'atk','dsextras','cairo','gio','pango','pangocairo'],
            'dist_dir':'lzuauto',
            }
}

setup(name = 'lzuauto-tk',
      windows=[lzuauto_exe],
      options = options_lzuauto,
)

setup(name = 'lzuauto-gtk',
      windows=[main_exe],
      zipfile = None,
      options = options_main,
)


#begin to pack
src_files = [
'main.pyw',
'lzuauto.pyw',
'conf.txt',
'tesseract.exe',
'leptonlib.dll',
'tessdata',
'setup.py',
#'pack.py',
]
src_args = ' '.join(src_files)

try:
    os.system('upx lzuauto/main.exe lzuauto/tcl85.dll lzuauto/tk85.dll \
    lzuauto/python27.dll lzuauto/*.pyd')

    os.system('7z a -t7z -xr!*.svn* lzuauto-%s-src.7z %s' % \
                (main.__version__, src_args))
except:
    sys.stderr.write('Please make sure upx and 7z are in system path.')
    sys.exit(-1)

os.system('7z a -t7z -xr!*.svn* lzuauto-%s-win.7z lzuauto/main.exe \
lzuauto/conf.txt lzuauto/tesseract.exe lzuauto/tessdata \
lzuauto/leptonlib.dll' % main.__version__)

tk_files = [
'lzuauto/lzuauto.exe',
'lzuauto/conf.txt',
'lzuauto/python27.dll',
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
            (lzuauto.__version__, tk_args))
