import requests
import sys
from requests_oauthlib import OAuth1
from auth import bearer_token, consumer_api_key, consumer_api_pass, access_token, access_token_secret
import os
import base64
import hashlib
import hmac
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
auth_consumer = OAuth1(consumer_api_key, consumer_api_pass, access_token, access_token_secret)
auth_bearer = f'Bearer {bearer_token}'

class Twitter():
    #os endpoints usados pelo bot
    __upload_endpoint = 'https://upload.twitter.com/1.1/media/upload.json'
    __dm_endpoint = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
    __auth_test_endpoint = 'https://api.twitter.com/1.1/account/verify_credentials.json'

    #o id de quem vai receber a dm
    def __init__(self, reciever_id = None):
        self.__reciever_id = reciever_id

    def upload_img(self, media):

        #Declara o caminho da img e busca o tamanho dela em bytes
        file = os.path.join(THIS_FOLDER, f'temp/{media}')
        total_bytes = os.path.getsize(file)

        #inicia o processo de upload;
        # a função retorna o media_id fornecido pelo twitter
        media_id = self.upload_init(total_bytes)

        #esta função faz o upload em chunks de 5mb
        self.upload_append(file, media_id, total_bytes)

        #fecha o processo, agr o media_id pode ser utilizado
        # para mandar dms ou postar tweets
        self.upload_finalize(media_id)

        return media_id

    def upload_init(self, total_bytes):

        #Faz o request com o comando INIT, o media_category é para dms
        r_init = {'command': 'INIT',
                       'total_bytes': total_bytes,
                       'media_type': 'image/png',
                       'media_category': 'dm_image'}

        r = requests.post(self.__upload_endpoint, params=r_init, auth=auth_consumer)

        #Esse print é para debug
        print(r.json())

        #Se não houver media_id no retorno ocorreu algo de errado,
        #presumidamente foi uma tentativa com um arquivo corrompido
        #ou que não seja uma img
        if 'media_id_string' not in r.json():
            manda_dm(self.__reciever_id, 'Opa patrão, catei um link zikado, '
                                         'faça seu pedido novamente nmrlzinha')

        self.check_request(r)

        return r.json()['media_id_string']

    def upload_append(self, file, media_id, total_bytes):

        #declara bytes_sent e segment_id e abre a img em modo 'read binary
        #segment_id = quantos chunks de 5mb foram uploaded
        segment_id = 0
        bytes_sent = 0

        f = open(file, 'rb')

        #Repete este loop enquanto não enviar o arquivo inteiro
        while bytes_sent < total_bytes:
            #aparemente 4*1024*1024 bytes dá 5mb... vivendo e aprendendo, vivendo e aprendendo
            chunk = f.read(4*1024*1024)

            #faz o request com o commando 'APPEND'
            r_append = {'command': 'APPEND',
                             'media_id': media_id,
                             'segment_index': segment_id}

            files = {'media': chunk}

            r = requests.post(self.__upload_endpoint, params=r_append, files=files, auth=auth_consumer)

            #checa se a request deu certo
            self.check_request(r)

            #incrementa o segment_id e guarda quantos byte já mandou
            segment_id = segment_id + 1
            bytes_sent = f.tell()

        #fecha o arquivo ;)
        f.close()

    def upload_finalize(self, media_id):

        #aqui vc basicamente apenas checa com o twitter pra ver se deu tudo certo
        r_finalize = {'command': 'FINALIZE', 'media_id': media_id, }

        r = requests.post(self.__upload_endpoint, params=r_finalize, auth=auth_consumer)

        self.check_request(r)

    def check_request(self, r):
        if r.status_code < 200 or r.status_code > 299:
            print(r.status_code)
            print(r.text)
            sys.exit(0)

    def manda_dm(self, msg=None, media=None):

        media_id = ''
        r_dm = {}

        #se tiver houver media o upload é feito e
        #a estrutura do pedido é feita corretamente
        if (media != None):
            media_id = self.upload_img(media)

            r_dm = {'event':
                        {'type': 'message_create',
                         'message_create': {'target': {'recipient_id': self.__reciever_id},
                                            'message_data': {
                                            'text': msg,
                                            'attachment': {'type': 'media', 'media': {'id': media_id}}}}}}
            print('acabei de fazer o trem')
        else:
            r_dm = {'event':
                        {'type': 'message_create',
                         'message_create': {'target': {'recipient_id': self.__reciever_id},
                                            'message_data': {
                                            'text': msg, }}}}
            print(' o carai')

        print('to enciminha do request de dm')
        r = requests.post(self.__dm_endpoint, json=r_dm, auth=auth_consumer)

    def crc_challenge(self, crc_token):
        consumer_secret_bytes = consumer_api_pass.encode('utf-8')
        crc_token_bytes = crc_token.encode('utf-8')
        sha256_hash_digest = hmac.new(consumer_secret_bytes, crc_token_bytes, hashlib.sha256).digest()

        r = {
            'response_token': f'sha256={base64.b64encode(sha256_hash_digest).decode()}'
        }

        return json.dumps(r)

#area de testes

# def main():
    # url = 'http://127.0.0.1:5000/twitter/webhook'
    # r_dict = {'crc_token' : 'foo'}
    # r_dict = {'for_user_id': '734896788130402304',
    #           'direct_message_events': [{'type': 'message_create', 'id': '1426293441634480132', 'created_timestamp': '1628889830393',
    #                                     'message_create': {'target': {'recipient_id': '734896788130402304'}, 'sender_id': '1397372028638961667',
    #                                                        'message_data': {'text': 'cachorro'}}}]}
    #9isLi1Q4yYnoKU0btjv6F56U9zp0FT97QMAeB5JdVdI=
    # r = requests.get(url, params=r_dict)
    #
    # print(r.text)

    # manda_dm('1397372028638961667', 'bundao', 'dog.png')

    # upload_imagem('dog.png')

# if(__name__ == "__main__"):
#     main()