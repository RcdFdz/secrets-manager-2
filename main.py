##
#TODO:
# verificar ruta GPG automàticamente
# evitar elementos repetidos en el diccionario
##
import gnupg
import sys
import os.path

BINARY = '/usr/local/bin/gpg'
GPG_DIR = '~/.gnupg/'
FILE = 'secrets'

gpg=gnupg.GPG(binary=BINARY,homedir=GPG_DIR)

def get_keys():
	keys=gpg.list_keys()
	fprints=[]
	for key in keys:
		if key['type'] == 'pub' and key['keyid']!='76D78F0500D026C4':
			fprints.append(str(key['fingerprint']))
	return fprints

def encrypt_content(content):
	finger_prints = get_keys()
	return gpg.encrypt(content, *finger_prints, always_trust=True, output=FILE)

def decrypt_content():
	file = open_read_file(FILE)
	return  gpg.decrypt(file.read())

def print_decrypt_content():
	key = input('Introduce key: ' )
	content = construct_dict()
	os.system("echo '%s' | pbcopy" % content[key])
	output = input('Password copyed to clipboard.\nShow password? (N/y): ' )
	if output.lower() == 'y': print(content[key])

def add_content(key,value):
	old_content = str(decrypt_content())
	new_content = old_content + '\n' + key + '\n' + value
	if check_keys(key):
		print("The key exist, please use other")
	else:
		encrypt_content(new_content)

def open_read_file(file):
	file = open('secrets', 'a+')
	file.seek(0)
	return file

def write_in_file(file,content):
	file.write(content)
	file.close()

def check_keys(new_key):
	return new_key in construct_dict()

def show_keys():
	for k,v in construct_dict().items():
		print(k)

def construct_dict():
	content = str(decrypt_content()).split('\n')
	dictionary = {}
	index = 0
	while index < (len(content)):
		dictionary[content[index]] = content[index+1]
		index = index + 2
	return dictionary

def initialize():
	file  = open('secrets', 'w+')
	key = input('Introduce a key: ')
	value = input('Introduce a value: ')
	kv = key+'\n'+value
	encrypt_content(kv)

def interactive():
	file  = open('secrets', 'a+')
	kv = {}
	key = input('Introduce a key: ')
	value = input('Introduce a value: ')
	add_content(key,value)

def main(argv):
	if os.path.isfile(FILE):
		option = int(input('\t1: Add Pair\n\t2: Decrypt\n\t3: Show Keys\nChoose: '))
		switcher = {
			0: lambda: '',
        		1: interactive,
        		2: print_decrypt_content,
        		3: show_keys,
    		}
		# Get the function from switcher dictionary
		func = switcher.get(option, lambda: 'nothing')
		# Execute the function
		return func()
	else:
		initialize()

if __name__ == "__main__":
	main(sys.argv[1:])
