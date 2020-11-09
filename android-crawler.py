#
#   Brandon Merhai
#
# 
import re
import requests
from bs4 import BeautifulSoup
import os
import html5lib

URL = 'https://developer.android.com/reference/android/app/ActionBar'
page = requests.get(URL)
base_url = 'https://developer.android.com'
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, 'outFiles')

try:
    os.mkdir(output_dir)
except OSError:
    if os.path.isdir(output_dir):
        print("Directory exists. Continuing...")
    else:
        print("Failed to create directory 'outFiles'. Please check permissions.")
else:
    print("Successfully created directory 'outFiles'.")

soup = BeautifulSoup(page.content, 'html5lib')
results = soup.find('span', text="android.app")

children_android_app = results.parent.parent.find('span', text="Classes")
parent_app_classes = children_android_app.parent.parent
links = parent_app_classes.find_all('a', class_='devsite-nav-title')

page = requests.get('https://developer.android.com/reference/android/app/ActionBar.OnMenuVisibilityListener')
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find('span', text="android.app")

interfaces_android_app = results.parent.parent.find('span', text="Interfaces")
parent_app_interfaces = interfaces_android_app.parent.parent
links_interfaces = parent_app_interfaces.find_all('a', class_='devsite-nav-title')

page = requests.get('https://developer.android.com/reference/android/app/AuthenticationRequiredException')
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find('span', text="android.app")

exceptions_android_app = results.parent.parent.find('span', text="Exceptions")
parent_app_exceptions = exceptions_android_app.parent.parent
links_exceptions = parent_app_exceptions.find_all('a', class_='devsite-nav-title')

organized = dict()

links_app_classes = []

links.extend(links_interfaces)
links.extend(links_exceptions)

for item in links:
    links_app_classes.append(base_url + item['href'])

size = len(links_app_classes)
num = 1

def createNotes(url, dictionary):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')

    print("Working on %d of %d: %s." % (num, size, url.split('/')[-1]))

    content = soup.find(id='jd-content')
    elements = content.find_all('h2', class_='api-section')
    accepted = ['Fields', 'Public constructors Private constructors', 'Public methods Private methods', 'Constants']
    fileName = os.path.join(output_dir, url.split('/')[-1])

    for item in elements:
        if item.text in accepted:
            for tag in item.find_next_siblings('div'):
                if tag.find('p', class_='caution'):
                    label = str(tag.find('h3', class_='api-name').text)
                    info = str(tag.find('p', class_='caution').text.replace("\n", " ").replace("       ", " ").replace("     ", " "))

                    with open(fileName, "a+") as f:
                        f.write("%s:%s\n" % (label, info))

                elif tag.find('p', class_='note'):
                    label = str(tag.find('h3', class_='api-name').text)
                    info = str(tag.find('p', class_='note').text.replace("\n", " "))

                    with open(fileName, "a+") as f:
                        f.write("%s:%s\n" % (label, info))

for item in links_app_classes:
    createNotes(item, organized)
    num = num + 1

print("Completed")