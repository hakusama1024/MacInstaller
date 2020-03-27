import sys
import os

import time
from datetime import date
from datetime import datetime
from optparse import OptionParser

sys.path.insert(0,'/Library/Frameworks/ParallelsVirtualizationSDK.framework/Versions/7/Libraries/Python/3.7')

import prlsdkapi
consts = prlsdkapi.prlsdk.consts

class VMsetup(object):
	def __init__(self):
		prlsdkapi.init_desktop_sdk()
		self.server = prlsdkapi.Server()

		result = self.server.login_local('', 0, consts.PSL_NORMAL_SECURITY).wait()

		login_response = result.get_param()

		self.current_path = os.path.dirname(os.path.abspath(__file__))

		self.vmlist = []
		self.runningVm = []

		file_path = os.path.join(self.current_path + "/vmlist")
		if not os.path.exists(file_path):
			print("file path not exist", file_path)
			raise
		if not os.path.isfile(file_path):
			print("file not exist", file_path)
			raise

		with open("vmlist", "r") as f:
			for line in f:
				self.vmlist.append(line.strip())

	def list(self, option, opt, value, parser):
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
				print("----------------------------------------------------")
				print("bring up tempalte vm: ")
				print(vm_uuid)
				print(vm_name)
		
	def create(self, option, opt, value, parser):
		today = date.today().strftime("%y_%m_%d")
		current_time = datetime.now().strftime("%H_%M_%S")
		result = self.server.get_vm_list().wait()
		snapshot_template_list = []	
		snapshot_name_list = []	
 
		for i in range(result.get_params_count()):
			vm = result.get_param_by_index(i)
			vm_config = vm.get_config()
			vm_name = vm_config.get_name()
			vm_uuid = vm.get_uuid()
			if vm_uuid in self.vmlist:
				print("----------------------------------------------------")
				print("Current vm uuid : ", vm_uuid)
				state_result = vm.get_state().wait()
				vm_info = state_result.get_param()
				state_code = vm_info.get_state()

				if state_code != consts.VMS_RUNNING:
					vm.start()
				state_result = vm.get_state().wait()
				vm_info = state_result.get_param()
				state_code = vm_info.get_state()
				if state_code == consts.VMS_RUNNING:
					try:
						new_name = today + " " + current_time + " Snapshot of " + vm.get_config().get_name()
						print("Clonning is in progress...")
						vm.create_snapshot(new_name).wait()
						print("Cloning was successful. New virtual machine name: ", new_name)
					except prlsdkapi.PrlSDKError as e:
						print("Error: %s" % e)
						continue

if __name__ == "__main__":
	vmsetup = VMsetup()

	usage = "usage: %prog arg"
	parser = OptionParser(usage)

	parser.add_option("-l", "--list", help="list snapshot template vm", action="callback", callback=vmsetup.list)
	parser.add_option("-n", "--new", help="create snapshot from template vm", action="callback", callback=vmsetup.create)

	(options, args) = parser.parse_args()

	if len(os.sys.argv) == 1 or len(os.sys.argv) > 2:
		parser.print_help()
