import os
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv('TT_BEARER_TOKEN')
consumer_api_key = os.getenv('TT_CONSUMER_API_KEY')
consumer_api_pass = os.getenv('TT_CONSUMER_API_PASS')
access_token = os.getenv('TT_ACCESS_TOKEN')
access_token_secret = os.getenv('TT_ACCESS_TOKEN_SECRET')