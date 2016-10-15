import pytest
from secrets_manager import SecretsManager

def test_delete_element():
	json = {'One':1, 'Two':2}
	sm = SecretsManager(json)
	x = sm.delete_entry('Two')
	assert x == {'One':True}

def test_delete_last_element():
	json = {'One':1}
	sm = SecretsManager(json)
	x = sm.delete_entry('One')
	assert x == {}

def test_delete_element_do_not_exist():
	json = {'One':1}
	sm = SecretsManager(json)
	with pytest.raises(KeyError):
		x = sm.delete_entry('Two')

def test_delete_from_empty_json():
	json = {}
	sm = SecretsManager(json)
	with pytest.raises(KeyError):
		x = sm.delete_entry('Two')
