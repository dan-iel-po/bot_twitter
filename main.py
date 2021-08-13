from flask import Flask, request, render_template, abort
from oauth import consumer_api_pass
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
        print(request.json)
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
