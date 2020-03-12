# -*- coding: utf-8 -*-
import scrapy
from test123.items import DarmaItem

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.yuewz.com']
    start_urls = ['http://www.yuewz.com/list/______1_1.html']
    p=1
    e_list=[]
    e=0
    pp_list=[]
    ph_list=[]
    pp=0
    def parse(self, response):
        etem = {}
        llist=response.css("div.dhp  a.pic")
        for li in llist:
            title= li.css(" img::attr(alt)").extract_first()
            darmurl='http://www.yuewz.com'+str(li.css("::attr(href)").extract_first())
            if not darmurl=='http://www.yuewz.com/tvb/index.html':
                etem['title']=title
                etem['url']=darmurl
                self.e_list.append(etem)
            print(etem)
            etem={}
        self.p+=1
        if self.p<71:
            next_url='http://www.yuewz.com/list/______1_'+str(self.p)+'.html'
            url=response.urljoin(next_url)
            yield scrapy.Request(url=url,callback=self.parse)
        else:
            print(self.e_list[self.e]['url'])
            next_url=self.e_list[self.e]['url']
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url, callback=self.parse_in)
            #item= DarmaItem()
            #item['title']=li.css("a::text").extract_first()
            #item['href']=li.css("a::attr(href)").extract_first()
            #print(item)

    def parse_in(self, response):
        ull = response.css("div.o_cn_r_box ")

    # ul = response.css("ul.mn_list_li_movie")
        if len(ull):
            for ul in ull:
                if ul.css("div div div span h2::text").extract_first()=='迅雷下载':
                    list1 = ul.css("ul.mn_list_li_movie li")
                    tem={}
                    href_list=[]
                    for li in list1:
                        tem['title']=li.css("a::text").extract_first()
                        tem['href']=li.css("a::attr(href)").extract_first()
                        href_list.append(tem)
                    item = DarmaItem()
                    item['title'] = self.e_list[self.e]['title']
                    item['href_list'] = href_list
                    # yield item
                    print(item)
                elif ul.css("div div div span h2::text").extract_first()=='网盘':
                    list1 = ul.css("ul.mn_list_li_movie li")
                    tem = {}
                    for li in list1:
                        tem['title'] = li.css("a::text").extract_first()
                        tem['href'] =  self.e_list[self.e]['url'][:-10]+str(li.css("a::attr(href)").extract_first())

                        self.pp_list.append(tem)
                    next_url = self.pp_list[self.pp]['href']
                    url = response.urljoin(next_url)
                    yield scrapy.Request(url=url, callback=self.parse_p)
        else:
            item= DarmaItem()
            item['title']=self.e_list[self.e]['title']
            item['href_list']=[]
            # yield item
            print(item)
        self.e += 1
        if self.e<len(self.e_list):
            next_url = self.e_list[self.e]['url']

            url = response.urljoin(next_url)
            yield scrapy.Request(url=url, callback=self.parse_in)
    # item['title']=li.css("a::text").extract_first()
    def parse_p(self, response):
        self.ph_list.append({'title':self.pp_list[self.pp]['title'] ,'href':response.css("html body div.p-player div.p-vbox div.p-v table tbody tr td p a font::text").extract_first()})
        self.pp+=1
        if self.pp<len(self.pp_list):
            next_url = self.pp_list[self.pp]['href']

            url = response.urljoin(next_url)
            yield scrapy.Request(url=url, callback=self.parse_p)
        else:
            item = DarmaItem()
            item['title'] = self.e_list[self.e]['title']
            item['href_list'] = self.ph_list
            #yield item
            print(item)
            self.pp_list=[]
            self.ph_list=[]
            self.pp=0
            self.e+=1
            if self.e<len(self.e_list):
                next_url = self.e_list[self.e]['url']

                url = response.urljoin(next_url)
                yield scrapy.Request(url=url, callback=self.parse_in)
