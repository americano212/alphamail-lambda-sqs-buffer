import json
import sys
import io
import os

package_path = os.path.join(os.path.dirname(__file__), 'packages')
if package_path not in sys.path:
    sys.path.append(package_path)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
from googletrans import Translator

def google_translate(sourceWord, sourceLanguage, targetLanguage):
    translator = Translator()
    
    result = translator.translate(text=sourceWord, src=sourceLanguage, dest=targetLanguage)

    return result.text


def lambda_handler(event, context):
    try:
        sourceWord = event['queryStringParameters']['sourceWord']
        sourceLanguage = event['queryStringParameters']['sourceLanguage']
        targetLanguage='ko'

        targetWord = google_translate(sourceWord, sourceLanguage, targetLanguage)

        return {
            'statusCode': 200,
            'body': json.dumps({'targetWord': targetWord}, ensure_ascii=False),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except Exception as err:
        print('[ERROR] ', err)
        return {
            'statusCode': 400,
            'body': json.dumps({'ERROR': str(err)}, ensure_ascii=False),
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