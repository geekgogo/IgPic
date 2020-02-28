# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from . import settings
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class IgpicPipeline(object):
    def process_item(self, item, spider):
        return item


class IgImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        # 'referer': 'https://www.douban.com/photos/photo/2370443040/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        if item:
            for image_url in item['image_urls']:
                self.default_headers['referer'] = image_url
                yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        item['image_paths'] = image_paths
        for j in range(len(item["images"])):
            os.rename(settings.IMAGES_STORE + '/' + image_paths[j],
                      settings.IMAGES_STORE + '/' + os.path.dirname(image_paths[j]) + "/" + item["images"][j] + os.path.splitext(image_paths[j])[1])

        return item


class IgVideoDownloadPipeline(FilesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        # 'referer': 'https://www.douban.com/photos/photo/2370443040/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            self.default_headers['referer'] = file_url
            yield Request(file_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        file_path = [x["path"] for ok, x in results if ok]
        if not file_path:
            raise DropItem("Item contains no videos")
        item["file_paths"] = file_path

        for j in item["file_paths"]:
            # 给视频添加后缀名
            os.rename(settings.FILES_STORE + '/' + j,
                      settings.FILES_STORE + '/' + j + ".mp4")

        return item
