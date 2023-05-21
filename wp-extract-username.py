import argparse
import requests
import re
import os
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}


def extract_usernames_rss(wordpress_url):    
    response = session.get(f"{wordpress_url}/feed/", headers=headers, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        try:
            all_usernames = []
            for item in soup.find_all("item"):
                creator = item.find("dc:creator")
                if creator and creator.text:
                    all_usernames.append(creator.text)
            return all_usernames
        except Exception as e:
            print(f"Failed to fetch usernames using RSS Feed. Error: {e} ")
            return []
    else:
        print(f"Failed to fetch usernames using RSSS Feed. Error: {response.text}")
        return []

def extract_usernames_rest_api(wordpress_url):
    api_url = wordpress_url + '/wp-json/wp/v2/users'
    response = session.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        users = response.json()
        usernames = [user['slug'] for user in users]
        return usernames
    else:
        print(f"Failed to fetch usernames using REST API. Error: {response.text}")
        return []

if __name__ == "__main__":
   usernames = extract_usernames_rest_api("https://wpuser:password@dev.careydayrit.com")
   print(usernames)