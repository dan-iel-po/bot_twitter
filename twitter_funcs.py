import requests
from requests_oauthlib import OAuth1
import oauth

def auth_consumer():
    auth = OAuth1(oauth.consumer_api_key, oauth.consumer_api_pass, oauth.access_token, oauth.access_token_secret)
    return auth

def auth_bearer():
    auth = OAuth1(oauth.bearer_token)
    return auth

def manda_dm(id_remetente, msg):
    r_dict = {'event':
                  {'type': 'message_create',
                  'message_create': {'target': {'recipient_id': id_remetente},
                  'message_data': {'text' : msg}}}}

    r = requests.post("https://api.twitter.com/1.1/direct_messages/events/new.json", json=r_dict, auth=auth_consumer())

    return r

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

#def main():

#if(__name__ == "__main__"):
    #main()