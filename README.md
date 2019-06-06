# python 网络爬虫之使用 Scrapy 爬取图片
### 下载图片需要用到 ImagesPipelines 这个类，首先介绍一下工作流程：
  1、首先需要在一个爬虫中，获取到图片的 url 并保存起来，也就是我们项目中MiniiamdemoSpider 类的功能
  2、项目从爬虫返回，进入到项目通道也就是 pipelines 中
  3、在通道中，在第一步中获取到图片 url 将被 scrapy 的调度器和下载器安排下载
  4、下载完成后，将返回一组列表，包括下载路径，源抓取地址和图片的校验码
  
  首先在 settings.py 中设置下载通道，下载路径以及下载参数
  ITEM_PIPELINES = {
    #  'test。pipelines.TestPipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline':1,
  }
  IMAGES_STORE ='E:\\scrapy_project\\test1\\image'

IMAGES_EXPIRES = 90

IMAGES_MIN_HEIGHT = 100

IMAGES_MIN_WIDTH = 100
其中IMAGES_STORE是设置的是图片保存的路径。IMAGES_EXPIRES是设置的项目保存的最长时间。IMAGES_MIN_HEIGHT和IMAGES_MIN_WIDTH是设置的图片尺寸大小
 
2 设置完成后，我们就开始写爬虫程序，也就是第一步获取到图片的URL。我们以http://699pic.com/people.html网站图片为例。中文名称为摄图网。里面有各种摄影图片。我们首先来看下网页结构。图片的地址都保存在
<div class=“swipeboxex”><div class=”list”><a><image>中的属性data-original


首先在item.py中定义如下几个结构体
class Test1Item(scrapy.Item):

    # define the fields for your item here like:

    # name = scrapy.Field()

    image_urls=Field()

    images=Field()

    image_path=Field()
 
根据这个网页结构，在test_spider.py文件中的代码如下。在items中保存了
class testSpider(Spider):

    name="test1" 

    allowd_domains=['699pic.com']

    start_urls=["http://699pic.com/people.html"]

    print start_urls

    def parse(self,response):

        items=Test1Item()
items['image_urls']=response.xpath('//div[@class="swipeboxEx"]/div[@class="list"]/a/img/@data-original').extract()

        return items
 
3 在第二步中获取到了图片url后，下面就要进入pipeline管道。进入pipeline.py。首先引入ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
然后只需要将Test1Pipeline继承自ImagesPipeline就可以了。里面可以不用写任意代码
class Test1Pipeline(ImagesPipeline):

    pass
ImagesPipeline中主要介绍2个函数。get_media_requests和item_completed.我们来看下代码的实现：
def get_media_requests(self, item, info):

    return [Request(x) for x in item.get(self.images_urls_field, [])]
 
从代码中可以看到get_meida)_requests是从管道中取出图片的url并调用request函数去获取这个url
Item_completed函数
def item_completed(self, results, item, info):

    if isinstance(item, dict) or self.images_result_field in item.fields:

        item[self.images_result_field] = [x for ok, x in results if ok]

    return item
当下载完了图片后，将图片的路径以及网址，校验码保存在item中
 
下面运行代码，这里贴出log中的运行日志：
2017-06-09 22:38:17 [scrapy] INFO: Scrapy 1.1.0 started (bot: test1)
  
