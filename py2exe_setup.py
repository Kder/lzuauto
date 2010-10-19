#encoding:utf-8

from distutils.core import setup
import py2exe
import sys
from lzuauto import __version__

if len(sys.argv) == 1:
    sys.argv.append('py2exe')

window_dict = {"script": "lzuauto.pyw",
#"icon_resources": [(0,'bialix.ico')],
"name": "lzuauto",
"version": __version__,
"description": u"兰大上网认证系统客户端",
"author": ['ysjdxcn','Kder'],
"copyright": 'Copyright 2010 ysjdxcn, Kder',
"comments": u"兰大上网认证系统客户端 by ysjdxcn <ysjdxcn (at) gmail.com>, Kder <kderlin (at) gmail.com>",
"company_name": 'ysjdxcn, Kder',
}
#the dict is from http://osdir.com/ml/python.py2exe/2004-08/msg00065.html

setup(name = 'lzuauto',
      windows=[window_dict],
#      zipfile = None,
      options = {'py2exe': {'bundle_files': 3,
                            'optimize': 2,
                            'compressed': 1,
#                            'includes':['atk','dsextras','cairo','gio','pango','pangocairo'],
                            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
                            'pyreadline', 'logging', 'email', 'ctypes', 'bz2', 'distutils', 'codegen',
                            'inspect', 'pickle','unicodedata'],
                            #'ascii' : True,
                            #'dll_excludes' : ['msvcr71.dll'],
                            'dist_dir':'lzuauto-tk1',
                            }
                },
)
