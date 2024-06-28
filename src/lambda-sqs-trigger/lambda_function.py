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

    query = '''
    SELECT id as email_id FROM mail WHERE is_spam IS NULL LIMIT 10
    '''
    cursor.execute(query)   
    select_all_result = cursor.fetchall()
    print("select_all_result", select_all_result, type(select_all_result))
    lst = [{'email_id': [1, 2]}]
    msg_body = json.dumps(lst)
    
    msg = send_sqs_message(os.environ['SQS_QUEUE'], msg_body)

    cnx.close()
    
def send_sqs_message(sqs_queue_url, msg_body):
    sqs_client = boto3.client('sqs')
    msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)

# lambda_handler(None, None)

