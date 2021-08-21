from flask import Flask, request, render_template, abort
from twitter import Twitter
from imgur_funcs import get_imglink, dog, cat
import os
import requests

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

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
            msg_data = data['direct_message_events'][0]['message_create']['message_data']['text'].lower()

            twitter = Twitter(user_id)

            if 'oi' in msg_data:
                twitter.manda_dm('Olá!')

            if 'cachorro' in msg_data:
                dog_link = get_imglink(dog)

                img = requests.get(dog_link)

                with open(os.path.join(THIS_FOLDER, 'temp/dog.png'), 'wb') as f:
                    f.write(img.content)

                twitter.manda_dm(media='dog.png')

            if 'gato' in msg_data:
                cat_link = get_imglink(cat)

                img = requests.get(cat_link)

                with open(os.path.join(THIS_FOLDER, 'temp/cat.png'), 'wb') as f:
                    f.write(img.content)

                twitter.manda_dm(media='cat.png')

        return 'success', 200
    elif (request.method == 'GET'):
        crc_token = request.args.get('crc_token')

        twitter = Twitter()

        return twitter.crc_challenge(crc_token)
    else:
        abort(400)

# app.run(debug=True)