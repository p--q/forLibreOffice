#!/opt/libreoffice6.4/program/python
# -*- coding: utf-8 -*-
import subprocess 
import uno
sdk_path = "/opt/libreoffice6.4/sdk/idl"  # idlフォルダへのパス。
ctx = uno.getComponentContext()
tdm = ctx.getByName('/singletons/com.sun.star.reflection.theTypeDescriptionManager')
idls = lambda q: subprocess.run(fr"grep -rl '{q}' {sdk_path}|sed -E 's@{sdk_path}/(\S+?)\.idl$@\1@;s@/@.@g'|sort", shell=True, capture_output=True).stdout.decode().split("\n")[:-1]  # シングルクォーテーションだと$が使えない。/をエスケープしないために@を使う。パイプを使うためにshell=Trueにする。
base_url = lambda t, i: fr"https://api.libreoffice.org/docs/idl/ref/{t}{'_1_1'.join(i.split('.'))}.html"  # t:type, i:IDL
# struct
structs = [fr'<a href="{base_url("struct", i)}">{i}</a> {" ".join(tdm.getByHierarchicalName(i).getMemberNames())}<br>' for i in idls('published struct')]
with open("output_struct.html", "w") as f:
	f.write("\n".join(structs))
# constants
constants = [fr'<a href="{base_url("namespace", i)}">{i}</a> {" ".join(j.getName().rsplit(".", 1)[1] for j in tdm.getByHierarchicalName(i).getConstants())}<br>' for i in idls('published constants')]
with open("output_constants.html", "w") as f:
	f.write("\n".join(constants))
# enum
# enums = [fr'<a href="{base_url("namespace", i)}">{i}</a> {" ".join(tdm.getByHierarchicalName(i).getEnumNames())}<br>' for i in idls('enum ')]
# with open("output_enum.html", "w") as f:
# 	f.write("\n".join(enums))
# for i in idls('enum '):
# 	print(i)
# 	print(tdm.getByHierarchicalName(i).getEnumNames())
	
# 	@deprecated 削る
	