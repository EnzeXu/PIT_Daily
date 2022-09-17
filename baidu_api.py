import requests
import random
import json
from hashlib import md5

from baidu_account import app_id, app_key

# # Set your own appid/appkey.
# appid = 'INPUT_YOUR_APPID'
# appkey = 'INPUT_YOUR_APPKEY'

# # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
# from_lang = 'en'
# to_lang = 'zh'
#
# endpoint = 'http://api.fanyi.baidu.com'
# path = '/api/trans/vip/translate'
# url = endpoint + path

# query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

# salt = random.randint(32768, 65536)
# sign = make_md5(app_id + query + str(salt) + app_key)
#
# # Build request
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# payload = {'appid': app_id, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
#
# # Send request
# r = requests.post(url, params=payload, headers=headers)
# result = r.json()
#
# # Show response
# print(json.dumps(result, indent=4, ensure_ascii=False))

from_lang = 'en'
to_lang = 'zh'
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


def baidu_translate(sentence):
    salt = random.randint(32768, 65536)
    sign = make_md5(app_id + sentence + str(salt) + app_key)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': app_id, 'q': sentence, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    return list(result["trans_result"])


if __name__ == "__main__":
    string = "Amidst the uncertainty and multiplicity of narratives, in such a moment and its interpretations, something true about the world can surely be discovered."
    print(baidu_translate('Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'))