# 📧 Alphamail(알파메일) lambda+SQS buffer Repository
🌐 서비스 주소: https://alphamail-web.vercel.app

✈ 공군창업경진대회 출품작

## 💻 프로젝트 소개
알파메일은 필요한 메일만 읽고, 핵심 내용에만 집중해서 빠르게 메일을 작성할 수 있는
서비스를 제공합니다.

고객은 중요 메일을 놓치지 않을 수 있고, 메일을 작성하는 시간을 줄일 수 있으며,
해킹메일 같은 사이버공격으로부터 데이터를 보호할 수 있습니다.

## 🔧 주요기능
1. 스팸 필터링 AI로 받은 메일을 필터링해 주고, 사용자의 행동을 분석하여 불필요한
메일의 노출을 줄여줍니다. 사용자는 별도의 설정 없이 광고와 반복성 메일에서
벗어나, 중요한 메일을 놓치지 않고, 해킹메일에 감염될 가능성을 제거할 수
있습니다.

2. 메일 작성에 최적화된 생성형 AI를 제공합니다. 상황을 설명해 주면, 메일을 작성해
주는 기능뿐만 아니라, 특정 메일에 대해 답장할 때, 메일 내용을 바탕으로 적절한
답장을 작성해 주는 기능을 탑재하여 사용자는 손쉽게 답장을 작성해 시간을 절약할
수 있습니다.

3. Gmail, Naver 메일 등 흩어진 메일함을 모아서 하나로 만들어줍니다.

## 🧿 Lambda functions
|                                                             API                                                              |       Function       |   Note   |
|------------------------------------------------------------------------------------------------------------------------------|----------------------|----------|
| [lambda-sqs-consumer](https://github.com/americano212/alphamail-lambda-sqs-buffer/tree/main/src/lambda-sqs-consumer)         | SQS 메시지 소비자 함수 |---------|
| [lambda-sqs-trigger](https://github.com/americano212/alphamail-lambda-sqs-buffer/tree/main/src/lambda-sqs-trigger)           | SQS 메시지 생성 함수   |---------|
| [lambda-google-translate](https://github.com/americano212/alphamail-lambda-sqs-buffer/tree/main/src/lambda-google-translate) | 구글 번역기           |---------|

## 🔗 연결된 프로젝트
프론트엔드 Github: https://github.com/americano212/nextjs-alphamail-web

백엔드 Github: https://github.com/jmk307/alphamail

## 🔨 Dev Guide
### Cloud Architecture
![sqs+lambda](https://github.com/americano212/alphamail-lambda-sqs-spam-classification/assets/53344349/0173e3e0-73b5-4c70-95ea-17901edbd2cd)

### 📣 lambda 배포시 유의사항
- requirements.txt 생성해서 library 추가
```bash
pip freeze > requirements.txt
```

- lambda_function.py 상단에 package_path 지정 코드 추가 
```python
import sys
import os
package_path = os.path.join(os.path.dirname(__file__), 'packages')
if package_path not in sys.path:
    sys.path.append(package_path)
```