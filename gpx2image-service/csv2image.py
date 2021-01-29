import json
import boto3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

s3 = boto3.resource('s3')


def main(event, context):

    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y%m%d%H%M%S')
    AWS_S3_BUCKET_NAME = 'gpx2image'
    AWS_S3_OUTOBJECT_NAME = 'test' + tstr +'.png'
    
    # try:
    bucket = s3.Bucket(AWS_S3_BUCKET_NAME)
    bucket.download_file('test.csv', '/tmp/test.csv')
    data = pd.read_csv('/tmp/test.csv',names=['x', 'y'])

    plt.plot(data['x'],data['y'],linewidth = 3.0, color="white")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.gca().invert_xaxis()
    plt.savefig('/tmp/' + AWS_S3_OUTOBJECT_NAME, transparent=True)

    # 上記ファイルをS3にアップロード
    bucket.upload_file('/tmp/' + AWS_S3_OUTOBJECT_NAME, AWS_S3_OUTOBJECT_NAME)
    return {
        'statusCode': 200,
        'body': '{"name": {AWS_S3_OUTOBJECT_NAME}, "code": "N00-00"}'
    }
        
    # except:
    #     return {
    #         'statusCode': 200,
    #         'body': '{"code": "E00-00", "message": "unexpected error occurs."}'
    #     }