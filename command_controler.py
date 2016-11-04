import json
import os
import sys

class CommandControler:
	gpg = ''

	def __init__(self, gpg):
		self.gpg = gpg

	def show_keys(self):
		try:
			json_content = json.loads(str(self.gpg.decrypt_content()))
			for key in sorted(json_content.keys()):
		 		print(key)
		except:
			raise ValueError

	def update_keys(self):
		self.gpg.encrypt_content(str(self.gpg.decrypt_content()))

	def main(self):
		pass

if __name__ == '__main__':
	cmdc = CommandControler()
	cmdc.main()
