# -*- coding: utf-8 -*-

# This file is part of sqldeveloperpassworddecrypter.
#
# Copyright (C) 2015, Thomas Debize <tdebize at mail.com>
# All rights reserved.
#
# sqldeveloperpassworddecrypter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sqldeveloperpassworddecrypter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sqldeveloperpassworddecrypter.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function 
from Crypto.Cipher import DES
import sys
from xml.etree import ElementTree
import base64
import array
import hashlib
import codecs

# Script version
VERSION = '1.2'
PASSWORD_ENCODING = 'ISO-8859-1'

import argparse
import platform

sql_developer_directory = '%APPDATA%\\SQL Developer\\' if platform.system() == 'Windows' else '~/.sqldeveloper/'

# Options definition
parser = argparse.ArgumentParser(description='Decodes passwords from SQL developer. If you don\'t explicitly specify an encrypted password or a connections file, then %(prog)s will search through "{0}" for connections.xml files and process them.'.format(sql_developer_directory.replace('%', '%%')))
parser.add_argument('--version', action='version', version='%(prog)s '+ VERSION)
main_grp = parser.add_argument_group('v3 and v4 parameters')
main_grp.add_argument('-p', '--encrypted-password', help='password that you want to decrypt from "o.jdeveloper.db.connection.*/connections.xml". Ex. -p 054D4844D8549C0DB78EE1A98FE4E085B8A484D20A81F7DCF8')
main_grp.add_argument('-c', '--connections-file', help='"connections.xml" file containing encrypted passwords. Ex. -c connections.xml')
v4_grp = parser.add_argument_group('v4 specific parameters')
v4_grp.add_argument('-d', '--db-system-id-value', help='machine-unique value of "db.system.id" attribute in the "o.sqldeveloper.*/product-preferences.xml" file. Ex: -d 6b2f64b2-e83e-49a5-9abf-cb2cd7e3a9ee')

# Handful functions
def des_cbc_decrypt(encrypted_password, decryption_key, iv):
	unpad = lambda s : s[:-ord(s[len(s)-1:])]
	crypter = DES.new(decryption_key, DES.MODE_CBC, iv)
	decrypted_password = unpad(crypter.decrypt(encrypted_password))
	
	return decrypted_password

def decrypt_v4(encrypted, db_system_id, parser):
	encrypted_password = base64.b64decode(encrypted)
	
	salt = codecs.decode('051399429372e8ad', 'hex')
	num_iteration = 42
			
	# key generation from a machine-unique value with a fixed salt
	key = codecs.encode(db_system_id, 'ASCII') + salt
	for i in range(num_iteration):
		m = hashlib.md5(key)
		key = m.digest()
	
	secret_key = key[:8]
	iv = key[8:]
	
	decrypted = des_cbc_decrypt(encrypted_password, secret_key, iv)
	
	return codecs.decode(decrypted, PASSWORD_ENCODING) 

def decrypt_v3(encrypted, parser):
	if len(encrypted) % 2 != 0:
		parser.error('v3 encrypted password length is not even (%s), aborting.' % len(encrypted))
	
	if not(encrypted.startswith("05")):
		parser.error('v3 encrypted password string not beginning with "05", aborting.\nRemember, for a v4 password you need the db.system.id value !')
	
	encrypted = codecs.decode(encrypted, 'hex')
	secret_key = encrypted[1:9]
	encrypted_password = encrypted[9:]
	iv = "\x00" * 8
	
	decrypted = des_cbc_decrypt(encrypted_password, secret_key, iv)
	
	return codecs.decode(decrypted, PASSWORD_ENCODING)

def search_connections_files():
	import os
	for root, dirs, files in os.walk(os.path.expandvars(sql_developer_directory)):
		if 'connections.xml' in files:
			yield os.path.join(root, 'connections.xml')
	
def main(options):
	"""
		Dat main
	"""
	global parser, VERSION
	print('sqldeveloperpassworddecryptor.py version %s\n' % VERSION)
	
	if options.encrypted_password:
		print("[+] encrypted password: %s" % options.encrypted_password)
		if options.db_system_id_value:
			# v4 decryption
			print("[+] db.system.id value: %s" % options.db_system_id_value)
			print("\n[+] decrypted password: %s" % decrypt_v4(options.encrypted_password, options.db_system_id_value, parser))
		
		else:
			#v3 decryption
			print("\n[+] decrypted password: %s" % decrypt_v3(options.encrypted_password, parser))
		return
	
	if options.connections_file:
		connections_files = [options.connections_file]
	else:
		connections_files = search_connections_files()
	
	processed_file = False
	for connections_file in connections_files:
		processed_file = True
		print("[+] Parsing file: %s" % connections_file)
		root = ElementTree.parse(connections_file).getroot()
		for level1 in root.findall('.//Reference'):
			con = {}
			for level2 in level1.findall('.//StringRefAddr'):
				if level2.get('addrType') == 'password':
					con[level2.get('addrType')] = decrypt_v3(level2[0].text, parser)
				elif level2.get('addrType') in ['ConnName', 'hostname', 'port', 'user', 'serviceName']: 
					con[level2.get('addrType')] = level2[0].text
			print("[+] Decrypted Connection: %s" % con)
	if not processed_file:
		parser.error("Could not find a connections.xml file. Please specify a file or password to decrypt.")
	
	print("[+] Task successfully completed.")
	
if __name__ == "__main__" :
	options = parser.parse_args()
	main(options)
