from flask import Flask, request, render_template, abort
from auth import consumer_api_pass
from twitter_funcs import manda_dm
import base64
import hashlib
import hmac
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/twitter/webhook', methods=['POST', 'GET'])
def webhook():
    if (request.method == 'POST'):
        data = request.json
        if 'direct_message_events' in data:
            user_id = data['direct_message_events'][0]['message_create']['sender_id']
            msg_data = data['direct_message_events'][0]['message_create']['message_data']['text']

            if 'oi' in msg_data:
                manda_dm(user_id, 'Olá!')

        return 'success', 200
    elif (request.method == 'GET'):
        consumer_secret_bytes = consumer_api_pass.encode('utf-8')
        crc_token_bytes = request.args.get('crc_token').encode('utf-8')
        sha256_hash_digest = hmac.new(consumer_secret_bytes, crc_token_bytes, hashlib.sha256).digest()

        r = {
            'response_token': f'sha256={base64.b64encode(sha256_hash_digest).decode()}'
        }

        return json.dumps(r)
    else:
        abort(400)
