from requests_oauthlib import OAuth1
import json

with open('../aaa.txt') as json_file:
    data = json.load(json_file)

consumer_key = data['consumer_key']
consumer_key_secret = data['consumer_key_secret']
oauth_token = data['oauth_token']
oauth_token_secret = data['oauth_token_secret']
oauth_hdr = OAuth1(consumer_key, consumer_key_secret, oauth_token,
                   oauth_token_secret)
stock_endpoint = data['stock_endpoint']
option_endpoint = data['option_endpoint']

