#coding=utf-8

import bs4
import sys
import requests
import json
import requests.utils
import pickle
import re
import string
import urllib
# import urllib2
import pdb
import os
import hashlib
import time
import math
import random
import datetime
import chardet
import collections
from PIL import Image,ImageFont,ImageDraw,ImageFile
import PIL
from datetime import timedelta, date



#修正系统编码
# reload(sys)	 
# sys.setdefaultencoding('utf-8')

testSession=requests.Session()
# file = open('test3.txt','w')

ImageFile.LOAD_TRUNCATED_IMAGES = True

###################################
#定义图片保存的函数
def saveImage(picname,picurl):
	while(True):
		try:
			# req = urllib2.Request(picurl)
			# req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36")
			# u = urllib2.urlopen(req,timeout=30)
			
			u = requests.get(picurl, timeout=90, headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"})
			data = u.content
			#pdb.set_trace()
			f = open(picname, 'wb')
			f.write(data)
			f.close()
			return True
		except Exception as e:
			# file.write(line+'\n')
			print(Exception,':',e)
			pdb.set_trace()
			return False




################
#测试图片合并
def process_image(message, title, author, today_time):
	imageFile = "desk.jpg"
	im1=Image.open(imageFile)
	width,height = im1.size

	disire_height  = 1200
	if height > disire_height:
		resize_para = height / float(disire_height)
		print(resize_para)
		# pdb.set_trace()
		im1 = im1.resize((int(width/resize_para), disire_height))
		width,height = im1.size
	box = (int(width/2-375),0, int(width/2+375),height)
	im1 = im1.crop(box)
	width,height = im1.size
	# txt_height = 600

	#message = u'城市怎麼可能倒立呢？這座芝加哥城其實好端端的站著。然而在日落時，它在鄰近密西根湖的平靜湖面會投下長影；如果光看倒影的話，它的建物看似倒立。這幅迷人但令人疑惑的美麗影像，是在2014年由拍攝者攝於一架即將降落在芝加哥．奧黑爾國際機場的飛機上。影像中，太陽同時出現在雲層上方與下方，只不過後者是平靜湖面的倒影。作為額外的獎賞，如果你仔細看的話 (有點小難度)，在影像中，你會找到另一架可能也是要接近同一座機場的飛機。      作者：Mark Hersch /  图片来自：台湾成功大学物理系'
	# length_message = len(message)
	txt_span = 27
	# num_txt_line = int(math.floor(width/txt_span))
	# num_rows = int(math.ceil(length_message / num_txt_line))
	
	num_rows, message = get_rows(message, width, txt_span)
	
	txt_height_more = 280
	txt_height = (num_rows+1) * (txt_span +15) + txt_height_more
	# if num_rows <= 4:
		# txt_height = (num_rows+1) * 46
	# else:
		# txt_height = 250

	# txt_height_more = max(0, num_rows-4) * 40

	




	







	# im3 = Image.new("RGBA", (width, height),color = None)
	# box= [0, 0, width,height-txt_height]
	# im_crop = im1.crop(box)
	# im3.paste(im_crop, (0, 0,  width,height-txt_height))
	# draw2 = ImageDraw.Draw(im3)
	# draw2.rectangle((0, height-txt_height, width, height), fill=(0, 0, 0, 128))
	# # # im3 = im3.convert('RGB')
	# # #draw2.rectangle((500, 500, 700, 700), fill=(0, 255, 0))
	# # # pdb.set_trace()
	# im1 = im1.convert('RGBA')
	# # # blend = Image.composite(im1, im2)
	# # im1 = im1.point(lambda i: i * 2)
	# blend = Image.blend(im1, im3, 0.3)
	# # # #blend.save("/home/sylecn/d/blend.png")


	# # # out = im1.point()
	# blend.save("desk2.jpg")
	# # if width > width2+30 and height > height2+30:
		

		
	im4 = Image.new("RGBA", (width, height + txt_height),color = None)

	im4.paste(im1, (0, 0, width, height))
	
	
	
	imageFile2 = "qr.jpg"
	im2=Image.open(imageFile2)
	im2 = im2.resize((200,200))
	width2,height2 = im2.size

	box = (int(width/2-100),  height + txt_height-240 , int(width/2+100), height + txt_height-40)

	im4.paste(im2, box)
	
	
	
	width,height = im4.size
	
	
	
	im4 = im4.convert('RGB')
	pix=im4.load()

	area = 200
	for i in range(1,area):
		for j in range(0,width):
			r1,g1,b1=pix[j, height - txt_height - i]
			# pdb.set_trace()
			r1 = int(r1 *  i / area)
			g1 = int(g1 *  i / area)
			b1 = int(b1 *  i / area)
			
			im4.putpixel((j, height - txt_height - i), (r1, g1,b1))
	
	
	txt_height += 100
	# im4.save('desk2.jpg')
	
	draw = ImageDraw.Draw(im4)

	color=(255,255,255)
	# pdb.set_trace()
	draw.line((60, height -310, width - 60, height-310), fill=color, width = 1)
	# font2 = ImageFont.truetype('test3.otf',33)
	# draw.text((50,25), u'半人马星人',color,font=font2)
	
	font2 = ImageFont.truetype('test3.otf',38)

	
	

	draw.text((60,height- txt_height-txt_height_more+170), title,color,font=font2)
	
	font2 = ImageFont.truetype('test3.otf',23)
	draw.text((60,height- txt_height-txt_height_more+250), author,color,font=font2)
	
	font2 = ImageFont.truetype('test3.otf',txt_span-2)
	for row in range(0, num_rows+1):
		# draw.text((60,height-10+row * (txt_span+10)), message[row * num_txt_line: (row+1) * num_txt_line],color,font=font2)
		draw.text((60,height- txt_height-txt_height_more+320+row * (txt_span+15)), message[row],color,font=font2)

	im4.save(today_time + ".jpg")
	
	
	
	
	
def get_rows(message, width, span):
	contents = []
	row_content = ''
	row_len = 0
	row_number = 0
	
	punctuation_list = [',', '.', u'。', u'，', '?', '!', u'?', u'!', ':', u'：', '，']
	for i in range(0, len(message)):
		word  = message[i] 
		if is_cn_char(word):
			row_len += span
		elif word.isalpha():
			row_len += span/2
		elif word == ' ':
			row_len += span/2
		elif word.isdigit():
			row_len += span/2
		# elif word in punctuation_list:
			# pdb.set_trace()
			# row_len += 0
		else:
			row_len += span/2
		row_content += word
		if row_len > width-140 and i<len(message)-1 and message[i+1] not in punctuation_list:
			# pdb.set_trace()
			contents.append(row_content)
			row_content = ''
			row_len = 0
			row_number += 1
	contents.append(row_content)
	return row_number, contents


def is_cn_char(i): 
    return 0x4e00<=ord(i)<0x9fa6

	

mode_choose=input('选择图片获取模式：1为APOD，2为默认:')
if mode_choose =='1':
	date_choose = input(u'选择日期：1为当天，2为手动输入:')
	if date_choose =='1':
		today_time = time.strftime("%Y%m%d")
		today_time = today_time[2:]
	else:
		today_time = input(u'输入日期（例如：161107）:')
	url = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/ap%s.html'%today_time
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.content)
	ps = soup.find_all('p')
	pic_url = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/' + ps[1].find('a')['href']
	saveImage('desk.jpg',pic_url)
	
	content_all = ps[2].text
	content = re.search('(?<=說明:).+', content_all, re.S).group(0)
	content = re.sub('[\r\n \\s]', '', content)
	content = re.sub('FollowAPOD.*', '', content)
	content = re.sub('AlmostHyperspace.*', '', content)

	cs = soup.find_all('center')
	infos = cs[1].text
	infos = infos.split('\n')
	title = infos[1]
	author = infos[3]
	author = author + ' / APOD'
	# pdb.set_trace()

else:
	title=input(u'输入图片标题：')
	title = title.decode('gbk')
	# pdb.set_trace()
	author=input(u'输入图片作者：')
	author = author.decode('gbk')
	content=input(u'输入图片介绍：')
	content = content.decode('gbk')
	
process_image(content, title, author, today_time)







