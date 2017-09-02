import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import base64
from config import config
import json
import copy
import io
import time
import cv2


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
    if 'error' in res['responses'][0]:
        print(res)
        assert False

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
        x_conditions = 'x' in lt and 'x' in rb
        y_conditions = 'y' in rb and 'y' in rb
        if not(x_conditions and y_conditions): continue

        lt_point = lt['x'], lt['y']
        rb_point = rb['x'], rb['y']
        draw_img.rectangle((lt_point, rb_point), outline=(150, 0, 0), fill=(150, 0, 0))

    c_img.save('./assets/%s.jpg' % (time.time()))
    c_img.show()


def preprocessing(img):
    pil_img = Image.open(io.BytesIO(img))
    print(len(pil_img.tobytes()))
    img_np = np.asarray(pil_img)
    gray_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    kernel = np.ones([5, 5], np.uint8)
    dilate = cv2.dilate(gray_img, kernel, iterations=1)

    sub = 255 - (dilate - gray_img)

    return {'dilate': dilate, 'sub': sub}


def main():
    img_path = './assets/1.jpg'

    img = None
    with open(img_path, 'rb') as f:
        img = f.read()

    print(len(img))
    img_dict = preprocessing(img)
    buffer = io.BytesIO()
    Image.fromarray(img_dict['sub']).save(buffer, 'jpeg')
    request_img = buffer.getvalue()
    print(len(request_img))

    # res = request_api(request_img)
    # detect_list = response_parser(res)
    # draw(img, detect_list)


if __name__ == '__main__':
    main()
