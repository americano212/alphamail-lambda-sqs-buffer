import json
import os
import boto3
from mysql.connector import (connection)

def lambda_handler(event, context):
    try:
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
            recordBody = json.loads(record['body'])[0]

            email_id_list = recordBody['email_id']

            for email_id in email_id_list:
                content = get_email_content(email_id, cursor)

                payload = spam_classification(content)
                statusCode = payload['statusCode']
                body = payload['body']

                if(statusCode == 200):
                    isSpam = True if body != 1 else False
                    save_is_spam(email_id, isSpam, cursor, cnx)
                else:
                    errorMessage = body
                    save_error_is_spam(email_id, errorMessage, cursor, cnx)

        cnx.close()
    except Exception as e:
        print('Error', e)

def get_email_content(email_id: int, cursor)->str:
    query = '''
    SELECT content FROM alphamail_dev.mail WHERE id={}
    '''.format(email_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result[0][0]

def spam_classification(content)->dict:
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='spam-classification',
        InvocationType='RequestResponse',
        Payload=json.dumps({"body-json": {"data": content}})
    )
    
    payload = json.loads(response['Payload'].read().decode('utf8').replace("'", '"'))
    return payload

def save_is_spam(email_id: int, is_spam: bool, cursor, cnx):
    query='''
    UPDATE mail SET is_spam={0} WHERE id={1}
    '''.format(1 if is_spam else 0, email_id)
    cursor.execute(query)
    cnx.commit()
    print("email_id", email_id)
    print(cursor.rowcount, "record(s) affected")
    

def save_error_is_spam(email_id: int, error_message: str, cursor, cnx):
    query='''
    UPDATE mail SET is_spam={0} WHERE id={1}
    '''.format(-1, email_id)
    cursor.execute(query)
    cnx.commit()
    print("email_id", email_id)
    print("error_message", error_message)

# event = {'Records': [{'messageId': 'b5e3a71c-2d6c-4cb1-b63f-a40140e79ecb', 'receiptHandle': 'AQEBvSo2nlu1BtFaHF4tJHPKnnsZxr3P+8rfQ3Ol+Im//gZsB8Lx/NWhPBfgw8h1lZbLuC5Gbb7xQecplAIaMN+tL2nxvr/67hq0+rutAvpq9Z6jKUC3eX7LYLoFPERhAx9bzTOnxTnU2EoQZ7fKH4LERAiVISB9eCMQcVn6we43cR1xU6uKVy+KfurSoH8Jg+Q7NCrF4YWAsePy6iB+SGd7Ck1CTfpGOVJRZ7qOsVsLe6vIGcHCgANeNeT6uoGO1TroZR0XJZ95N7ntQ/IfIsR1KpB35MOyeo+JEpMed2FtPpjP165QfImmbzcCCsTXEGQ01YHDCeXYlPUVfrw/h+X7XtYDDrdk9t0CzWlzc+aENCna2PSYAtNe86HdSFZX07XtG1gHz8mWPQM1Sef5k4sxt/+PHLfCsPTvAMp7M62gFtw=', 'body': '[{"email_id": [1, 2]}]', 'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-667e5c03-53329ab12355f3d24289a171;Parent=4592baba5fa057e6;Sampled=0;Lineage=c6c7d02b:0', 'SentTimestamp': '1719557125833', 'SenderId': 'AROA47CRWGZ7UE5PZBWTJ:lambda-sqs-trigger', 'ApproximateFirstReceiveTimestamp': '1719557125835'}, 'messageAttributes': {}, 'md5OfBody': '7826165d70deae7e440711f70a2723d7', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-northeast-2:891377038975:sqs-alphamail-spam-classification', 'awsRegion': 'ap-northeast-2'}]}
# lambda_handler(event, "context")