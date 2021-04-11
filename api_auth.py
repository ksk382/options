import sys, os, base64, datetime, hashlib, hmac
import requests # pip install requests
from cred_file import secret_key, access_key, host

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).hexdigest()

def getSignatureKey(key, dateStamp):
    kDate = sign(key, dateStamp)
    kDate = bytes(kDate, 'ascii')
    return bytes(sign(kDate, 'iex_request'), 'ascii')

def get_auth_headers():

    # ************* REQUEST VALUES *************
    method = 'GET'
    sec_key = bytes(secret_key, 'ascii')

    canonical_querystring = 'token=' + access_key
    canonical_uri = '/v1/stock/aapl/company'
    #endpoint = "https://" + host + canonical_uri

    if access_key is None or sec_key is None:
        print('No access key is available.')
        sys.exit()

    t = datetime.datetime.utcnow()
    iexdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    canonical_headers = 'host:' + host + '\n' + 'x-iex-date:' + iexdate + '\n'
    signed_headers = 'host;x-iex-date'
    payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    algorithm = 'IEX-HMAC-SHA256'
    credential_scope = datestamp + '/' + 'iex_request'
    string_to_sign = algorithm + '\n' +  iexdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    signing_key = getSignatureKey(sec_key, datestamp)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {'x-iex-date':iexdate, 'Authorization': authorization_header}

    return headers


if __name__ == '__main__':

    # ************* SEND THE REQUEST *************
    host = 'cloud.iexapis.com'
    canonical_uri = '/v1/stock/msft/stats'
    endpoint = "https://" + host + canonical_uri
    #access_key = os.environ.get('IEX_PUBLIC_KEY')
    canonical_querystring = 'token=' + access_key

    request_url = endpoint + '?' + canonical_querystring

    headers = get_auth_headers()

    print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
    print('Request URL = ' + request_url)
    print ('Headers: \n', headers)
    r = requests.get(request_url, headers=headers)

    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    print(r.text)