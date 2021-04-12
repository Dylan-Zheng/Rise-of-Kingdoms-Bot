import requests
import string
import random
import base64
import time
import json

from io import BytesIO
from requests_toolbelt import MultipartEncoder

'''
    <form method="post" action="http://2captcha.com/in.php">
    <input type="hidden" name="method" value="base64">
    <input type="hidden" name="coordinatescaptcha" value="1">
    Your key:
    <input type="text" name="key" value="YOUR_APIKEY">
    ClickCaptcha file body in base64 format:
    <textarea name="body">BASE64_CLICKCAPTCHA_FILE</textarea>
    </form>
'''

key = None


def send_base64_image(img):
    if key is None:
        return None
    url = 'http://2captcha.com/in.php'
    mp_encoder = MultipartEncoder(
        fields={
            'method': 'base64',
            'coordinatescaptcha': '1',
            'key': key,
            'body': img
        }
    )
    headers = {'Content-Type': mp_encoder.content_type}
    resp = requests.post(url, data=mp_encoder, headers=headers)
    resp_text_arr = resp.text.split('|')
    if resp_text_arr[0] == 'OK':
        print("Receive tid: {}".format(resp_text_arr[1]))
        return resp_text_arr[1]
    else:
        raise RuntimeError('2Captcha Error: {}'.format(resp.text))


def get_answer(tid):
    if key is None:
        return None
    url = 'http://2captcha.com/res.php?key={}&action=get&id={}&json=1'.format(key, tid)
    resp_text = requests.get(url).text
    return resp_text


def refund(tid):
    url = "http://2captcha.com/res.php?key={}&action=reportbad&id={}".format(key, tid)
    resp_text = requests.get(url).text


def solve_verification(img):
    if key is None:
        return None
    img = img.quantize(colors=64, method=2)
    buffered = BytesIO()
    img.save(buffered, format="PNG", optimize=True, quality=5)
    img_base64 = base64.b64encode(buffered.getvalue())

    tid = send_base64_image(img_base64)
    time.sleep(5)

    ans = None
    while ans is None or ans['status'] != 1:
        ans = json.loads(get_answer(tid))
        if ans['request'] == 'CAPCHA_NOT_READY':
            time.sleep(5)
        elif ans['status'] == 0:
            raise RuntimeError('2Captcha Error: {}'.format(ans['request']))

    points = []
    try:
        for p in ans['request']:
            points.append([int(p['x']), int(p['y'])])
    except:
        refund(tid)

    return points
