import pytest
import __builtin__
import os
import json
import time
from interactive_cmd import InteractiveCMD
from gpg_tools import GPGTools

if os.path.isfile('secrets'):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	os.rename('secrets', '._secrets.bkp'+str(timestr))

for i in range(1,100):
	if os.path.isfile('secrets'+str(i)): os.remove('secrets'+str(i))

def get_files(file_name1, file_name2):
	file1 = open(file_name1, 'w')
	file1.write("-----BEGIN PGP MESSAGE-----\n\nhQIMA+HIES/TSZytAQ//XFNQVedjCG5VLoyhbnOQjhAfVvuBxnZp0kfkPj3iGH+a\nefC2pZ/uzwYEkZgZa8JoOT4MIguex5UEy8YehsDZ3omGnkK4lSyYXy1BTG4LxQBG\nmRMmufVZJtU4W0q8Syce7cfA6FXR7AdECCegmkdJ/5nngJvEoLEB7MXFT7idGf5+\n2fAYfJJ/C6p6Y54xnFmh1NIAYZuYfw/MQaT2q5nJUn0y+FfxE2Zapj4Vr0mU4bsY\np/Wj5axEo0GVSiFHZL3ToYhOi7eRFqIvfJ/Wid8MIuuw79KnuRjVPzBnWKhMbF4z\nFxvjaKcpRPjNsZDgXCx9rkwFEwkYG1KqmWionZO0uj9Iut1S6+SEf/6r41Q2hjwn\nXUNA8oq45MXRC8X2vhOfWUJcdjj7JEf/K0TkIkSJhQn/vIUOShcNgTNKdDbVCJkE\n5oxdSkSOizGXN44wKLPaCccKyH02eJiO+LXvkRWcIP9kRrtAC5WnDAtod0N+NgSw\nGOnDqQxuQwJ6J7AOIz29lwxF27aXis5sxTz2UK4f9Fw1FvTp1YD32zDBS2w82BWy\nyZmIcp2VaR4hWrTC5atTel17co/gVfquaeyDWs3zQ9u116hRRctUS+m4o4l8HGdS\nZq4nB/pBlXQYFGLaeGaZB1pcUm1/Yq17lLzTZ01/OXwCma61cqIEY9Q6WuKZ0nyF\nAgwDCDQBmit7oo4BD/sEdmO9bU0k2AX3PrDeA2FkkTVgcctpzFvYDSOCKPs5fmL+\n3rSsYKcudSoiC4qcPiYaPave+h4UDnGq7MShW8dkQeZUFJpeZdf/UMjrnoeSdMgg\nPoWIJtD/tbobqtnVBXY/cvoQYaIQLpC2PEvOwDooxYb69fSyujKXkngR0MXt1Q9V\nyGOdDBRN5SGlEDcIWE1kz8J9dDgVt0D27uqOTdFKBSpA11/3SFCyvdQkIisuQK8v\nLJydAmD1XpewMPnbTvcE+zClUFjLRgdI1sYgHCE5ubHKB04wGQhtrNj8c5V/IyGg\ndRQsfnD7WflSpCjQUfUxCi+fDQg3ZgPiJgi4ao75LskNIovdkiZVaeI4Y0LCCIqI\nSLM0kfOKDJtV28yZgGPRCSuHT7lwi9x74ULj3/P6sWgerxrsZOY4KDlcgzVirYdc\nYgvYi4kEMgS4vJ5PGAQlYD37RZ+McDnCEzSdNQd0aIOGGVYhyBaVbGJgpDxJX5bJ\nrGO2E7NWsF77qNxto+e63IeKAO1pSS/a7r+lqfcGazcp3ZoaNHYdU5psJgf27siI\nxWZhrSMno3e/yYUHO+I6IX8Oswf4mH2pUWrong5MziLd9EPvSD5ijZe84dREUlzz\nmxJd+7eFFPDLA39hgsgdKjL5mrPEbV++GbVg3AokFhQrQlfeZmyGu1kI9/c/mtJx\nAZ/D+V9CJV7IEOWqDSw8OTh2GH0gAHqcalJnnA3Y37LJ15v+BiT88JZfj6VJReFN\nWJZvKBqSj8+DaHZfQxkigALejbIvCAFmZr3iVgmZYpuTmE4Rumwa07x2+JlhJkti\nCCpzx4qpAAdMhKRp+X4WbEI=\n=zd48\n-----END PGP MESSAGE-----")
	file1.close()

	file2 = open(file_name2, 'w')
	file2.write("-----BEGIN PGP MESSAGE-----\n\nhQIMA+HIES/TSZytAQ//XFNQVedjCG5VLoyhbnOQjhAfVvuBxnZp0kfkPj3iGH+a\nefC2pZ/uzwYEkZgZa8JoOT4MIguex5UEy8YehsDZ3omGnkK4lSyYXy1BTG4LxQBG\nmRMmufVZJtU4W0q8Syce7cfA6FXR7AdECCegmkdJ/5nngJvEoLEB7MXFT7idGf5+\n2fAYfJJ/C6p6Y54xnFmh1NIAYZuYfw/MQaT2q5nJUn0y+FfxE2Zapj4Vr0mU4bsY\np/Wj5axEo0GVSiFHZL3ToYhOi7eRFqIvfJ/Wid8MIuuw79KnuRjVPzBnWKhMbF4z\nFxvjaKcpRPjNsZDgXCx9rkwFEwkYG1KqmWionZO0uj9Iut1S6+SEf/6r41Q2hjwn\nXUNA8oq45MXRC8X2vhOfWUJcdjj7JEf/K0TkIkSJhQn/vIUOShcNgTNKdDbVCJkE\n5oxdSkSOizGXN44wKLPaCccKyH02eJiO+LXvkRWcIP9kRrtAC5WnDAtod0N+NgSw\nGOnDqQxuQwJ6J7AOIz29lwxF27aXis5sxTz2UK4f9Fw1FvTp1YD32zDBS2w82BWy\nyZmIcp2VaR4hWrTC5atTel17co/gVfquaeyDWs3zQ9u116hRRctUS+m4o4l8HGdS\nZq4nB/pBlXQYFGLaeGaZB1pcUm1/Yq17lLzTZ01/OXwCma61cqIEY9Q6WuKZ0nyF\nAgwDCDQBmit7oo4BD/sEdmO9bU0k2AX3PrDeA2FkkTVgcctpzFvYDSOCKPs5fmL+\n3rSsYKcudSoiC4qcPiYaPave+h4UDnGq7MShW8dkQeZUFJpeZdf/UMjrnoeSdMgg\nPoWIJtD/tbobqtnVBXY/cvoQYaIQLpC2PEvOwDooxYb69fSyujKXkngR0MXt1Q9V\nyGOdDBRN5SGlEDcIWE1kz8J9dDgVt0D27uqOTdFKBSpA11/3SFCyvdQkIisuQK8v\nLJydAmD1XpewMPnbTvcE+zClUFjLRgdI1sYgHCE5ubHKB04wGQhtrNj8c5V/IyGg\ndRQsfnD7WflSpCjQUfUxCi+fDQg3ZgPiJgi4ao75LskNIovdkiZVaeI4Y0LCCIqI\nSLM0kfOKDJtV28yZgGPRCSuHT7lwi9x74ULj3/P6sWgerxrsZOY4KDlcgzVirYdc\nYgvYi4kEMgS4vJ5PGAQlYD37RZ+McDnCEzSdNQd0aIOGGVYhyBaVbGJgpDxJX5bJ\nrGO2E7NWsF77qNxto+e63IeKAO1pSS/a7r+lqfcGazcp3ZoaNHYdU5psJgf27siI\nxWZhrSMno3e/yYUHO+I6IX8Oswf4mH2pUWrong5MziLd9EPvSD5ijZe84dREUlzz\nmxJd+7eFFPDLA39hgsgdKjL5mrPEbV++GbVg3AokFhQrQlfeZmyGu1kI9/c/mtJx\nAZ/D+V9CJV7IEOWqDSw8OTh2GH0gAHqcalJnnA3Y37LJ15v+BiT88JZfj6VJReFN\nWJZvKBqSj8+DaHZfQxkigALejbIvCAFmZr3iVgmZYpuTmE4Rumwa07x2+JlhJkti\nCCpzx4qpAAdMhKRp+X4WbEI=\n=zd48\n-----END PGP MESSAGE-----")
	file2.close()

def remove_files(list):
	for file in list:
		os.remove(str(os.getcwd()) + '/' + file)

def get_GPG(message, secrets_file, secrets_key):
	gpg = GPGTools(file = secrets_file, key = secrets_key)
	gpg.encrypt_content(message)

	return gpg

def test_interactive_menu_no_file_add_content(monkeypatch):
	gpg = GPGTools(key = '12345')

	aux = ['1','One', 'user1', 'pass1', 'url1', 'other1']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()

	json_ex = json.loads('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}')
	json_gpg = json.loads(str(gpg.decrypt_content()))

	for i in json_gpg["One"]:
		assert json_gpg["One"][i] == json_ex["One"][i]

	remove_files(['secrets'])

def test_interactive_menu_no_file_exit(monkeypatch):
	gpg = GPGTools(key = '12345')

	aux = ['2']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)

	with pytest.raises(SystemExit):
		icmd.interactive_menu()

def test_interactive_menu_with_file_add_content(monkeypatch):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}',
					'secrets_tmp29', '12345')

	aux = ['1','Two', 'user2', 'pass2', 'url2', 'other2']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()

	json_ex = json.loads('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}')
	json_gpg = json.loads(str(gpg.decrypt_content()))

	for i in json_gpg["Two"]:
		assert json_gpg["Two"][i] == json_ex["Two"][i]

	for i in json_gpg["One"]:
		assert json_gpg["One"][i] == json_ex["One"][i]

	remove_files(['secrets_tmp29'])

def test_interactive_menu_with_file_modify_content(monkeypatch, capsys):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}',
					'secrets_tmp30', '12345')

	aux = ['2','One', 'user2', 'pass2', 'url2', 'other2']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()
	out, err = capsys.readouterr()

	json_ex = json.loads('{"One": {"user":"user2","password":"pass2","url":"url2","other":"other2"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}')
	json_gpg = json.loads(str(gpg.decrypt_content()))

	for i in json_gpg["Two"]:
		assert json_gpg["Two"][i] == json_ex["Two"][i]

	for i in json_gpg["One"]:
		assert json_gpg["One"][i] == json_ex["One"][i]

	assert out == 'Leave all elements without value for delete the entry\nDone! Identifier One has been modified\n'

	remove_files(['secrets_tmp30'])

def test_interactive_menu_with_file_modify_content_delete(monkeypatch, capsys):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}',
					'secrets_tmp31', '12345')

	aux = ['2','One', '', '', '', '']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()
	out, err = capsys.readouterr()

	json_ex = json.loads('{"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}')
	json_gpg = json.loads(str(gpg.decrypt_content()))

	for i in json_gpg["Two"]:
		assert json_gpg["Two"][i] == json_ex["Two"][i]

	with pytest.raises(KeyError):
		json_gpg["One"]

	assert out == 'Leave all elements without value for delete the entry\nDone! Identifier One has been deleted\n'

	remove_files(['secrets_tmp31'])

def test_interactive_menu_with_file_print_decrypt_content(monkeypatch, capsys):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}',
					'secrets_tmp32', '12345')

	aux = ['3','Two', 'list', 'One','Y','N']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()
	out, err = capsys.readouterr()

	assert out == 'One\nuser: user1\npassword: pass1\nurl: url1\nother: other1\n'

	remove_files(['secrets_tmp32'])

def test_interactive_menu_with_file_print_decrypt_content(monkeypatch, capsys):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}',
					'secrets_tmp33', '12345')

	aux = ['4']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()
	out, err = capsys.readouterr()

	assert out == 'One\nTwo\n'

	remove_files(['secrets_tmp33'])

def test_update_keys(monkeypatch):
	get_files('secrets_tmp34', 'secrets_tmp35')

	gpg = GPGTools(file = 'secrets_tmp34', key = '12345')
	aux = ['5']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.interactive_menu()

	file1 = open('secrets_tmp34','r')
	file2 = open('secrets_tmp35','r')

	assert file1.read() != file2.read()

	remove_files(['secrets_tmp34','secrets_tmp35'])

def test_no_update_keys():
	''' This test ensure that the codification works properly
	in the future this could be moved to the test_gpg_tools
	'''
	get_files('secrets_tmp36', 'secrets_tmp37')

	gpg = GPGTools(file = 'secrets_tmp36', key = '12345')
	icmd = InteractiveCMD(gpg)

	file1 = open('secrets_tmp36','r')
	file2 = open('secrets_tmp37','r')

	assert file1.read() == file2.read()

	remove_files(['secrets_tmp36','secrets_tmp37'])

def test_interactive_menu_no_file_exit(monkeypatch):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"Two": {"user":"user2","password":"pass2","url":"url2","other":"other2"}}',
					'secrets_tmp38', '12345')

	aux = ['6']
	def mock_raw_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(__builtin__, 'raw_input',mock_raw_input_user)

	icmd = InteractiveCMD(gpg)

	with pytest.raises(SystemExit):
		icmd.interactive_menu()

	remove_files(['secrets_tmp38'])

