import pytest
from json_manager import JSONManager

def test_delete_element():
	json = {'One': 1, 'Two': 2}
	jm = JSONManager(json)
	x = jm.delete_entry('Two')
	assert x == {'One':True}

def test_delete_last_element():
	json = {'One': 1}
	jm = JSONManager(json)
	x = jm.delete_entry('One')
	assert x == {}

def test_delete_element_does_not_exist():
	json = {'One': 1}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.delete_entry('Two')

def test_delete_from_empty_json():
	json = {}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.delete_entry('Two')

def test_modify_value():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	x = jm.modify_values('One', {'user': 'user3'})
	assert x == {'One': {'user':'user3','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}

def test_modify_values_does_not_exist():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.modify_values('One',{'aaaa':'user3','pass':'pass3'})

def test_modify_id():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	x = jm.modify_id('One','Three')
	assert x == {'Three': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}

def test_modify_id_does_not_exist():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.modify_id('Four','Three')

def test_add_value():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	x = jm.add('Three',{'user':'user3','pass':'pass3','url':'url3','other':'other3'})
	assert x == {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}, 'Three': {'user':'user3','pass':'pass3','url':'url3','other':'other3'}}

def test_add_value_exist():
	json = {'One': {'user':'user1','pass':'pass1','url':'url1','other':'other1'}, 'Two': {'user':'user2','pass':'pass2','url':'url2','other':'other2'}}
	jm = JSONManager(json)
	with pytest.raises(KeyError):
		x = jm.add('Two',{'user':'user3','pass':'pass3','url':'url3','other':'other3'})

def test_get_keys():
	json = {'One': 1, 'Two': 2}
	jm = JSONManager(json)
	x = jm.get_keys()
	assert x == ['One','Two']

def test_get_keys_empty():
	json = {}
	jm = JSONManager(json)
	x = jm.get_keys()
	assert x == []

def test_get_keys_no_json():
	json = 'Error'
	jm = JSONManager(json)
	with pytest.raises(ValueError):
		x = jm.get_keys()
