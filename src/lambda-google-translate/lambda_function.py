import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
from googletrans import Translator

def google_translate(sourceWord, sourceLanguage, targetLanguage):
    translator = Translator()
    
    result = translator.translate(text=sourceWord, src=sourceLanguage, dest=targetLanguage)

    return result.text


def lambda_handler(event, context):
    sourceWord = event['queryStringParameters']['sourceWord']
    sourceLanguage = event['queryStringParameters']['sourceLanguage']
    targetLanguage='ko'

    targetWord = google_translate(sourceWord, sourceLanguage, targetLanguage)

    return {
        'statusCode': 200,
        'body': json.dumps({'targetWord': targetWord}, ensure_ascii=False),
        'headers': {'Content-Type': 'application/json'}
    }

# event = {
#   'queryStringParameters' :{
#     "sourceWord": "apple",
#     "sourceLanguage": "en"
#   }
# }

# context = {}
# print(lambda_handler(event, context))