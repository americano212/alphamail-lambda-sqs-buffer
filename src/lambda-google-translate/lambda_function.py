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
    print("event", event)
    try:
        sourceWord = event['queryStringParameters']['sourceWord']
        sourceLanguage = event['queryStringParameters']['sourceLanguage']
        targetLanguage = event['queryStringParameters']['targetLanguage']
        
        print("sourceWord", sourceWord, type(sourceWord))
        print("sourceLanguage", sourceLanguage, type(sourceLanguage))
        print("targetLanguage", targetLanguage, type(targetLanguage))
        targetWord = google_translate(sourceWord, sourceLanguage, targetLanguage)

        return {
            'statusCode': 200,
            'body': json.dumps({'targetWord': targetWord}, ensure_ascii=False)
        }
    
    except Exception as err:
        print('[ERROR] ', err)
        return {
            'statusCode': 400,
            'body': json.dumps({'ERROR': str(err)}, ensure_ascii=False)
        }

# event = {
#   'queryStringParameters' :{
#       "sourceWord": "안녕하세요. 나는 홍길동입니다.",
#       "sourceLanguage": "ko",
#       "targetLanguage": "en"
#   }
# }

# context = {}
# print(lambda_handler(event, context))