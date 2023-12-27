# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


class Translation:
    def __init__(self, appid, appkey):
        # Set your own appid/appkey.
        print(f'appid: {appid}\nappkey: ****{appkey[:5]}')
        self.appid = appid
        self.appkey = appkey
        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`

    def query_jp_zh(self, text):
        from_lang = 'jp'
        to_lang = 'zh'

        query = text

        # Generate salt and sign

        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        # Show response
        # return json.dumps(result, indent=4, ensure_ascii=False)

        return result

    def query_zh_jp(self, text):
        from_lang = 'zh'
        to_lang = 'jp'

        query = text

        # Generate salt and sign

        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        # Show response
        return result

    def query_en_zh(self, text):
        from_lang = 'en'
        to_lang = 'zh'

        query = text

        # Generate salt and sign

        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        # Show response
        return result

    def query_zh_en(self, text):
        from_lang = 'zh'
        to_lang = 'en'

        query = text

        # Generate salt and sign

        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        # Show response
        return result


if __name__ == '__main__':
    t = Translation()

    print(t.query_jp_zh('駅弁'))
    print(t.query_zh_jp('吃饭'))
