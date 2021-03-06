import os

from bs4 import BeautifulSoup
import re
import json
import requests
from os import path
from os import system
from datetime import datetime
from requests.auth import HTTPBasicAuth

settings = {}
try:
    with open("config/app.config") as json_file:
        settings = json.load(json_file)
finally:
    pass

url = settings["repository_url"]


# function to start process
def initiate():
    extensions = ['jpg', 'jpeg', 'png']
    file_details = get_file_names(extensions)

    for file_url in file_details["file_names"]:
        temp_name = file_url.split("/")
        file_name = temp_name[(len(temp_name) - 1)]
        if path.exists('assets/images/screenshots/%s' % file_name):
            if file_details["max_date"] > int(path.getmtime('assets/images/screenshots/%s' % file_name)):
                print("File %s already exists but is old. Downloading" % file_name)
                download_file(file_url, file_name)
            else:
                print("File %s already exists" % file_name)
        else:
            print("Downloading file %s" % file_name)
            download_file(file_url, file_name)
    get_display_configuration()


# function to download a file
def download_file(file_url, file_name):
    if settings["authentication_type"] == "Basic HTTP Authentication":
        cmd = "wget -N --http-user='%s' --http-password='%s' --directory-prefix=assets/images/screenshots/ %s" % (settings['username'], settings['password'], file_url)
    else:
        cmd = "wget -N --directory-prefix=assets/images/screenshots/ %s" % file_url
    os.system(cmd)


# function to retrieve file names
def get_file_names(ext=''):
    if settings["authentication_type"] == "Basic HTTP Authentication":
        page = requests.get(url, auth=(settings['username'], settings['password'])).text
    else:
        page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    names = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(tuple(ext))]
    dates = re.findall(r'\d{2}-\w{3}-\d{4}\s\d{2}:\d{2}', str(soup))
    dates = [int(datetime.strptime(day, "%d-%b-%Y %H:%M").strftime('%s')) for day in dates]
    max_date = sorted(dates)[-1]

    return {"file_names": names, "max_date": max_date}


def get_display_configuration():
    file_url = '%smetabase_exports.json' % url
    if settings["authentication_type"] == "Basic HTTP Authentication":
        cmd = "wget -N --http-user='%s' --http-password='%s' --directory-prefix=config/ %s" % (settings['username'], settings['password'], file_url)
    else:
        cmd = "wget -N --directory-prefix=assets/images/screenshots/ %s" % file_url

    os.system(cmd)


if __name__ == "__main__":
    initiate()
