#encoding:utf-8

from distutils.core import setup
import py2exe
import sys
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

options_main = {'py2exe': {'bundle_files': 1,
            'optimize': 2,
            'compressed': 1,
            'includes':['atk','dsextras','cairo','gio','pango','pangocairo'],
            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
            'pyreadline', 'logging', 'email', 'ctypes', 'bz2', 'distutils', 'codegen',
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
            'pyreadline', 'logging', 'email', 'ctypes', 'bz2', 'distutils', 'codegen',
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

