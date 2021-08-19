import requests
import urllib.parse
import sys
from requests_oauthlib import OAuth1
import auth
import os

# url = 'https://animalsender.pythonanywhere.com/twitter/webhook'

def auth_consumer():
    authentication = OAuth1(auth.consumer_api_key, auth.consumer_api_pass, auth.access_token, auth.access_token_secret)
    return authentication

def auth_bearer():
    auth = f'Bearer {auth.bearer_token}'
    return auth

def upload_imagem(media):
    upload_url = 'https://upload.twitter.com/1.1/media/upload.json'

    file = f'temp/{media}'
    bytes = os.path.getsize(file)

    r_dict_init = {'command': 'INIT',
              'total_bytes': bytes,
              'media_type': 'image/png',
              'media_category': 'dm_image'}

    r = requests.post(upload_url, params=r_dict_init, auth=auth_consumer())

    media_id = r.json()['media_id_string']

    upload_append(file, media_id, bytes, upload_url)

    r_dict_finalize = {'command': 'FINALIZE', 'media_id': media_id,}

    r = requests.post(upload_url, params=r_dict_finalize, auth=auth_consumer())

    return media_id

def upload_append(file, media_id, total_bytes, upload_url):

    segment_id = 0
    bytes_sent = 0

    f = open(file, 'rb')

    while bytes_sent < total_bytes:
        chunk = f.read(4*1024*1024)

        r_dict_append = {'command': 'APPEND',
                         'media_id': media_id,
                         'segment_index': 0}

        files = {'media': chunk}

        r = requests.post(upload_url, params=r_dict_append, files=files, auth=auth_consumer())

        if r.status_code < 200 or r.status_code > 299:
            print(r.status_code)
            print(r.text)
            sys.exit(0)

        segment_id = segment_id + 1
        bytes_sent = f.tell()

    f.close()

def manda_dm(id_destinatario, msg=None, media=None):

    media_id = ''

    if (media != None):
        media_id = upload_imagem(media)

    r_dict = {'event':
                  {'type': 'message_create',
                  'message_create': {'target': {'recipient_id': id_destinatario},
                  'message_data': {
                      'text' : msg, 'attachment': {'type': 'media', 'media': {'id': media_id}}}}}}

    r = requests.post("https://api.twitter.com/1.1/direct_messages/events/new.json", json=r_dict, auth=auth_consumer())

def recupera_tweet(id):
    r_dict = {'ids': id, 'expansions': 'author_id'}

    r = requests.get('https://api.twitter.com/2/tweets', params=r_dict, auth=auth_consumer())

    return r

def tweet(status):
    r_dict = {'status': status}

    r = requests.post("https://api.twitter.com/1.1/statuses/update.json", params=r_dict, auth=auth_consumer())

    return r

def testa_auth():
    r = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    r = requests.get(r, auth=auth_consumer())

    return r

# def main():
    # url = 'http://127.0.0.1:5000/twitter/webhook'
    # r_dict = {'for_user_id': '734896788130402304',
    #           'direct_message_events': [{'type': 'message_create', 'id': '1426293441634480132', 'created_timestamp': '1628889830393',
    #                                     'message_create': {'target': {'recipient_id': '734896788130402304'}, 'sender_id': '1397372028638961667',
    #                                                        'message_data': {'text': 'dog'}}}]}
    #
    # r = requests.post(url, json=r_dict)

    # manda_dm('1397372028638961667', 'bundao', 'dog.png')

    # upload_imagem('dog.png')
#
# if(__name__ == "__main__"):
#     main()