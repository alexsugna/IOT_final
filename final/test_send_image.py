import requests

url = 'http://18.222.187.211:5000/identify_person?personGroup_name=testing_personGroupppp'
#url = 'http://127.0.0.1:5000/list_personGroups'

files = { 'file' : open('obama2.jpg', 'rb') }

response = requests.request("POST", url, files=files)
print(response.text)
