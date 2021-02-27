import requests
import string
import random
import base64
import time

from io import BytesIO
from requests_toolbelt import MultipartEncoder

userstr = None
rebate = None

def get_server():
    url = 'http://0.haoi23.net/svlist.html'
    resp_text = requests.get(url).text
    return resp_text.replace('===', '').replace('+++', '').split('--')[0]


def get_point(server_url):
    url = 'http://{}/GetPoint.aspx'.format(server_url)
    mp_encoder = MultipartEncoder(
        fields={
            'user': userstr,
            'r': generate_random_hex(10)
        }
    )
    headers = {'Content-Type': mp_encoder.content_type}
    resp = requests.post(url, data=mp_encoder, headers=headers)
    resp_text = resp.text
    if resp_text[0] == '#':
        raise RuntimeError('Haoi Error: {}'.format(resp_text))
    return resp_text


def send_base64_image(server_url, img):
    url = 'http://{}/UploadBase64.aspx'.format(server_url)
    mp_encoder = MultipartEncoder(
        fields={
            'userstr': userstr,
            'gameid': '6004',
            'timeout': '600',
            'rebate': rebate,
            'daiLi': 'haoi',
            'kou': '0',
            'beizhu': '',
            'ver': 'web2',
            'key': generate_random_hex(10),
            'img': img
        }
    )
    headers = {'Content-Type': mp_encoder.content_type}
    resp = requests.post(url, data=mp_encoder, headers=headers)
    resp_text = resp.text
    print("Receive tid: {}".format(resp_text))
    return resp_text


def get_answer(server_url, tid):
    count = 0
    url = 'http://{}/GetAnswer.aspx'.format(server_url)
    mp_encoder = MultipartEncoder(
        fields={
            'id': tid,
            'r': generate_random_hex(10),
        }
    )
    headers = {'Content-Type': mp_encoder.content_type}

    resp_text = requests.post(url, data=mp_encoder, headers=headers).text
    return resp_text


def solve_verification(img):
    if userstr is None or rebate is None:
        return None
    img = img.quantize(colors=128, method=2)
    buffered = BytesIO()
    img.save(buffered, format="PNG", optimize=True, quality=5)
    img_base64 = base64.b64encode(buffered.getvalue())

    server_url = get_server()
    tid = send_base64_image(server_url, img_base64)
    ans = None
    while (ans is None or ans == '') and tid[0] != '#':
        ans = get_answer(server_url, tid)
        time.sleep(2)
    if tid[0] != '#':
        points = ans.split('|')
        for i in range(len(points)):
            points[i] = points[i].split(',')
            points[i][0] = int(points[i][0])
            points[i][1] = int(points[i][1])
        return points
    return None


def generate_random_hex(num_of_digits):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(num_of_digits)])
