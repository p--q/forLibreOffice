#!/opt/libreoffice6.4/program/python
# -*- coding: utf-8 -*-
import subprocess 
import uno
from com.sun.star.uno.TypeClass import ENUM, STRUCT, CONSTANTS, TYPEDEF  # enum
sdk_path = "/opt/libreoffice6.4/sdk/idl"  # idlフォルダへのパス。
ctx = uno.getComponentContext()
tdm = ctx.getByName('/singletons/com.sun.star.reflection.theTypeDescriptionManager')
idlset = lambda q: set(subprocess.run(fr"grep -rl '{q}' {sdk_path}|sed -E 's@{sdk_path}/(\S+?)\.idl$@\1@;s@/@.@g'", shell=True, capture_output=True).stdout.decode().splitlines())  # シングルクォーテーションだと$が使えない。/をエスケープしないために@を使う。パイプを使うためにshell=Trueにする。
base_url = lambda t, i: fr"https://api.libreoffice.org/docs/idl/ref/{t}{'_1_1'.join(i.split('.'))}.html"  # t:type, i:IDL
atag = lambda t, i, m: fr'<a target="_blank" href="{base_url(t, i)}">{i}</a> {m}<br>'
deprecated_set = idlset("@deprecated ")
# struct
structs = []
structs_list = sorted(idlset('struct ').difference(deprecated_set))
for i in structs_list:
	td = tdm.getByHierarchicalName(i)
	if td.getTypeClass()==STRUCT:
		structs.append(atag("struct", i, td.getMemberNames()))
with open("output_struct.html", "w") as f:
	f.write("\n".join(structs))
# constants
constants = []
constants_list = sorted(idlset('constants ').difference(deprecated_set))
for i in constants_list:
	td = tdm.getByHierarchicalName(i)
	if td.getTypeClass()==CONSTANTS:
		constants.append(atag("namespace", i, [j.getName().rsplit(".", 1)[1] for j in td.getConstants()]))
with open("output_constants.html", "w") as f:
	f.write("\n".join(constants))
# enum
enums = []
enums_list = sorted(idlset('enum ').difference(deprecated_set))
base_url = lambda t, i: fr"https://api.libreoffice.org/docs/idl/ref/{t}{'_1_1'.join(i.split('.')[:-1])}.html#details"  # t:type, i:IDL, enumとtypedefは上の階層のページを開く。
for i in enums_list:
	td = tdm.getByHierarchicalName(i)
	if td.getTypeClass()==ENUM:
		enums.append(atag("namespace", i, td.getEnumNames()))
with open("output_enum.html", "w") as f:
	f.write("\n".join(enums))
# typedef
typedefs = []
typedefs_list = sorted(idlset('typedef ').difference(deprecated_set))
for i in typedefs_list:
	td = tdm.getByHierarchicalName(i)
	if td.getTypeClass()==TYPEDEF:
		typedefs.append(atag("namespace", i, td.getReferencedType().getName()))
with open("output_typedef.html", "w") as f:
	f.write("\n".join(typedefs))
