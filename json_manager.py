import json
from gpg_tools import GPGTools

class JSONManager:
	json_content = {}

	def __init__(self, new_json = None):
		if new_json or new_json == {}:
			self.json_content = new_json
		else:
			gpg = GPGTools()
			self.json_content = json.loads(str(gpg.decrypt_content()))

	def delete_entry(self, id):
		self.json_content.pop(id)
		return self.json_content

	def modify_values(self, id, list_values):
		for key in list_values:
			if key in self.json_content[id].keys():
				self.json_content[id][key] = list_values[key]
			else:
				raise KeyError
		return self.json_content

	def modify_id(self, old_id, new_id):
		aux = self.json_content[old_id]
		self.json_content.pop(old_id)
		self.json_content[new_id] = aux
		return self.json_content

	def add(self, id, list_values):
		if id not in self.json_content:
			self.json_content[id] = list_values
		else:
			raise KeyError
		return self.json_content

	def get_keys(self):
		try:
			keys = sorted(self.json_content.keys())
			return keys
		except:
			raise ValueError

	def main(self):
		pass

if __name__ == '__main__':
	sm = JSONManager();
	sm.main()
