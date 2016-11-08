import json
import os
import sys
from json_manager import JSONManager

class CommandControler:
	gpg = ''

	def __init__(self, gpg):
		self.gpg = gpg

	def add_content(self, json_content):
		json_content = json.loads(str(json_content).replace("'",'"'))
		try:
			old_json_content = json.loads(str(self.gpg.decrypt_content()))
			for i in json_content.keys():
				old_json_content[i]=json_content[i]
			new_json_content = old_json_content
		except:
			raise

		jkv = json.dumps(new_json_content, sort_keys=True)
		self.gpg.encrypt_content(jkv)

	def show_keys(self):
		try:
			json_content = json.loads(str(self.gpg.decrypt_content()))
			for key in sorted(json_content.keys()):
		 		print(key)
		except:
			raise ValueError

	def update_keys(self):
		self.gpg.encrypt_content(str(self.gpg.decrypt_content()))

	def get_keys(self):
		jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		return jm.get_keys()

	def main(self):
		pass

if __name__ == '__main__':
	cmdc = CommandControler()
	cmdc.main()
