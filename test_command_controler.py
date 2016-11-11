import pytest
import builtins
import os
import json
from command_controler import CommandControler
from gpg_tools import GPGTools

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

def test_get_json():
	gpg = get_GPG('{"One": 1, "Two": 2}', 'secrets_tmp1', '12345')
	cmdc = CommandControler(gpg)
	json = cmdc.get_json()

	assert json == '{"One": 1, "Two": 2}'

	remove_files(['secrets_tmp1'])

def test_set_json():
	gpg = get_GPG('{"One": 1, "Two": 2}', 'secrets_tmp2', '12345')

	gpg2 = GPGTools(file = 'secrets_tmp3', key = '12345')
	cmdc = CommandControler(gpg2)
	cmdc.set_json('{"One": 1, "Two": 2}')

	file1 = open('secrets_tmp2', 'r')
	file2 = open('secrets_tmp3', 'r')

	assert file1.read() != file2.read()

	remove_files(['secrets_tmp2', 'secrets_tmp3'])

def test_get_keys():
	gpg = get_GPG('{"One": 1, "Two": 2}', 'secrets_tmp4', '12345')
	cmdc = CommandControler(gpg)
	keys = cmdc.get_keys()

	assert keys == ['One', 'Two']

	remove_files(['secrets_tmp4'])

def test_add_content(monkeypatch):
	gpg = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"example": {"user":"example","password":"example","url":"example","other":"example"}}',
						'secrets_tmp5', '12345')

	gpg2 = get_GPG('{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}',
						'secrets_tmp6', '12345')

	json_msg = '{"example": {"user":"example","password":"example","url":"example","other":"example"}}'
	cmdc = CommandControler(gpg2)
	cmdc.add_content(json_msg)

	json_gpg = json.loads(str(gpg.decrypt_content()))
	json_gpg2 = json.loads(str(gpg2.decrypt_content()))

	assert json_gpg == json_gpg2

	remove_files(['secrets_tmp5', 'secrets_tmp6'])

def test_show_keys(capsys):
	gpg = get_GPG('{"One": 1, "Two": 2}', 'secrets_tmp7', '12345')
	cmdc = CommandControler(gpg)
	cmdc.show_keys()
	out, err = capsys.readouterr()

	assert out == 'One\nTwo\n'

	remove_files(['secrets_tmp7'])

def test_show_keys_empty(capsys):
	gpg = get_GPG('{}', 'secrets_tmp8', '12345')

	cmdc = CommandControler(gpg)
	cmdc.show_keys()
	out, err = capsys.readouterr()

	assert out == ''
	remove_files(['secrets_tmp8'])

def test_show_keys_no_json(capsys):
	gpg = get_GPG('d', 'secrets_tmp9', '12345')

	with pytest.raises(ValueError):
		cmdc = CommandControler(gpg)
		cmdc.show_keys()
		out, err = capsys.readouterr()
		assert out == ''

	remove_files(['secrets_tmp9'])

def test_update_keys():
	get_files('secrets_tmp10', 'secrets_tmp11')

	gpg = GPGTools(file = 'secrets_tmp10', key = '12345')
	cmdc = CommandControler(gpg)
	cmdc.update_keys()

	file1 = open('secrets_tmp10','r')
	file2 = open('secrets_tmp11','r')

	assert file1.read() != file2.read()

	remove_files(['secrets_tmp10','secrets_tmp11'])

def test_no_update_keys():
	''' This test ensure that the codification works properly
	in the future this could be moved to the test_gpg_tools
	'''
	get_files('secrets_tmp12', 'secrets_tmp13')

	gpg = GPGTools(file = 'secrets_tmp12', key = '12345')
	cmdc = CommandControler(gpg)

	file1 = open('secrets_tmp12','r')
	file2 = open('secrets_tmp13','r')

	assert file1.read() == file2.read()

	remove_files(['secrets_tmp12','secrets_tmp13'])
