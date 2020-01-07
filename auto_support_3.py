

'''
	定期抓取bing壁纸并设置为桌面。
	by：Json Chen
	created：2017-05-07
	change log:
			2018-12-11	Json	调整壁纸设置方式为修改注册表
'''


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
import pdb
import os
import hashlib
import time,datetime
import math
import random
import smtplib
import ctypes
import imaplib, email
import win32api,win32process,win32con,win32gui
from PIL import Image,ImageFont,ImageDraw
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header




#定义图片保存的函数
def saveImage(picname,picurl):
	while(True):
		try:
			req = urllib.request.Request(picurl)
			req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36")
			u = urllib.request.urlopen(req,timeout=3)
			data = u.read()
			#pdb.set_trace()
			f = open(picname, 'wb')
			f.write(data)
			f.close()
			return True
		except Exception as e:
			# print Exception,':',e
			return False
			

def change_background(picture_path):
	ctypes.windll.user32.SystemParametersInfoW(20, 0, os.getcwd() + '\\' + picture_path, 3)		
			
			
			
	
def set_wallpaper_from_bmp(bmp_path):  
	#打开指定注册表路径	
	reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
	#最后的参数:2拉伸,0居中,6适应,10填充,0平铺	 
	win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")	
	#最后的参数:1表示平铺,拉伸居中等都是0  
	win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
	win32api.RegSetValueEx(reg_key, "WallPaper", 0, win32con.REG_SZ, bmp_path) 

	#刷新桌面  
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(img_path):  
	#把图片格式统一转换成bmp格式,并放在源图片的同一目录  
	img_dir = os.path.dirname(img_path)	

	bmpImage = Image.open(img_path)	 
	new_bmp_path = os.path.join(img_dir,'wallpaper.bmp')  
	bmpImage.save(new_bmp_path, "BMP")	
	set_wallpaper_from_bmp(new_bmp_path) 

	
	
	
#获取其他网站相关内容
def get_content(a):
	readSession=requests.Session()
	content="up"
	if a<=1:  #获取「ONE·一个」网站内容
		file=open('vol.txt','r')
		page=int(file.readline())
		file.close()
		while(True):
			try:
				# page=(page+1)%2339
				page = random.randint(1,2548)
				read_url='http://m.wufazhuce.com/one/%d'%page		
				response_read=readSession.get(read_url)
				soup_read=bs4.BeautifulSoup(response_read.text,from_encoding='utf-8')
				content=soup_read.find('p',class_='text-content').text#+'\n\t\t\t\t\tfrom 「ONE · 一个」'
				file=open('vol.txt','w')
				file.write(str(page))
				file.close()
				break
			except Exception as e:
				print('get ONE err,',Exception,':',e)
				time.sleep(1)
				pass
	
	return content
	
	
	

#图片添加文字

def add_text_to_pic(txt):
	#设置字体，如果没有，也可以不设置
	#font = ImageFont.truetype("C:\Windows.old\windows\Fonts\simsun.ttc",25)
	font = ImageFont.truetype('test.otf',21)
	#打开底版图片
	imageFile = "desk.jpg"
	im1=Image.open(imageFile)
	width,height = im1.size
	# 在图片上添加文字 1
	draw = ImageDraw.Draw(im1)
	pix=im1.load()
	r=0
	g=0
	b=0
	#pdb.set_trace()
	for i in range(1,1000):
		r1,g1,b1=pix[width-i, height-100]
		r+=r1
		g+=g1
		b+=b1
	for i in range(1,200):
		r1,g1,b1=pix[width-500, height-50-i]
		r+=r1
		g+=g1
		b+=b1
	r= r/1200
	g= g/1200
	b= b/1200
	#r, g, b = pix[width-800, height-400]
	if (r<128):
		r = 255
	else:
		r = 0
	if (g<128):
		g = 255
	else:
		g = 0
	if (b<128):
		b = 255
	else:
		b = 0
	#pdb.set_trace()
	color=(r,g,b)
	# print r,g,b
	
	
	r2=0
	g2=0
	b2=0
	#pdb.set_trace()
	for i in range(1,1000):
		r1,g1,b1=pix[width-i, 100]
		r2+=r1
		g2+=g1
		b2+=b1
	for i in range(1,200):
		r1,g1,b1=pix[width-500, 50+i]
		r2+=r1
		g2+=g1
		b2+=b1
	r2= r2/1200
	g2= g2/1200
	b2= b2/1200
	#r, g, b = pix[width-800, height-400]
	if (r2<128):
		r2 = 255
	else:
		r2 = 0
	if (g2<128):
		g2= 255
	else:
		g2 = 0
	if (b<128):
		b2 = 255
	else:
		b2 = 0
	#pdb.set_trace()
	color2=(r2,g2,b2)
	
	
	font2 = ImageFont.truetype('test.ttf',27)
	
	
	dif=height - 50
	txt_set=[]
	index=0
	for txt_chip in txt.split('\n'):
		if index%2==0 and index!=0:
			txt_set.append('&')
		index+=1
		if len(txt_chip)>30:
			for i in range(0,len(txt_chip),30):
				txt_set.append(txt_chip[i:i+30])
		else:
			txt_set.append(txt_chip)
	for txt_chip in txt_set:
		if txt_chip=='&':
			draw.line((width-700, height-dif, width, height-dif), fill=(255,255,255), width = 2)
			dif-=15
		else:
			draw.text((width-700,height-dif),txt_chip,color2,font=font)
			draw = ImageDraw.Draw(im1)
			dif-=32
	
	
	font2 = ImageFont.truetype('test.ttf',35)
	message=u'marathon countdown --'
	seconds=(datetime.datetime(2019,4,30,12,0,0) - datetime.datetime.now()).total_seconds()
	days=seconds/24/3600
	message2=u'%2f秒,合计%2f天'%(seconds,days)
	
	# draw.text((width-500,height-200),message,color,font=font2)
	# draw.text((width-500,height-150),message2,color,font=font2)
	# draw.line((width-500, height-410, width, height-410), fill=(255,255,255), width = 2)
	# draw.line((0, 0, 100,100), fill=(255,255,255), width = 3)
	# 保存
	im1.save("desk2.jpg")
	
	
	
	
	

def get_mail_and_set_desk():
	while True:
		try:
			M = imaplib.IMAP4("imap.timesgroup.com") 
			break
		except Exception as e:	 
			# print 'IMAP4 error: %s' % e	
			time.sleep(10)
			pass
	# print M	
	mail_list=[]
	try:  
		try:  
			M.login('chenzexiong','******')  
		except Exception as e:	 
			# print 'login error: %s' % e	 
			M.close()  
		#M.select()
		result, message = M.select()
		months=['padding','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		today = datetime.date.today()
		year=today.year
		month=months[today.month]
		day=today.day
		date='%s-%s-%s'%(day,month,year)
		typ, data = M.search(None, 'ON',date)
		
		i=0
		for num in string.split(data[0]):  
			try:
				# if i>2:
					# break
				#print '1'
				#pdb.set_trace()
				typ, data = M.fetch(num, '(RFC822)')
				#print '2'
				msg = email.message_from_string(data[0][1])
				#print '3'
				mailContentDict = parseEmail(msg)
				#print '4'
				from_user=re.search(r'<.+>',msg["From"]).group(0)
				#print '5'
				# print from_user
				subject = email.Header.decode_header(msg["Subject"])
				sub = my_unicode(subject[0][0], subject[0][1])
				# print sub	 
				time1=re.search(r'\d+:\d+:\d+',msg["Date"]).group(0)
				time1=re.sub(r':','',time1)
				# print time1
				# print "_______________________________"
				#print '6'
				mail_list.append((from_user,sub,time1))
				#print '7'
				i+=1
				
				
			except Exception as e:
				pass
				# print 'got msg error: %s' % e			   
		#M.close()
		M.logout()
	except Exception as e: 
		pass
		# print 'imap error: %s' % e
	#pdb.set_trace()
	try:
		mail_list2=sorted(mail_list, key=lambda mail_list : mail_list[2])
		message=get_content(0)+'\n'
		lenth=min(4,len(mail_list2)+1)
		for i in range(1,lenth):
			mail = mail_list2[-i]
			message+=u'邮件：%s\n发送人：%s\n'%(mail[1],mail[0])
		add_text_to_pic(message)
		set_wallpaper(os.getcwd()+'\\desk2.jpg')
		#pdb.set_trace()
	except Exception as e: 
		pass
		# print 'get mail info error: %s' % e		
	
	
def getUrlRespHtml(url):
	# heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			# 'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
			# 'Accept-Language':'zh-cn,zh;q=0.5',
			# 'Cache-Control':'max-age=0',
			# 'Connection':'keep-alive',
			# 'Host':'John',
			# 'Keep-Alive':'115',
			# 'Referer':url,
			# 'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
	
	# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
	# urllib.request.install_opener(opener)
	# req = urllib.request.Request(url)
	# opener.addheaders = heads.items()
	# respHtml = opener.open(req).read()
	res = requests.get(url)
	respHtml = res.text
	return respHtml

	
	
	
def get_bing_wallpaper():
	redate=getUrlRespHtml('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')

	redate=json.loads(redate)
	# pdb.set_trace()
	backgroundimg = redate['images'][0]['url']
	today_demo = redate['images'][0]['copyright']
	saveImage('desk.jpg','http://www.bing.com'+backgroundimg)
	print(today_demo)
	return today_demo


	
def get_ngchina_wallpaper():
	try:
		url = 'http://www.ngchina.com.cn/photography/photo_of_the_day/5904.html'
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
		res = requests.get(url)
		soup = bs4.BeautifulSoup(res.content)
		pic_url = soup.find("div",class_="tab_wrapper").div.ul.li.a.img['src']
		today_demo = soup.find('meta', attrs={"name":"description"})["content"]
		print(pic_url)
		# print(saveImage('desk.jpg',pic_url))
		res = requests.get(pic_url)
		f = open("desk.jpg","wb")
		f.write(res.content)
		f.close()
		return today_demo
	except Exception as e:
		print(e)
		return ""

import ctypes

# ct = win32api.GetConsoleTitle()
# hd = win32gui.FindWindow(0,ct) 
# is_send_desk = 1
# win32gui.ShowWindow(hd,0)	

	
if __name__ == "__main__":

	whnd = ctypes.windll.kernel32.GetConsoleWindow()
	if whnd != 0:
		ctypes.windll.user32.ShowWindow(whnd, 0)
		ctypes.windll.kernel32.CloseHandle(whnd)

	time.sleep(30)
		
	# txt = get_bing_wallpaper()
	
	
	count = 0
	while True:
		if count % 240 == 0:
			txt = get_bing_wallpaper()
		if count % 60 == 0:
			pass
			# txt = get_content(0)
		add_text_to_pic(txt)
	
		change_background('desk2.jpg')
		count += 1
		time.sleep(60)