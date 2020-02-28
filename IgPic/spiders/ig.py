import scrapy
from IgPic.items import IgpicItem
from scrapy.http import Request
from scrapy import Selector
import json
from .. import settings

class DownloadInstagramPic(scrapy.Spider):
    name = "downloadIgPic"

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.instagram.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ['instagram.com', 'cdninstagram.com']
        # 爬取页面的url
        self.start_urls = [
            "https://www.instagram.com/p/B9CLQU9JTTi/?utm_source=ig_web_button_share_sheet"]

        # call the father base function

        # super(download_douban, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, headers=self.default_headers, callback=self.parse)

    def parse(self, response):
        # 根据访问start_urls得到的response，利用xpath定位到js脚本，转化成json格式后获取图片与视频的地址
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]
        ret = json.loads(jscleaned)

        # 链接中可能包含一张图片或者多张图片与视频，从此处开始判断
        media_info = ret["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]

        item = IgpicItem()
        pic_list = list()
        pic_id = list()
        video_list = list()
        # 链接中只有一张图片或一个视频
        if media_info["media_preview"]:
            if media_info["is_video"]:
                video_url = media_info["video_url"]
                video_list.append(video_url)
            else:
                pic_url = media_info["display_url"]
                pic_id.append(media_info["id"])
                pic_list.append(pic_url)


        # 链接中包含多张图片或视频
        else:
            pic_url = media_info["edge_sidecar_to_children"]["edges"]
            if pic_url:
                for i in pic_url:
                    # 判断是否为视频
                    if i.get("node").get("is_video"):
                        video_url = i.get("node").get("video_url")
                        video_list.append(video_url)
                    else:
                        pic_list.append(i.get("node").get("display_url"))
                        pic_id.append(i.get("node").get("id"))

        # item项目字段必须是list类型
        item["image_urls"] = pic_list
        item["images"] = pic_id
        item["file_urls"] = video_list
        yield item

