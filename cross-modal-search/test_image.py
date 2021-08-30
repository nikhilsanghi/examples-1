import cv2
import base64
import requests
import json
from jina import Document
import os
text = 'a group of 3 people'
headers = {
    'Content-Type': 'application/json',
}
data = '{"top_k":20,"mode":"search","data":["' + text + '"]}'
response = requests.post(
    'http://0.0.0.0:45678/search', headers=headers, data=data)
res = response.json()

with open('data.json', 'w') as f:
    json.dump(res, f)


def print_pic(b64_string, i):
    doc = Document(b64_string)
    doc.convert_image_datauri_to_blob()
    # print(doc.blob)
    x = base64.b64encode(doc.uri.encode('ascii'))
    content = base64.b64decode(x)
    cv2.imwrite(str(i)+'.jpg', cv2.cvtColor(doc.blob, cv2.COLOR_RGB2BGR))


with open('data.json', 'r') as openfile:
    data = json.load(openfile)
    directory=r'test_image_results'
    os.chdir(directory)

    for i in range(len(data['data']['docs'][0]['matches'])):
        b64_string = data['data']['docs'][0]['matches'][i]
        print_pic(b64_string, i)


