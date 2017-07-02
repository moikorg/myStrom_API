#!/usr/bin/env python3

import configparser
from flask import Flask
import requests
import pprint


def configSectionMap(section):
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
#config.read('/root/bin/myStrom_API/config.rc')
config.read('config.rc')

uname = configSectionMap("Credentials")['username']
passwd = configSectionMap("Credentials")['password']
myStrom_url = configSectionMap("MyStrom")['baseurl']

auth_url = myStrom_url + 'auth?email={eMail}&password={password}'.format(eMail=uname, password=passwd)
r = requests.get(auth_url)
if r.status_code != 200:
    print ("Error, no connection and authentication possible")
    exit(1)

r_json = r.json()
if r_json['status'] != 'ok':
    print ("Authentication failed")
    exit(1)

# save the authorization token for all coming requests
authToken = r_json['authToken']

# get the device list
url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='devices', token=authToken)
#print (url_getStatus)
r = requests.get(url_getStatus)
if r.json()['status'] != 'ok':
    print ("Error getting the list")
    exit(1)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(r.json())

# get a list of connected devices
for myobject in r.json()['devices']:
    if myobject['name'] != '':
        if myobject['name'] == "Printer":
            printerID = myobject['id']
        elif myobject['name'] == "Anti Vol Stube":
            antiVolID = myobject['id']
            print (myobject['name'], myobject['id'])

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!<br>This is the myStrom API root"


@app.route("/printer")
def print_status():
    assert isinstance(printerID, object)

    # /mobile/device/switch
    url_getStatus = myStrom_url + '{method}?authToken={token}'.format(method='device/switch', token=authToken)
    r = requests.post(url_getStatus, data={'id': printerID, 'on': 'True'})
    if r.json()['status'] != 'ok':
        return "Error switching the device: Printer"
    print (r.json())

    return "Printer turned on"

@app.route("/light")
def ligth_toggle():

    url_post_light = myStrom_url + '{method}?authToken={token}'.format(method='device/switch', token=authToken)
    # toggle the light to off
    r = requests.post(url_post_light, data={'id': antiVolID, 'action': 'toggle'})
    if r.json()['status'] != 'ok':
        return "Error switching the device" + r.json()
#    pp = pprint.PrettyPrinter(indent=4)
#    pp.pprint(r.json())
    return ("okay")


if __name__ == "__main__":
    # run it on port 5001
    app.run(port=5001, host='0.0.0.0')
