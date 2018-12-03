import urllib.request
import urllib.parse
from requests_html import HTML

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

url = 'http://localhost:8000/uploads/simple/'
r = requests.get(url)
print(r.headers)

cookie = r.headers.get('Set-Cookie').split(';')[0]
csrf_token = cookie.split('=')[1]
referer = r.headers.get('referer')
print(cookie)


files = MultipartEncoder(
    {'csrfmiddlewaretoken':csrf_token, 'myfile': ('test', open('../LICENSE', 'rb'), 'text/plain')}
)

headers = {}
headers['Content-Type'] = files.content_type
headers['Cookie'] = cookie
headers['referer'] = referer
r = requests.post(url, data=files, headers=headers)

print(HTML(html=r.content).html)
