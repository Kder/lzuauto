import os
from main import __version__

os.system(r'7z a -t7z -xr!*.svn* lzuauto-%s-src.7z @file_list.txt' % __version__)
os.system(r'7z a -t7z -xr!*.svn* lzuauto-%s-win.7z lzuauto/main.exe lzuauto/conf.txt lzuauto/tesseract.exe lzuauto/tessdata' % __version__)
