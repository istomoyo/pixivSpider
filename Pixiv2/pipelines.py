# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#导入scrapy中的图片管道
from scrapy.pipelines.images import ImagesPipeline
import scrapy
class Pixiv2Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #直接交给调度器
        yield scrapy.Request(
            url=item['url'],
            meta={'title':item['name']},
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        title = request.meta['title']
        filename = title+".png"
        return filename
