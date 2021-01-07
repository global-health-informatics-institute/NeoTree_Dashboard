from bs4 import BeautifulSoup
import json
import requests
from os import path

settings = {}
try:
    with open("config/app.config") as json_file:
        settings = json.load(json_file)
finally:
    pass

url = settings["repository_url"]

# url = 'http://www.rebekkagudleifs.com/photos/scenery/'


def initiate():
    extensions = ['jpg', 'jpeg', 'png']
    files = get_file_names(extensions)
    for file_url in files:
        temp_name = file_url.split("/")
        file_name = temp_name[(len(temp_name) - 1)]
        if path.exists('assets/images/screenshots/%s' % file_name):
            print("File %s already exists" % file_name)
        else:
            print("Downloading file %s" % file_name)
            if settings["authentication_type"] == "Basic HTTP Authentication":
                file_object = requests.get(file_url, auth=(settings['username'], settings['password']))
            else:
                file_object = requests.get(file_url)

            with open('assets/images/screenshots/%s' % file_name, 'wb') as local_file:
                local_file.write(file_object.content)


# function to retrieve file names
def get_file_names(ext=''):
    if settings["authentication_type"] == "Basic HTTP Authentication":
        page = requests.get(url, auth=(settings['username'], settings['password'])).text
    else:
        page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(tuple(ext))]


if __name__ == "__main__":
    initiate()
