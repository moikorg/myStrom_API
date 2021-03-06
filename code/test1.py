#!/usr/bin/env python3

import requests
from sys import exit
import pprint
import configparser


def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# get the config data from the config file
config = configparser.ConfigParser()
config.read('./config.rc')

uname = ConfigSectionMap("Credentials")['username']
passwd = ConfigSectionMap("Credentials")['password']
myStrom_url = ConfigSectionMap("MyStrom")['baseurl']
# TODO: test if this is in the PyCharm Todo list



auth_url = myStrom_url + 'auth?email={eMail}&password={password}'.format(eMail=uname, password=passwd)
r = requests.get(auth_url)
if r.status_code != 200:
    print ("Error, no connection and authentication possible")
    exit(1)

r_json= r.json()
if r_json['status'] != 'ok':
    print ("Authentication failed")
    exit(1)

# save the authorization token for all coming requests
authToken = r_json['authToken']

# get the device list
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='devices', token=authToken)
print (url_getStatus)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print ("Error getting the list")
    exit(1)

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(r.json())

# get a list of connected devices and pick the printer ID
for myobject in r.json()['devices']:
    if myobject['name'] != '':
        if myobject['name'] == "Printer":
            print (myobject['name'], myobject['id'])

# get the weather
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='weather', token=authToken)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print ("Error getting the list")
    exit(1)
print (r.json())

# get the profile
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='profile', token=authToken)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print ("Error getting the list")
    exit(1)
print (r.json())


# upgrade device
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='device/firmware/upgrade', token=authToken)
r = requests.post(url_getStatus, data = {'id': '0013C1232E4A'})
if r.json()['status'] != 'ok':
    print ("Error updating")
print (r.json())


# # switch a device to on/off
# # /mobile/device/switch
# url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='device/switch', token=authToken)
# r = requests.post(url_getStatus, data = {'id': '0013C121EE93', 'on': 'True'})
# if r.json()['status'] != 'ok':
#     print ("Error switching the device")
#     print (r.json())
#     exit(1)
# print (r.json())
