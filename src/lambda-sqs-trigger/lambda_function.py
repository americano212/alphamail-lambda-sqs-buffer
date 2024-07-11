import json
import sys
import os
import boto3

package_path = os.path.join(os.path.dirname(__file__), 'packages')
if package_path not in sys.path:
    sys.path.append(package_path)
    
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
    SELECT id as email_id FROM mail WHERE is_spam IS NULL LIMIT 100
    '''
    cursor.execute(query)   
    select_all_result = cursor.fetchall()
    cnx.close()

    lst = [x[0] for x in select_all_result]

    for idx in range(0, len(lst), 10):
        result = {'email_id': lst[idx:idx+10]}
        msg_body = json.dumps(result)
        msg = send_sqs_message(os.environ['SQS_QUEUE'], msg_body)

    
    
def send_sqs_message(sqs_queue_url, msg_body):
    sqs_client = boto3.client('sqs')
    msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)
    return msg

# lambda_handler(None, None)

