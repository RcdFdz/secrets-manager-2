import pytest
import json as j
from json_manager import JSONManager

def test_delete_element():
	json = {"One": 1, "Two": 2}
	jm = JSONManager(json)
	x = jm.delete_entry("Two")
	assert x == {"One":True}

def test_delete_last_element():
	json = {"One": 1}
	jm = JSONManager(json)
	x = jm.delete_entry("One")
	assert x == {}

def test_delete_element_does_not_exist():
	json = {"One": 1}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.delete_entry("Two")

def test_delete_from_empty_json():
	json = {}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.delete_entry("Two")

def test_modify_value():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	x = jm.modify_values("One", {"user": "user3"})
	assert x == {"One": {"user":"user3","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}

def test_modify_values_does_not_exist():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.modify_values("One",{"aaaa":"user3","password":"password3"})

def test_modify_id():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	x = jm.modify_id("One","Three")
	assert x == {"Three": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}

def test_modify_id_does_not_exist():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.modify_id("Four","Three")

def test_add_value():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	x = jm.add("Three",{"user":"user3","password":"password3","url":"url3","other":"other3"})
	assert x == {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}, "Three": {"user":"user3","password":"password3","url":"url3","other":"other3"}}

def test_add_value_exist():
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}, "Two": {"user":"user2","password":"password2","url":"url2","other":"other2"}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.add("Two",{"user":"user3","password":"password3","url":"url3","other":"other3"})

def test_get_keys():
	json = {"One": 1, "Two": 2}
	jm = JSONManager(json)
	x = jm.get_keys()
	assert x == ["One","Two"]

def test_get_keys_empty():
	json = {}
	jm = JSONManager(json)
	x = jm.get_keys()
	assert x == []

def test_get_keys_no_json():
	json = "Error"
	jm = JSONManager(json)
	with pytest.raises(ValueError):
		x = jm.get_keys()

def test_fix_json():
	json = {"user":"1","password":"2"}
	jm = JSONManager(json)
	x = jm.fix_json(j.dumps(json))

	for i in ['user','password','url','other']:
		if( i in json):
			assert x[i] == json[i]
		else:
			assert x[i] == ''

def test_fix_json_2():
	json = {"user":"1","password":"2","no":"aha"}
	jm = JSONManager(json)
	x = jm.fix_json(j.dumps(json))

	for i in ['user','password','url','other']:
		if( i in json):
			assert x[i] == json[i]
		else:
			assert x[i] == ''

def test_print_values(capsys):
	json = {"One": {"user":"user1","password":"password1","url":"url1","other":"other1"}}
	jm = JSONManager(json)
	jm.print_values('One', 'all')
	out, err = capsys.readouterr()

	assert out == 'User: user1\nPassword: password1\nUrl: url1\nOther: other1\n'

