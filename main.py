import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import base64
from config import config
import json
import copy
import io
import time


def request_api(img):
    content = base64.b64encode(img).decode('utf8')
    url = '%s?key=%s' % (config['api']['url'], config['api']['key'])
    print(url)
    res = json.dumps({
        'requests': [{
            'image': {
                'content': content
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': 10
            }]
        }]
    })
    res = requests.post(url, res)
    return res.json()


def response_parser(res):
    text_annotations = res['responses'][0]['textAnnotations']

    detect_list = []
    for text in text_annotations:
        if 'locale' in text: continue
        detect_list.append([text['description'], text['boundingPoly']['vertices']])

        print(text['description'], text['boundingPoly']['vertices'])

    return detect_list


def draw(img, detect_list):
    c_img = Image.open(io.BytesIO(img))
    draw_img = ImageDraw.Draw(c_img)
    for detect in detect_list:
        lt = detect[1][0]
        rb = detect[1][2]
        lt_point = lt['x'], lt['y']
        rb_point = rb['x'], rb['y']
        draw_img.rectangle((lt_point, rb_point), outline=(150, 0, 0), fill=(150, 0, 0))

    c_img.save('./assets/%s.jpg' % (time.time()))
    c_img.show()


def main():
    img_path = './assets/1.jpg'

    img = None
    with open(img_path, 'rb') as f:
        img = f.read()

    res = request_api(img)
    detect_list = response_parser(res)
    draw(img, detect_list)


if __name__ == '__main__':
    main()
