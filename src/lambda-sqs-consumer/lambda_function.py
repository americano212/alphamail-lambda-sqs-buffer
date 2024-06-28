import json
import os
import boto3
from mysql.connector import (connection)

def lambda_handler(event, context):
    config = {
        'user': os.environ['user'],
        'password': os.environ['password'],
        'host':  os.environ['host'],
        'database':  os.environ['database'],
    }
    cnx = connection.MySQLConnection(**config)
    cursor = cnx.cursor()

    records = event['Records']
    
    for record in records:
        body = json.loads(record['body'])[0]
        
        print("body", body, type(body))
        email_id_list = body['email_id']

        for email_id in email_id_list:
            print("email_id", email_id, type(email_id))

            content = get_email_content(email_id, cursor)
            print("content", content)
            isSpam = spam_classification(content)
            print("isSpam", isSpam)

    cnx.close()

    


def get_email_content(email_id: int, cursor)->str:
    query = '''
    SELECT content FROM alphamail_dev.mail WHERE id={}
    '''.format(email_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result[0][0]

def spam_classification(content)->bool:
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='spam-classification',
        InvocationType='RequestResponse',
        Payload=json.dumps({"body-json": {"data": content}})
    )
    payload = response['Payload'].read()
    print("payload", payload, type(payload))
    return True

# event = {'Records': [{'messageId': 'b5e3a71c-2d6c-4cb1-b63f-a40140e79ecb', 'receiptHandle': 'AQEBvSo2nlu1BtFaHF4tJHPKnnsZxr3P+8rfQ3Ol+Im//gZsB8Lx/NWhPBfgw8h1lZbLuC5Gbb7xQecplAIaMN+tL2nxvr/67hq0+rutAvpq9Z6jKUC3eX7LYLoFPERhAx9bzTOnxTnU2EoQZ7fKH4LERAiVISB9eCMQcVn6we43cR1xU6uKVy+KfurSoH8Jg+Q7NCrF4YWAsePy6iB+SGd7Ck1CTfpGOVJRZ7qOsVsLe6vIGcHCgANeNeT6uoGO1TroZR0XJZ95N7ntQ/IfIsR1KpB35MOyeo+JEpMed2FtPpjP165QfImmbzcCCsTXEGQ01YHDCeXYlPUVfrw/h+X7XtYDDrdk9t0CzWlzc+aENCna2PSYAtNe86HdSFZX07XtG1gHz8mWPQM1Sef5k4sxt/+PHLfCsPTvAMp7M62gFtw=', 'body': '[{"email_id": [1, 2]}]', 'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-667e5c03-53329ab12355f3d24289a171;Parent=4592baba5fa057e6;Sampled=0;Lineage=c6c7d02b:0', 'SentTimestamp': '1719557125833', 'SenderId': 'AROA47CRWGZ7UE5PZBWTJ:lambda-sqs-trigger', 'ApproximateFirstReceiveTimestamp': '1719557125835'}, 'messageAttributes': {}, 'md5OfBody': '7826165d70deae7e440711f70a2723d7', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-northeast-2:891377038975:sqs-alphamail-spam-classification', 'awsRegion': 'ap-northeast-2'}]}
# lambda_handler(event, "context")