#!/usr/local/bin/python

import requests
from sys import exit
import pprint

# r = requests.get('https://api.github.com/events')
# print(r)
# print(r.text)

uname = 'xx.org'
passwd = 'xxx'
# auth_data = json.dumps({'email':uname, 'password':passwd})

myStrom_url = 'https://mystrom.ch/mobile/'

auth_url = myStrom_url + 'auth?email={eMail}&password={password}'.format(eMail=uname, password=passwd)
r = requests.get(auth_url)
if r.status_code != 200:
    print "Error, no connection and authentication possible"
    exit(1)

r_json= r.json()
if r_json['status'] != 'ok':
    print "Authentication failed"
    exit(1)

# save the authorization token for all coming requests
authToken = r_json['authToken']

# get the device list
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='devices', token=authToken)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print "Error getting the list"
    exit(1)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(r.json())

for myobject in r.json()['devices']:
    if myobject['name'] == 'Raspberry Pi':
        print myobject

# get the weather
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='weather', token=authToken)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print "Error getting the list"
    exit(1)
print r.json()
