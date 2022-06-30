import cv2
import datetime
import boto3
import requests
import uuid
import time
import json


#S3 업로드 코드
s3 = boto3.client('s3',
    aws_access_key_id = "aws_access_key_id",
    aws_secret_access_key = "aws_secret_access_key")
bucket_name = 'capston-dgu'
#end

#CLOVA OCR
api_url = 'https://1mte94hdpr.apigw.ntruss.com/custom/v1/15641/df7e3d874c4ebcd0839255e7bb5ecec3d3dc754994d59c437e615e4934d6fdcd/general'
secret_key = 'secret_key='
#end

output_file = 'OCR.json'
video_capture = cv2.VideoCapture(0)

while (True):

    grabbed, frame = video_capture.read()
    cv2.imshow('Original Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.jpg'
        cv2.imwrite(file, frame)
        s3.upload_file(file, bucket_name, file)
        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': file
                }   
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
        ('file', open(file,'rb'))
        ]
        headers = {
            'X-OCR-SECRET': secret_key
        }

        response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

        #print(response.text)

        res = json.loads(response.text)
        print(res)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(res, outfile, indent=4, ensure_ascii=False)
        
        break

video_capture.release()
cv2.destroyAllWindows()



