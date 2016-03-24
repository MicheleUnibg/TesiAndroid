import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from apk.items import ApkItem
from scrapy.conf import settings
import sqlite3
import requests

class ApkSpider(CrawlSpider):
    name = "trova"
    allowed_domains = ["apk4fun.com"]
    start_urls = ["http://www.apk4fun.com/" ]
    rules=(
	Rule(LinkExtractor(allow=('games/'),restrict_xpaths=('//ul[@class="top-list"]//li//div[@class="top-icon"]//a',)),follow=True),
	Rule(LinkExtractor(deny=('apk/'),restrict_xpaths=('//ul[@class="apps"]',)),callback="parse_items",follow=True),
)
    def parse_items(self,response):

		item= ApkItem()
	        item['link']=response.url
		item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract()
	        item['dimensione']=response.xpath('//div[@class="specb"]/p[2]/text()').extract()
		link_apk=response.xpath('//div[@class="post-outer clearfix"]/p/strong/a[@class="readmore"]/@href').extract()
		lAPK=''.join(link_apk)
 		item['identificativo']=lAPK[5:len(lAPK)-1]
	        link_apk=response.xpath('//div[@class="post-outer clearfix"]/p/strong/a[@class="readmore"]/@href').extract()
		item['linkApk']="http://www.apk4fun.com/int/"+item['identificativo']+"/apk4fun/"
	        item['pubblicazione']=response.xpath('//div[@class="post-title"]/p[2]/a/text()').extract()
	        item['genere']=response.xpath('//div[@class="post-title"]/p[1]/a/text()').extract()
		conn=sqlite3.connect("database.db")
		c=conn.cursor()	
  		c.execute("CREATE TABLE IF NOT EXISTS prova2 (identificativo integer PRIMARY KEY NOT NULL, titolo text, dimensione text, genere text, pubblicazione text, link text, linkApk text,linkDownload text,scaricato boolean )")
  		
		conn.commit()
		conn.close()
		request = scrapy.Request(item['linkApk'],
                             callback=self.parse_page2)
		request.meta['item'] = item
    		return request

    def parse_page2(self,response):
	 	item = response.meta['item']
		link_pagina=''.join(response.url)
		item['ide']=link_pagina[27:len(link_pagina)-9]
		iden=int(item['ide'])
    		titolo=''.join(item['title'])
	        dim=''.join(item['dimensione'])
		gen=''.join(item['genere'])
		pubb=''.join(item['pubblicazione'])
		link="".join(item['link'])
 	
		#print iden
    		item["linkD"]=response.xpath('//p//strong//a[@class="readmore"][1]/@href').extract()
		linkdown="".join(item['linkD'])

		#estraggo il vero link del download
		inizio="setTimeout(\"window.location.href='"
		fine="';\", 2500);</script>"
		r=requests.get(linkdown,stream=True)
		ni=r.text.find(inizio)+len(inizio)
		nf=r.text.find(fine)
		download=r.text[ni:nf]

		link_apk=response.xpath('//div[@class="post-outer clearfix"]/p/strong/a[@class="readmore"]/@href').extract()
		lAPK=''.join(link_apk)
		conn=sqlite3.connect("database.db")
		c=conn.cursor()	
		c.execute("INSERT INTO prova2 (identificativo,titolo,dimensione,genere,link,pubblicazione,linkApk,linkDownload,scaricato) VALUES(?,?,?,?,?,?,?,?,'false');",(iden,titolo,dim,gen,link,pubb,lAPK,download))
		#c.execute("UPDATE prova2 set linkDownload=? WHERE identificativo=?",(download,iden))
		conn.commit()
		conn.close()
    		yield item

		
		    
	           
