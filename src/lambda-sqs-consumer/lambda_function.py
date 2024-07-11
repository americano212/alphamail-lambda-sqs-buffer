import json
import sys
import os
import boto3

package_path = os.path.join(os.path.dirname(__file__), 'packages')
if package_path not in sys.path:
    sys.path.append(package_path)

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
        # print("records", records, type(records))
        for record in records:
            print("record",record)
            recordBody = json.loads(record['body'])
            print("recordBody",recordBody)
            email_id_list = recordBody['email_id']

            for email_id in email_id_list:
                content = get_email_content(email_id, cursor)
                translate(content)
                payload = spam_classification(content)
                statusCode = payload['statusCode']
                body = payload['body']

                if(statusCode == 200):
                    isSpam = body
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

def translate(content):
    print("translate_content", content, type(content))
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(    
        FunctionName='lambda-google-translate',
        InvocationType='RequestResponse',
        Payload=json.dumps({"queryStringParameters": {"sourceWord": content, "sourceLanguage": "ko", "targetLanguage": "en"}})
    )
    print("payload!", response['Payload'])
    print("read!", response['Payload'].read())
    print("decode! unicode-escape", response['Payload'].read().decode('unicode-escape'))
    print("decode! ascii", response['Payload'].read().decode('ascii'))
    print("decode! utf-8", response['Payload'].read().decode('utf-8'))
    print("replace!", response['Payload'].read().decode('utf-8').replace("'", '"'))
    payload = json.loads(response['Payload'].read().decode('utf-8').replace("'", '"'))
    print("translate_payload-----------", payload)

def save_is_spam(email_id: int, is_spam: int, cursor, cnx):
    query='''
    UPDATE mail SET is_spam={0} WHERE id={1}
    '''.format(is_spam, email_id)
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

event = {'Records': [{'body': '{"email_id": [1, 2, 3]}'}]}
lambda_handler(event, "context")