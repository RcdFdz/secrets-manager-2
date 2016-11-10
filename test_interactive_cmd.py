import pytest
import builtins
import os
import json
import clipboard
from interactive_cmd import InteractiveCMD
from gpg_tools import GPGTools

def remove_files(list):
	for file in list:
		os.remove(str(os.getcwd()) + '/' + file)

def test_exit():
	message = '{"One": {"user":"example","pass":"example","url":"example","other":"example"}}'

	gpg = GPGTools(file = 'secrets_tmp', key = '12345')
	gpg.encrypt_content(message)

	icmd = InteractiveCMD(gpg)
	with pytest.raises(SystemExit):
		icmd.exit()

	remove_files(['secrets_tmp'])

def test_add_content(monkeypatch):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"},"example": {"user":"example","password":"example","url":"example","other":"example"}}'
	gpg = GPGTools(file = 'secrets_tmp4', key = '12345')
	gpg.encrypt_content(message)

	message2 = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'
	gpg2 = GPGTools(file = 'secrets_tmp5', key = '12345')
	gpg2.encrypt_content(message2)
	icmd = InteractiveCMD(gpg2)

	def mock_input_user(*args, **kwargs):
		return 'example'

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd.add_content()

	json_gpg = json.loads(str(gpg.decrypt_content()))
	json_gpg2 = json.loads(str(gpg2.decrypt_content()))

	assert json_gpg == json_gpg2

	remove_files(['secrets_tmp4','secrets_tmp5'])

def test_add_content_no_secrets():
	return True

def test_show_keys(capsys):
	message = '{"One": 1, "Two": 2}'

	gpg = GPGTools(file = 'secrets_tmp3', key = '12345')
	gpg.encrypt_content(message)

	icmd = InteractiveCMD(gpg)
	icmd.show_keys()
	out, err = capsys.readouterr()

	assert out == 'One\nTwo\n'

	remove_files(['secrets_tmp3'])

def test_decrypt_content_ok(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file = 'secrets_tmp6', key = '12345')
	gpg.encrypt_content(message)

	aux = ['One','Y','N']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.print_decrypt_content()
	out, err = capsys.readouterr()

	assert out == 'user: user1\npassword: pass1\nurl: url1\nother: other1\n'

	remove_files(['secrets_tmp6'])

def test_decrypt_content_ko(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file = 'secrets_tmp6', key = '12345')
	gpg.encrypt_content(message)

	aux = ['One','Y','N']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.print_decrypt_content()
	out, err = capsys.readouterr()

	assert out != 'user: user\npassword: pass1\nurl: url1\nother: other1\n'

	remove_files(['secrets_tmp6'])

def test_decrypt_content_fail_id(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file = 'secrets_tmp6', key = '12345')
	gpg.encrypt_content(message)

	aux = ['Two','One','Y','N']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.print_decrypt_content()
	out, err = capsys.readouterr()

	assert out == 'user: user1\npassword: pass1\nurl: url1\nother: other1\n'

	remove_files(['secrets_tmp6'])

def test_decrypt_content_copy_clipboard(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file = 'secrets_tmp6', key = '12345')
	gpg.encrypt_content(message)

	aux = ['One','N','password']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.print_decrypt_content()
	out = clipboard.paste()

	assert out == 'pass1\n'

	remove_files(['secrets_tmp6'])

def test_id_or_list(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file = 'secrets_tmp6', key = '12345')
	gpg.encrypt_content(message)

	aux = ['list', 'One']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.id_or_list()
	out, err = capsys.readouterr()

	assert out == 'One\n'

	remove_files(['secrets_tmp6'])

def test_modify_content(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'
	message2 = '{"One": {"user":"user2","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file='secrets_tmp7', key='12345')
	gpg.encrypt_content(message)

	gpg2 = GPGTools(file='secrets_tmp8', key='12345')
	gpg2.encrypt_content(message2)

	aux = ['One', 'user2', 'pass1', 'url1','other1']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.modify_content()
	out, err = capsys.readouterr()

	file1 = open('secrets_tmp7','r')
	file2 = open('secrets_tmp8','r')

	json1 = json.loads(str(gpg.decrypt_content()))
	json2 = json.loads(str(gpg2.decrypt_content()))

	assert json1['One']['user'] == json2['One']['user']
	assert out == 'Leave all elements without value for delete the entry\nDone! Identifier One has been modified\n'

	remove_files(['secrets_tmp7','secrets_tmp8'])

def test_modify_content_delete(monkeypatch, capsys):
	message = '{"One": {"user":"user1","password":"pass1","url":"url1","other":"other1"}}'

	gpg = GPGTools(file='secrets_tmp7', key='12345')
	gpg.encrypt_content(message)

	aux = ['One', '', '', '','']
	def mock_input_user(*args, **kwargs):
		a = aux[0]
		del aux[0]
		return a

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	icmd = InteractiveCMD(gpg)
	icmd.modify_content()
	out, err = capsys.readouterr()

	file1 = open('secrets_tmp7','r')

	json1 = json.loads(str(gpg.decrypt_content()))

	assert json1 == {}
	assert out == 'Leave all elements without value for delete the entry\nDone! Identifier One has been deleted\n'

	remove_files(['secrets_tmp7'])
