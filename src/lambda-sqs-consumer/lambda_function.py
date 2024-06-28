import json

def lambda_handler(event, context):
    print("event", event)
    records = event['Records']
    
    for record in records:
        body = record['body']
        print("body", body)
        email_id = body['email_id']
        print("email_id", email_id, type(email_id))