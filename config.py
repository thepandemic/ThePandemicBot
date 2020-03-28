import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '')

TELEGRAM_TOKEN = "1014840884:AAHRl3QtKjOjTAz9BIgPV-4XWXA95Y5s3bE"
CHAT_ID = "-1001212798809"

if not TELEGRAM_TOKEN or not CHAT_ID:
  raise Exception('TELEGRAM_TOKEN, CHAT_ID 확인필요')