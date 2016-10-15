import gnupg
import glob

BINARY = '/usr/local/bin/gpg'
GPG_DIR = '~/.gnupg/'
PUB_KEYS = './pub-keys/*.asc'
FILE = 'secrets'

gpg=gnupg.GPG(binary=BINARY,homedir=GPG_DIR)

class GPGTools:
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
		finger_prints = get_keys()
		return gpg.encrypt(content, *finger_prints, always_trust=True, output=FILE)

	def decrypt_content(self):
		file = open(FILE, 'a+')
		file.seek(0)
		return gpg.decrypt(file.read())

