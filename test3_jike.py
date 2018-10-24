#coding=utf8
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import re
import os

#设置抓取页数
PAGE_NUM = 21

#获取当前文件的绝对路径
BASE_DIR = os.path.dirname(__file__)

#抓取函数
#该抓取方法为ID遍历抓取
def get_page():
	#爬虫的原始链接BaseUrl
	url_base = 'http://www.jikexueyuan.com/course/?pageNum='

	#设置User-Agent
	headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
	}

	#当前页码
	page_num = 1

	#循环爬取页面
	while page_num <= PAGE_NUM:
		#此时的抓取链接
		url = url_base+str(page_num)
		print("将要抓取页面的的链接："+url)

		#requests抓取链接页面
		try:
			page = requests.get(url,headers=headers)
		except:
			print("重新抓取："+url)
			continue

		#BeautifulSoup分析页面，抓取需求内容
		soup = BeautifulSoup(page.content,'html.parser')
		soup = soup.body
		lis = soup.find_all(attrs={"test":"0"})
		#print(lis)
		for item in lis:
			try:
				#print(item.contents)
				#用beautifulsoup抓取出想要的数据
				lesson_name = item.contents[1].img['title']  #课程名称
				lesson_url = item.contents[1].a['href']  #课程链接
				lesson_content = item.contents[3].p.text
				lesson_content = re.sub("\s", '', lesson_content)  #课程简介
				lesson_stu = item.contents[3].find('em',{'class':'learn-number'}).text  #学习人数
				lesson_time = item.contents[3].find('dd',{'class':'mar-b8'}).em.text  #课程时间
				lesson_time = re.sub("\s", '', lesson_time)  #正则表达式去除字符串中的所有空格
				lesson_level = item.contents[3].find('dd',{'class':'zhongji'}).em.text  #课程难度

				#把抓取的数据保存到元组中，传入save()函数
				lesson_data = {"lesson_name":lesson_name,"lesson_url":lesson_url,"lesson_content":lesson_content,"lesson_stu":lesson_stu,"lesson_time":lesson_time,"lesson_level":lesson_level}
				save(lesson_data)
			except:
				pass


		#设置循环次数
		page_num+=1

def save(lesson):
	name = lesson["lesson_name"]
	url = lesson["lesson_url"]
	cont = lesson["lesson_content"]
	stu = lesson["lesson_stu"]
	time = lesson["lesson_time"]
	level = lesson["lesson_level"]

	#链接数据库sqlite3
	conn = sqlite3.connect(os.path.join(BASE_DIR,'test3_jike.db'))
	cur = conn.cursor()
	sql = "insert into lesson(id,lesson_name,lesson_url,lesson_content,lesson_stu,lesson_time,lesson_level) values(null,'%s','%s','%s','%s','%s','%s')"%(name,url,cont,stu,time,level)
	cur.execute(sql)
	conn.commit()
	conn.close()

if __name__ == '__main__':
	starttime = datetime.datetime.now()
	get_page()
	endtime = datetime.datetime.now()
	print("爬取%d页用时："%PAGE_NUM,(endtime-starttime).seconds,"s")