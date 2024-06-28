import json

def lambda_handler(event, context):
    print("event", event)
    records = event['Records']
    
    for record in records:
        body = record['body']
        print("body", body)