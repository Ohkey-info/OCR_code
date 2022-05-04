import cv2
import datetime
import boto3

#S3 업로드 코드
s3 = boto3.client('s3',
    aws_access_key_id = "AKIAXD4YJDWSS7UNX6VJ",
    aws_secret_access_key = "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")
bucket_name = 'capston-dgu'
#end

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
        print(file, ' saved')

video_capture.release()
cv2.destroyAllWindows()