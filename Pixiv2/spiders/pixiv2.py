#一个json,50png
import json
import os.path
import scrapy
import datetime
import re
from ..items import Pixiv2Item
from ..get_name import get_name
class Pixiv2Spider(scrapy.Spider):
    name = "pixiv2"
    allowed_domains = ["www.pixiv.com"]
    url = "https://www.pixiv.net/ranking.php?p={}&format=json"

    directory = f'D:\\Pixiv\\{get_name()}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    def clean_file_name(self,raw_name):
        cleaned_name = re.sub(r'[\\/:"*?<>|]', '', raw_name)
        return cleaned_name
    def parse_url(self,url):
        url_list = url.split('/')
        url_list[3] = 'img-original'
        url_list.pop(4)
        url_list.pop(4)
        url_list[-1] = url_list[-1].replace("0_master1200.jpg", '{}.png')
        new_url = "/".join(url_list)
        return new_url
    def start_requests(self):
        for pn in range(1,2):
            url = self.url.format(pn)
            yield scrapy.Request(
                url=url,
                callback=self.parse_two
            )
    def parse_two(self, response):
        html = json.loads(response.text)
        for img in html['contents']:
            title = img['title']
            title = self.clean_file_name(title)
            one_url = img['url']
            print(one_url)
            num = int(img['illust_page_count'].strip())
            for i in range(0,num):
                item = Pixiv2Item()
                item['name'] = title+'_'+str(i)
                item['url'] = self.parse_url(one_url).format(i)
                item['number'] = num
                yield item