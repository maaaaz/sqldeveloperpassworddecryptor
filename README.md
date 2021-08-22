SQL Developer password decryptor
================================

Description
-----------
A simple script to decrypt stored passwords from the Oracle SQL Developer IDE.

Features
--------
* Support old (v3, v4->v19.1) and new (from v19.2) password encryption
* Comes in 2 flavors: a Jython and a Python script

Prerequisites
-----
### Passwords
-------------

##### Version 3 until version 18.1
Passwords are stored encrypted in the `connections.xml` file in those locations:
* Windows: `%APPDATA%\SQL Developer\system<VERSION>\o.jdeveloper.db.connection.<VERSION>\connections.xml`
* Linux: `~/.sqldeveloper/system<VERSION>/o.jdeveloper.db.connection.<VERSION>/connections.xml`

##### Version 18.3 and newer
Passwords are stored encrypted in the `connections.json` file in those locations:
* Windows: `%APPDATA%\SQL Developer\system<VERSION>\o.jdeveloper.db.connection\connections.json`
* Linux: `~/.sqldeveloper/system<VERSION>/o.jdeveloper.db.connection/connections.json`

### Installation ID
-------------------
Passwords are stored encrypted in the aforementioned `connections.xml` and `connections.json` file but the encryption key by default uses an installation-unique random UUID value `db.system.id` in the `product-preferences` file.

##### Version 3 until version 18.1
* Windows: `%APPDATA%\SQL Developer\system<VERSION>\o.sqldeveloper.<VERSION>\product-preferences.xml`
* Linux: `~/.sqldeveloper/system<VERSION>/o.sqldeveloper.<VERSION>/product-preferences.xml`  
  
##### Version 18.3 and newer
* Windows: `%APPDATA%\SQL Developer\system<VERSION>\o.sqldeveloper\product-preferences.xml`
* Linux: `~/.sqldeveloper/system<VERSION>/o.sqldeveloper/product-preferences.xml`  
  
When exporting one or more connections from **version 4**, the user is asked to type a password: **that password is then used as a key to encrypt the entries instead of the `db.system.id` value.**


Options
-------
```
$ python sqldeveloperpassworddecryptor.py -h
Usage: sqldeveloperpassworddecryptor.py [options]
Version: 2.1

Options:
  -h, --help            show this help message and exit

  Main parameters:
    -p ENCRYPTED_PASSWORD, --encrypted-password=ENCRYPTED_PASSWORD
                        (mandatory): password that you want to decrypt. Ex. -p
                        054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8
    -d DB_SYSTEM_ID_VALUE, --db-system-id-value=DB_SYSTEM_ID_VALUE
                        (mandatory from v4): installation-unique value of
                        "db.system.id" attribute in the "product-
                        preferences.xml" file, or the export file encryption
                        key. Ex: -d 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee
    -o, --old           (mandatory between v4 and v19.1) if the password you
                        want to decrypt is for a product version between 4 and
                        19.1
```

Examples
--------
#### v3 password
```
$ jython sqldeveloperpassworddecryptor.jy -p 054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8
[+] encrypted password: 054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8

[+] decrypted password: password
```

#### v4 -> v19.1 password
```
$ python sqldeveloperpassworddecryptor.py -d 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee -p Shz0tQgqkuAfLy65s21gTVD7wacDYwG6 -o
sqldeveloperpassworddecryptor.py version 2.1

[+] encrypted password: Shz0tQgqkuAfLy65s21gTVD7wacDYwG6
[+] db.system.id value: 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee

[+] decrypted password: s4gswagswaag!5465636MP
```

#### from v19.2 password
```
$ python sqldeveloperpassworddecryptor.py -d 7d97189a-4e22-4061-bc07-35b9d2b39f3c -p "LUA63VW21TqaHNJSvKF6DI8zv1/dvXzBhyMPVN8lAws="
sqldeveloperpassworddecryptor.py version 2.1

[+] encrypted password: LUA63VW21TqaHNJSvKF6DI8zv1/dvXzBhyMPVN8lAws=
[+] db.system.id value: 7d97189a-4e22-4061-bc07-35b9d2b39f3c

[+] decrypted password: password1
```

Dependencies and installation
-----------------------------
* For the `Jython` version: well, only Jython (`apt-get install jython` or download it [here](https://www.jython.org/download))
* For the `Python` version:
  * The **easiest way** to setup everything: `pip install sqldeveloperpassworddecryptor` and then directly use `$ sqldeveloperpassworddecryptor`
  * Or manually install PyCryptodome: `pip install pycryptodomex`

Changelog
---------
* version 2.1 - 08/11/2021: new encryption type support (from v19.2)
* version 2.0 - 11/11/2020: Python 3 support
* version 1.2 - 07/14/2017: replacing PyCrypto by PyCryptodomex for [these reasons](https://blog.sqreen.io/stop-using-pycrypto-use-pycryptodome/)
* version 1.1 - 05/30/2017: shebang addition
* version 1.0 - 07/23/2014: Initial commit

Copyright and license
---------------------
sqldeveloperpassworddecryptor is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software  Foundation, either version 3 of the License, or (at your option) any later version.

sqldeveloperpassworddecryptor is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with sqldeveloperpassworddecryptor. 
If not, see http://www.gnu.org/licenses/.

Greetings
---------
* ajokela for its [Java snippet for v3](https://gist.github.com/ajokela/1846191)
* AlessandroZ for its [Python snippet for v4](https://raw.githubusercontent.com/AlessandroZ/LaZagne/master/Linux/src/softwares/databases/sqldeveloper.py)

Contact
-------
* Thomas Debize < tdebize at mail d0t com >