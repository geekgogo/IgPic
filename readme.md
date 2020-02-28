# 功能
抓取instagram分享链接的图片，支持链接中包含的多张图片以及视频的抓取，前提是能科学上网

# 使用方法

1. 使用`python3`的`pip`管理包下载安装`scrapy`
2. 将你从instagram复制的链接替换掉`IgPic/IgPic/spiders/ig.py`中的`start_urls`
3. 进入项目的根目录运行`scrapy crawl downloadIgPic`
4. 视频和图片分别存放在`image`和`video`目录下

# 难点记录

1. 页面获取到后无法使用html定位到所需内容，所以使用抓取js脚本的方法，获取数据

2. 重写`ImagesPipeline`和`FilesPipeline`的`get_media_requests`与`item_completed`的方法重命名图片和视频，需要在`settings`中打开自定义的`pipeline`

3. 分享链接可能包含多张图片与视频，每种不同的情况都需要考虑，因此使用`scrapy shell 地址`访问不同的地址，取得不同的数据写入json文本中来对比不同的地方。

4. | 文件                | 用途               |
   | ------------------- | ------------------ |
   | single_pic.txt      | 数据只包含一张图片 |
   | two_pic.txt         | 数据包含两张图片   |
   | pics_and_videos.txt | 数据包含图片和视频 |
   | video.txt           | 数据只有一个视频   |

5. 利用以上json格式的文本分析