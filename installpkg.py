#!/usr/bin/python

import os
import sys
import subprocess

class InstallPKG(object):
	def __init__(self):
		path = sys.argv[0]
		self.share_folder_path = "/".join(path.split("/")[:-1]) + "/"
		print(self.share_folder_path)

		num_argv = len(sys.argv)

		self.argu_list = []

		if num_argv > 1:
			self.argu_list = sys.argv[1:]
			print(self.argu_list)


	def get_dmg_list(self):
		self.dmg_list = []
		if os.path.isdir(self.share_folder_path):
			file_list = os.listdir(self.share_folder_path)
			for item in file_list:
				if ".dmg" in item.lower():
					if self.argu_list:
						for argu in self.argu_list:
							if argu.lower() in item.lower():
								self.dmg_list.append(os.path.join(self.share_folder_path, item))
					else:
						self.dmg_list.append(os.path.join(self.share_folder_path, item))
				if ".pkg" in item.lower():
					if "vertica" in item.lower():
						self.vertica_path = os.path.join(self.share_folder_path, item)
						print("vertica path : ", self.vertica_path)
						self.vertica_path = self.vertica_path.replace(" ", "\\ ").replace("(", "\(").replace(")", "\)")
	
	def attach_dmg(self):
		attach_command = 'hdiutil attach '
		self.attach_place = []
		if not self.dmg_list: return
		for item in self.dmg_list:
			print("Attaching dmg file :", item)
			command = attach_command + item
			proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			mount_place = out.split("\t")[-1].replace("\n", "").replace(" ", "\ ")
			self.attach_place.append(mount_place)
	
	def detach_dmg(self):
		for item in self.attach_place:
			print("Detaching dmg file :", item)
			command = "hdiutil detach " + item + " -force"
			proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
		print("Finish detaching..")
	
	def get_pkg_list(self):
		volume_path = "/Volumes/"
		self.pkg_list = []
		dir_list = os.listdir(volume_path)
		for item in dir_list:
			if "tableau" in item.lower():
				dir_path = os.path.join(volume_path, item)
				if os.path.isdir(dir_path):
					pkg_list = os.listdir(dir_path)
					for f in pkg_list:
						if ".pkg" in f:
							self.pkg_list.append(os.path.join(dir_path, f))
	
	def install_app(self):
		if not self.pkg_list: return
		install_command = "installer -pkg "
		target = " -target /"
		for pkg in self.pkg_list:
			if "vertica" in pkg.lower():
				self.vertica()
				continue

			print("Installing pkg :", pkg)
			pkg = pkg.replace(" ", "\\ ").replace("(", "\(").replace(")", "\)")
			command = install_command + pkg + target
			os.system(command)

	def vertica(self):
		print("find vertica-----------")
		if not os.path.exists("/Library/ODBC/Vertica"):
			cmd = "mkdir -p /Library/ODBC/Vertica"
			proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
		print("-------prepare for copy")
		cmd = ["/bin/cp", self.vertica_path, "/Library/ODBC/Vertica/"]
		cmd = "cp /Volumes/SharedFolders/ShareTest/vertica-odbc-7.1.2-0.mac.pkg /Library/ODBC/Vertica"
		print("------copy command :", cmd)
		proc = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		print("------cp vertica to /Library/ODBC/Vertica/")
	
#    def codesign(self):
#        application_path = "/Applications/"
#        app_list = []
#        dir_list = os.listdir(application_path)
#        for item in dir_list:
#            if "tableau" in item.lower():
#                item = item.replace(" ", "\\ ").replace("(", "\(").replace(")", "\)")
#                dir_path = os.path.join(application_path, item)
#                print("codesign ", dir_path)
#                command = "codesign -vv " + dir_path
#                proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
#                (out, err) = proc.communicate()
#                print("codesign res ", out, err)

if __name__ == "__main__":
	installpkg = InstallPKG()
	
	installpkg.get_dmg_list()
	installpkg.attach_dmg()
	installpkg.get_pkg_list()
	installpkg.install_app()
	installpkg.detach_dmg()

