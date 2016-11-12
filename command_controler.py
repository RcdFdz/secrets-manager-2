import json
import os
import sys
from json_manager import JSONManager
from gpg_tools import GPGTools

class CommandControler:
	gpg = ''

	def __init__(self, gpg):
		self.gpg = gpg

	def get_key_value(self, key, option):
		jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		jm.print_values(key, option)

	def get_json(self):
		return str(self.gpg.decrypt_content())

	def set_json(self, json):
		self.gpg.encrypt_content(json)

	def get_keys(self):
		jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		return jm.get_keys()

	def add_content(self, new_json_content):
		new_json_content = json.loads(str(new_json_content))
		if(os.path.isfile(self.gpg.get_file())):
			old_json_content = json.loads(str(self.gpg.decrypt_content()))
		else:
			old_json_content = {}
		for i in new_json_content.keys():
			old_json_content[i] = new_json_content[i]
		final_json_content = old_json_content

		jkv = json.dumps(final_json_content, sort_keys=True)
		self.gpg.encrypt_content(jkv)

	def add_content_id_json(self, id, json_content):
		if(os.path.isfile(self.gpg.get_file())):
			jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		else:
			jm = JSONManager(json.loads('{}'))
		jkv = jm.add(id, json.loads(str(json_content[0])))
		jkv = json.dumps(jkv)
		self.gpg.encrypt_content(jkv)

	def modify_content(self, id, json_content):
		if(os.path.isfile(self.gpg.get_file())):
			jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		else:
			jm = JSONManager(json.loads('{}'))
		jkv = jm.modify_values(id, json.loads(str(json_content[0])))
		jkv = json.dumps(jkv)
		self.gpg.encrypt_content(jkv)

	def modify_id(self, old_id, new_id):
		jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		jkv = json.dumps(jm.modify_id(old_id, new_id))
		self.gpg.encrypt_content(jkv)

	def del_id(self, id):
		jm = JSONManager(json.loads(str(self.gpg.decrypt_content())))
		jkv = json.dumps(jm.delete_entry(id))
		self.gpg.encrypt_content(jkv)

	def update_keys(self):
		self.gpg.encrypt_content(str(self.gpg.decrypt_content()))

	def show_keys(self):
		try:
			json_content = json.loads(str(self.gpg.decrypt_content()))
			for key in sorted(json_content.keys()):
		 		print(key)
		except:
			raise ValueError

	def main(self):
		pass

if __name__ == '__main__':
	gpg = GPGTools()
	cmdc = CommandControler(gpg)
	cmdc.main()
