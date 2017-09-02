import requests
from PIL import Image
import numpy as np
import base64
from config import config
import json


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

    
def main():
    img_path = './assets/1.jpg'

    img = None
    with open(img_path, 'rb') as f:
        img = f.read()

    res = request_api(img)
    detect_list = response_parser(res)


if __name__ == '__main__':
    main()
