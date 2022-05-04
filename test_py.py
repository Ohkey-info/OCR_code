import requests
import uuid
import time
import json

api_url = 'https://1mte94hdpr.apigw.ntruss.com/custom/v1/15641/df7e3d874c4ebcd0839255e7bb5ecec3d3dc754994d59c437e615e4934d6fdcd/general'
secret_key = 'UXdxaFVvdVRrSWRVQnRtUFhZVWZpUWZObGxnb05lcHA='
image_url = '파일 S3 URL'
output_file = 'OCR.json'

request_json = {
    'images': [
        {
            'format': 'png',
            'name': 'image',
            'url' : image_url
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = json.dumps(request_json).encode('UTF-8')

headers = {
  'X-OCR-SECRET': secret_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", api_url, headers=headers, data = payload)

#print(response.text)

res = json.loads(response.text)
print(res)

with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(res, outfile, indent=4, ensure_ascii=False)