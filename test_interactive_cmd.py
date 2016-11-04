import pytest
import builtins
import os
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
	message = '{"One": {"user":"example","pass":"example","url":"example","other":"example"}}'

	gpg = GPGTools(file = 'secrets_tmp4', key = '12345')
	gpg.encrypt_content(message)

	gpg2 = GPGTools(file = 'secrets_tmp5', key = '12345')
	icmd = InteractiveCMD(gpg2)

	def mock_input_user(*args, **kwargs):
		return 'example'

	monkeypatch.setattr(builtins, 'input',mock_input_user)

	x = icmd.add_content()

	file1 = open('secrets_tmp4','r')
	file2 = open('secrets_tmp5','r')

	assert file1.read() == file2.read()

	remove_files(['secrets_tmp4','secrets_tmp5'])

# def test_raw_input(monkeypatch):
#     ''' Get user input without actually having a user type letters using
#     monkeypatch. '''
#     def mock_raw_input(*args, **kwargs):
#         ''' Act like someone just typed 'yolo'. '''
#         return 'yolo';

#     # Put the mock_raw_input in place of the actual raw_input on the
#     # __builtin__ module.
#     monkeypatch.setattr(__builtin__, 'raw_input', mock_raw_input)

#     # retval should now contain 'yolo'
#     retval = raw_input()

#     assert retval == 'yolo'

