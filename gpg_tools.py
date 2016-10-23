import gnupg
import glob

BINARY = '/usr/local/bin/gpg'
GPG_DIR = '~/.gnupg/'
PUB_KEYS = './pub-keys/*.asc'

gpg=gnupg.GPG(binary=BINARY,homedir=GPG_DIR)

class GPGTools:
	FILE = 'secrets'
	KEY = None

	def __init__(self, file = None, key = None):
		if file:
			self.FILE = file
		if key:
			self.KEY = key

	def get_keys(self):
		files = glob.glob(PUB_KEYS)
		keys_data = ''
		for name in files:
			try:
				with open(name) as file:
					 keys_data+=str(file.read())
			except IOError as exc:
				if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
					raise # Propagate other kinds of IOError.
		import_result = gpg.import_keys(keys_data)
		fprints=[]
		for key in import_result.results:
			fprints.append(str(key['fingerprint']))
		return fprints

	def encrypt_content(self, content):
		finger_prints = self.get_keys()
		return gpg.encrypt(content, *finger_prints, always_trust=True, output=self.FILE)

	def decrypt_content(self):
		file = open(self.FILE, 'a+')
		file.seek(0)
		if self.KEY:
			return gpg.decrypt(file.read(), passphrase=self.KEY)
		else:
			return gpg.decrypt(file.read())

	def main(self):
		pass

if __name__ == '__main__':
	gpgTools = GPGTools(file = 'secrets', key = '12345')
	gpgTools.main()
