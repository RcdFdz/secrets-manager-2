import pytest
import builtins
import os
import json
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

def test_show_keys(capsys):
	message = '{"One": 1, "Two": 2}'

	gpg = GPGTools(file = 'secrets_tmp3', key = '12345')
	gpg.encrypt_content(message)

	icmd = InteractiveCMD(gpg)
	icmd.show_keys()
	out, err = capsys.readouterr()

	assert out == 'One\nTwo\n'

	remove_files(['secrets_tmp3'])


