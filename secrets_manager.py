#!/usr/local/bin/python3
from gpg_tools import GPGTools

json_content = {}

class SecretsManager:
	def __init__(self, new_json = None):
		gpg = GPGTools()
		global json_content
		if new_json or new_json == {}:
			json_content = new_json
		else:
			json_content = gpg.decrypt_content()

	def delete_entry(self, id):
		global json_content
		json_content.pop(id)
		return json_content

	def main(self):
		pass

if __name__ == '__main__':
	sm = SecretsManager();
	sm.main()
