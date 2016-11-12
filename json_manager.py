import json
import sys

class JSONManager:
	json_content = {}

	def __init__(self, new_json):
		self.json_content = new_json

	def delete_entry(self, id):
		try:
			self.json_content.pop(id)
			return self.json_content
		except:
			KeyError

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

	def fix_json(self, content):
		try:
			json_content = json.loads(content)
			new_json = json.loads('{"user":"", "password":"", "url":"", "other":""}')
			for i in new_json.keys():
				if i in json_content.keys():
					new_json[i] = json_content[i]

			return json.dumps(new_json)

		except:
			raise
			print("Error you must enter a valid json")
		sys.exit()

	def add(self, id, list_values):
		list_values = self.fix_json(json.dumps(list_values))
		if id not in self.json_content:
			self.json_content[id] = json.loads(list_values)
			return self.json_content
		else:
			raise KeyError

	def get_keys(self):
		try:
			keys = sorted(self.json_content.keys())
			return keys
		except:
			raise ValueError

	def print_values(self, key, option):
		if option.lower() == 'all':
			for e in ['user', 'password', 'url', 'other']:
				print(e.capitalize() + ': ' + self.json_content[key][e])
		elif option.lower() == 'user': print(self.json_content[key]['user'])
		elif option.lower() == 'pass': print(self.json_content[key]['password'])
		elif option.lower() == 'url': print(self.json_content[key]['url'])
		elif option.lower() == 'other': print(self.json_content[key]['other'])

	def main(self):
		pass

if __name__ == '__main__':
	jm = JSONManager(sys.argv[1:]);
	jm.main()
