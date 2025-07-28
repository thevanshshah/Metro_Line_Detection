import requests

url = "http://127.0.0.1:8000/upload"
files = {'file': open('m1.jpeg', 'rb')}  # your image here
data = {'mode': 'detection', 'fps': '0'}

response = requests.post(url, files=files, data=data)
print(response.status_code)
print(response.json())
