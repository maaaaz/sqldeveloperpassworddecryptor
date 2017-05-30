SQL Developer password decryptor
================================

Description
-----------
A simple script to decrypt stored passwords from the Oracle SQL Developer IDE.

Features
--------
* Support old v3 and current v4 passwords
* Comes in 2 flavors: a Jython and a Python script

Prerequisites
-----
#### Version 3
Passwords are stored encrypted in the `connections.xml` file in those locations:
* Windows: `C:\Users\<USER>\AppData\Roaming\SQL Developer\system<VERSION>\o.jdeveloper.db.connection.<VERSION>\connections.xml`
* Linux: `~/.sqldeveloper/system<VERSION>/o.jdeveloper.db.connection.<VERSION>/connections.xml`

#### Version 4
Passwords are stored encrypted in the aforementioned `connections.xml` file but the encryption key by default uses a machine-unique value `db.system.id` in the `product-preferences.xml` file accessible here:
* Windows: `C:\Users\<USER>\AppData\Roaming\SQL Developer\system<VERSION>\o.sqldeveloper.<VERSION>\product-preferences.xml`
* Linux: `~/.sqldeveloper/system<VERSION>/o.sqldeveloper.<VERSION>/product-preferences.xml`  
  
When exporting one or more connections in version 4, the user is asked to type a password: **that password is then used as a key to encrypt the entries instead of the `db.system.id` value.**

Options
-------
```
$ python sqldeveloperpassworddecryptor.py -h
Usage: sqldeveloperpassworddecryptor.py [options]
Version: 1.1

Options:
  -h, --help            show this help message and exit

  v3 and v4 parameters:
    -p ENCRYPTED_PASSWORD, --encrypted-password=ENCRYPTED_PASSWORD
                        (mandatory): password that you want to decrypt. Ex. -p
                        054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8

  v4 specific parameters:
    -d DB_SYSTEM_ID_VALUE, --db-system-id-value=DB_SYSTEM_ID_VALUE
                        (mandatory for v4): machine-unique value of
                        "db.system.id" attribute in the "product-
                        preferences.xml" file, or the export file encryption
                        key. Ex: -d 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee
```

Examples
--------
#### v3 password
```
$ jython sqldeveloperpassworddecryptor.jy -p 054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8
[+] encrypted password: 054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8

[+] decrypted password: password
```

#### v4 password
```
$ python sqldeveloperpassworddecryptor.py -d 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee -p Shz0tQgqkuAfLy65s21gTVD7wacDYwG6
[+] encrypted password: Shz0tQgqkuAfLy65s21gTVD7wacDYwG6
[+] db.system.id value: 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee

[+] decrypted password: s4gswagswaag!5465636MP
```

Dependencies
------------
* For the `Jython` version: well, only Jython (`apt-get install jython` or download it [here](http://www.jython.org/downloads.html))
* For the `Python` version: PyCrypto

Changelog
---------
* version 1.1 - 05/30/2017: shebang addition
* version 1.0 - 07/23/2014: Initial commit

Copyright and license
---------------------
sqldeveloperpassworddecryptor is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sqldeveloperpassworddecryptor is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with sqldeveloperpassworddecryptor. 
If not, see http://www.gnu.org/licenses/.

Greetings
---------
* ajokela for its [Java snippet for v3](https://gist.github.com/ajokela/1846191)
* AlessandroZ for its [Python snippet for v4](https://raw.githubusercontent.com/AlessandroZ/LaZagne/master/Linux/src/softwares/databases/sqldeveloper.py)

Contact
-------
* Thomas Debize < tdebize at mail d0t com >