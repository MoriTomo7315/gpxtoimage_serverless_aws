import json
import boto3
import csv
import gpxpy

s3 = boto3.client('s3')


def main(event, context):

    AWS_S3_BUCKET_NAME = 'gpx2image'
    AWS_S3_INOBJECT_NAME = event['Records'][0]['s3']['object']['key']
    AWS_S3_OUTOBJECT_NAME = 'test.gpx'
    
    # try:
    body = s3.get_object(Bucket=AWS_S3_BUCKET_NAME,Key=AWS_S3_INOBJECT_NAME)['Body'].read()
    gpx  = gpxpy.parse(body.decode('utf-8'))

    data  = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude])

    file = open('/tmp/test.csv', 'w')
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)
    file.close()
    
    # 上記ファイルをS3にアップロード
    s3.upload_file('/tmp/test.csv', AWS_S3_BUCKET_NAME, 'test.csv')
    return {
        'statusCode': 200,
        'body': '{"message": "success", "code": "N00-00"}'
    }

    # except:
    #     return {
    #         'statusCode': 200,
    #         'body': '{"code": "E00-00", "message": "unexpected error occurs."}'
    #     }