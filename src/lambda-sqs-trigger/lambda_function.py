import json
import os
import boto3


def lambda_handler(event, context):
    lst = [{'email_id': 1, 'email_id': 2}]
    msg_body = json.dumps(lst)
    print("msg_body", msg_body)
    msg = send_sqs_message(os.environ['SQS_QUEUE'], msg_body)
    print("msg", msg)
    
def send_sqs_message(sqs_queue_url, msg_body):
    sqs_client = boto3.client('sqs')

    msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)