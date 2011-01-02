#encoding:utf-8

from distutils.core import setup
import py2exe
from py2exe.build_exe import py2exe as BuildExe
import os,sys

def TixInfo():
    import Tkinter
    import _tkinter

    tk=_tkinter.create()

    tcl_version=_tkinter.TCL_VERSION
    tk_version=_tkinter.TK_VERSION
    tix_version=tk.call("package","version","Tix")

    tcl_dir=tk.call("info","library")

    del tk, _tkinter, Tkinter

    return (tcl_version,tk_version,tix_version,tcl_dir)

class myPy2Exe(BuildExe):

    def plat_finalize(self, modules, py_files, extensions, dlls):
        BuildExe.plat_finalize(self, modules, py_files, extensions, dlls)

        if "Tix" in modules:
            # Tix adjustments
            tcl_version,tk_version,tix_version,tcl_dir = TixInfo()

            tixdll="tix%s.dll"% tix_version.replace(".","")#,
#                                    tcl_version.replace(".","")
            tcldll="tcl%s.dll"%tcl_version.replace(".","")
            tkdll="tk%s.dll"%tk_version.replace(".","")

            dlls.add(os.path.join(sys.prefix,"tcl",'Tix%s'%tix_version,tixdll))

            self.dlls_in_exedir.extend( [tcldll,tkdll,tixdll ] )

            tcl_src_dir = os.path.split(tcl_dir)[0]
            tcl_dst_dir = os.path.join(self.lib_dir, "tcl")
            self.announce("Copying TIX files from %s..." % tcl_src_dir)
            self.copy_tree(os.path.join(tcl_src_dir, "tix%s" % tix_version),
                           os.path.join(tcl_dst_dir, "tix%s" % tix_version))

opts = {'py2exe': {'bundle_files': 1,
#                            'optimize': 2,
#                            'compressed': 1,
#                            'includes':['atk','dsextras','cairo','gio','pango','pangocairo'],
#                            'excludes' : ['_ssl', '_hashlib', 'doctest', 'pdb', 'unittest', 'difflib',
#                            'pyreadline', 'logging', 'email', 'ctypes', 'bz2', 'distutils', 'codegen',
#                            'inspect', 'pickle','unicodedata'],
                            #'ascii' : True,
                            #'dll_excludes' : ['msvcr71.dll'],
                            'dist_dir':'lzuauto-tk2',
                            }
                }

setup(
    script_args=['py2exe'],
    cmdclass={'py2exe':myPy2Exe},
    windows=['lzuauto.pyw'],
    options=opts,
)