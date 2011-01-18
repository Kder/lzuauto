#encoding:utf-8

import sys
import os
from distutils.core import setup
import py2exe
import shutil
import main
import lzuauto

if len(sys.argv) == 1:
    sys.argv.append('py2exe')
version = main.__version__
revision = main.__revision__.split(':')[1][:-1].strip()
main_exe = {"script": "main.pyw",
"icon_resources": [(0,'lzuauto.ico')],
"name": "lzuauto",
"version": '%s.%s' % (version, revision),
"description": u"兰大上网认证系统客户端",
"author": ['ysjdxcn','Kder'],
"copyright": 'Copyright 2010 ysjdxcn, Kder',
"comments": u"兰大上网认证系统客户端 by ysjdxcn <ysjdxcn (at) gmail.com>, Kder <kderlin (at) gmail.com>",
"company_name": 'ysjdxcn, Kder',
}
#the dict is from http://osdir.com/ml/python.py2exe/2004-08/msg00065.html

lzuauto_exe = main_exe.copy()
lzuauto_exe["script"] = 'lzuauto.pyw'
lzuauto_exe["version"] = '%s.%s' % (version, lzuauto.__revision__.split(':')[1][:-1].strip())

options_main = {'py2exe': {'bundle_files': 3,
            'optimize': 2,
            'compressed': 1,
            'includes':['atk','dsextras','cairo','gio','pango','pangocairo'],
            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
            'pyreadline', 'logging', 'email', 'bz2', 'distutils', 'codegen',
            'inspect', 'pickle','unicodedata'],
            #'ascii' : True,
            #'dll_excludes' : ['msvcr71.dll'],
            'dist_dir':'lzuauto-gtk',
#            'dist_dir':'lzuauto-gtk1',
            }
}

options_lzuauto = {'py2exe': {'bundle_files': 3,
            'optimize': 2,
            'compressed': 1,
            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
            'pyreadline', 'logging', 'email', 'bz2', 'distutils', 'codegen',
            'inspect', 'pickle','unicodedata', 'gtk', 'pygtk', 'gobject', 'pygobject',
            'glib', 'atk','dsextras','cairo','gio','pango','pangocairo'],
            'dist_dir':'lzuauto-tk',
#            'dist_dir':'lzuauto-tk1',
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
#sys.exit()

base_files = [
'conf.txt',
#'tesseract.exe',
#'leptonlib.dll',
#'tessdata',
]

#begin to pack
src_files = base_files + [
'main.pyw',
'lzuauto.pyw',
#'setup.py',
]
src_args = ' '.join(src_files)

try:
    for i in base_files:
        for j in ['lzuauto-gtk', 'lzuauto-tk']:
            if os.path.isdir(i):
                if not os.path.isdir(j + os.sep + i):
                    shutil.copytree(i, j + os.sep + i)
            else:
                shutil.copy(i, j)
    for i in ['etc', 'lib', 'share']:
    if not os.path.isdir('lzuauto-gtk' + os.sep + i):
        shutil.copytree('etc', 'lzuauto-gtk' + os.sep + i)
    os.system('upx lzuauto-gtk/*.pyd lzuauto-gtk/*.exe lzuauto-gtk/*.dll')
    os.system('upx lzuauto-tk/*.pyd lzuauto-tk/*.exe lzuauto-tk/*.dll')

    os.system('7z a -xr!*.svn* lzuauto-%s.%s-src.zip %s' % \
                (version, revision, src_args))
    os.system('7z a -xr!*.svn* -xr!*/tessdata -xr!*/leptonlib.dll \
-xr!*/tesseract.exe lzuauto-%s.%s-win-gtk.zip lzuauto-gtk' % 
        (version, revision))

except Exception,e:
    sys.stderr.write(str(e))
    sys.stderr.write('Please make sure upx and 7z are in system path.')
    sys.exit(-1)

# os.system('7z a -t7z -xr!*.svn* lzuauto-%s-win.7z lzuauto/main.exe \
# lzuauto/conf.txt lzuauto/tesseract.exe lzuauto/tessdata \
# lzuauto/leptonlib.dll' % version)

tk_files = [
'lzuauto-tk/conf.txt',
#'lzuauto-tk/tesseract.exe',
#'lzuauto-tk/leptonlib.dll',
#'lzuauto-tk/tessdata',
'lzuauto-tk/lzuauto.exe',
'lzuauto-tk/python27.dll',
'lzuauto-tk/library.zip',
'lzuauto-tk/_ctypes.pyd',
'lzuauto-tk/_socket.pyd',
'lzuauto-tk/_tkinter.pyd',
'lzuauto-tk/select.pyd',
'lzuauto-tk/tcl85.dll',
'lzuauto-tk/tk85.dll',
'lzuauto-tk/tcl/tcl8.5/auto.tcl',
'lzuauto-tk/tcl/tcl8.5/init.tcl',
'lzuauto-tk/tcl/tcl8.5/tclIndex',
'lzuauto-tk/tcl/tk8.5/tclIndex',
'lzuauto-tk/tcl/tk8.5/*.tcl',
'lzuauto-tk/tcl/tk8.5/ttk',
]

tk_args = ' '.join(tk_files)

os.system(r'7z a -xr!*.svn* lzuauto-%s.%s-win-tk.zip %s' % \
            (version, revision, tk_args))
