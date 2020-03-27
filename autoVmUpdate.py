import sys
import os
import subprocess

from datetime import date
from datetime import datetime

sys.path.insert(0,'/Library/Frameworks/ParallelsVirtualizationSDK.framework/Versions/7/Libraries/Python/3.7')

import prlsdkapi
consts = prlsdkapi.prlsdk.consts

class VMupdate(object):
	def __init__(self):
		
		self.current_path = os.getcwd()
		path = sys.argv[0]
		self.current_path = "/".join(path.split("/")[:-1]) + "/"

		self.vmlist = []
		self.runningVm = []
		self.log = []

		prlsdkapi.init_desktop_sdk()
		print(prlsdkapi.is_sdk_initialized())
		self.server = prlsdkapi.Server()

		result = self.server.login_local('', 0, consts.PSL_NORMAL_SECURITY).wait()

		login_response = result.get_param()

		product_version = login_response.get_product_version()
		print("product_version:", product_version)
		
		host_os_version = login_response.get_host_os_version()
		print("host_os_version:", host_os_version)
		
		host_uuid = login_response.get_server_uuid()
		print("host_uuid:", host_uuid)
		
		result = self.server.get_srv_config().wait()
		srv_config = result.get_param()

		file_path = os.path.join(self.current_path + "/vmlist")
		if not os.path.exists(file_path):
			print("file path not exist", file_path)
			raise
		if not os.path.isfile(file_path):
			print("file not exist", file_path)
			raise

		with open(file_path, "r") as f:
			for line in f:
				self.vmlist.append(line.strip())

	def bringUpVms(self):
		result = self.server.get_vm_list().wait()
		for i in range(result.get_params_count()):
			vm = result.get_param_by_index(i)
			vm_config = vm.get_config()
			vm_name = vm_config.get_name()
			vm_uuid = vm.get_uuid()

			if vm_uuid in self.vmlist:
				state_result = vm.get_state().wait()
				vm_info = state_result.get_param()
				state_code = vm_info.get_state()

				if state_code != consts.VMS_RUNNING:
					vm.start()
				state_result = vm.get_state().wait()
				vm_info = state_result.get_param()
				state_code = vm_info.get_state()

				if state_code == consts.VMS_RUNNING:
					self.runningVm.append(vm_uuid)

	def installUpdate(self):
		for uuid in self.runningVm:
			self.log.append("Updating VM uuid " + uuid + "\n")
			proc = subprocess.Popen(["/usr/local/bin/prlctl", "exec", uuid, "softwareupdate", "-aiR"])
			try:
				outs, errs = proc.communicate()
				self.log.append("Finish Updating VM uuid " + uuid + "\n")
			except:
				proc.kill()
				outs, errs = proc.communicate()
				self.log.append("Error updating VM uuid " + uuid)
				self.log.append(outs, errs)
		
	def writeUpdateLog(self):
		now = datetime.now().isoformat(timespec='minutes')   
		
		log_path = self.current_path + "vmUpdateLog"
		with open(log_path, "a") as f:
			f.write('----------------------')
			f.write(now)
			f.write('\n')
			for line in self.log:
				f.write(line)
				f.write('\n')
			

if __name__ == "__main__":
	vmupdate = VMupdate()
	vmupdate.bringUpVms()
	vmupdate.installUpdate()
	vmupdate.writeUpdateLog()

		



