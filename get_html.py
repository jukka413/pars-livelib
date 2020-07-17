import random

import requests
import time
from fake_useragent import UserAgent


class GetHTML:

    def get_html(url):
        headers = {'User-Agent': UserAgent().chrome}
        rq = requests.get(url, headers=headers)
        rq.encoding = 'utf-8'

        print('Getting HTML-code from ', url)
        time.sleep(random.randint(40, 45))

        return rq.text
