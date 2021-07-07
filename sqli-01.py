#!/usr/bin/python3

# This script scans the console output logs of a Jenkins host

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings
from bs4 import BeautifulSoup

import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="Specify a target. \nE.g. -t jenkins.local")
args = parser.parse_args()

if not args.target:
    print("[!] You need to spcify a target.")
    print("[*] Example usage: dumplings.py -t jenkins.local")
    exit(0)

host = args.target

def extract_element_from_json(obj, path):
    def extract(obj, path, ind, arr):
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr

    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr


def list_all_builds():
    jobUrls = []

    jenkinsFilter = ["jobs"]

    for i in range(4):
        buildListApi = 'https://' + host + '/jenkins/api/json?tree=' + ('jobs[' * (i + 1)) + 'builds[url]' + (
                    ']' * (i + 1))
        print("[*] Grabbing urls from %s" % buildListApi)
        buildListResp = requests.get(buildListApi).json()

        wUrlFilter = jenkinsFilter.copy()
        wUrlFilter.append("builds")
        wUrlFilter.append("url")
        jobUrls.append(extract_element_from_json(buildListResp, wUrlFilter))
        jenkinsFilter.append("jobs")

    return jobUrls


def check_secrets(urlList):
    secretList = []

    for urlChunk in urlList:
        for url in urlChunk:
            if url is not None:
                consoleUrl = url + 'consoleFull'
                resp = requests.get(consoleUrl)
                resp.raise_for_status()

                # extract console
                soup = BeautifulSoup(resp.text, "html.parser")
                pre = soup.find('pre', {'class', 'console-output'})

                file = open('currentResp.txt', 'w')
                file.write(str(pre))
                file.close()

                secrets = SecretsCollection()
                with default_settings():
                    secrets.scan_file('currentResp.txt')

                print("Secrets found in " + consoleUrl)
                print(json.dumps(secrets.json(), indent=2))
                secretList.append(secrets.json())


if __name__ == '__main__':
    check_secrets(list_all_builds())
