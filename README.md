### Password Manager
The aim to the present project is to solve the shared secrets problem in small teams.

### How it works
The first time that the script is runs asks for key/value input and generates the secrets file by using the public keys saved in pub-keys folder.

Before the secret file is generated the menu accepts:
* Add Key/Value Pair
* Exit

Once there is at least one secret, the application allows to work with an small CRUD in interactive mode.

The menu accepts:
* Add Key/Value Pair
* Modify/Delete Key/Value Pair
* Decrypt Key/Value Pair
* Show Keys
* Update public keys
* Exit

There is also the posibility to work without interactive mode, by using terminal arguments:

```
➜  secrets-manager-3 git:(master) ✗ python3 s-manager.py -h

usage: s-manager.py [-h] [-i] [-l] [-k identifier] [-v identifier]
                      [-a identifier]

Manager for sensible information under PGP

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     display the interactive menu for s-manager
  -l, --list            list all the stored identifiers
  -k identifier, --key identifier
                        return the key for the given identifier
  -v identifier, --value identifier
                        return the value for the given identifier
  -a identifier, --all identifier
                        display the key and value pair for the given
                        identifier
```

### Requirements
This projects requires python3 and GPG Suite version 2016.07 (https://gpgtools.org/) or greater.

Also will be required to run `pip3 install -r requirements.txt`.

### TODO

* Add option to modify Identifier
* Add option to add directly from command a key/value/note
* Modify ONLY identifier/key/value/note should be an option
