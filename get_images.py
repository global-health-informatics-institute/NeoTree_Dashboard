from bs4 import BeautifulSoup
import requests

url = 'http://www.rebekkagudleifs.com/photos/scenery/'
extensions = ['jpg', 'jpeg','png']


# function to retrieve file names
def listFD(url, ext=''):
    page = requests.get(url).text

    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


# Loop to get image files
for ext in extensions:
    for file_url in listFD(url, ext):
        temp_name = file_url.split("/")
        file_name = temp_name[(len(temp_name) - 1)]
        file_object = requests.get(file_url)

        with open('assets/images/screenshots/%s' % file_name, 'wb') as local_file:
            local_file.write(file_object.content)

        print file_name