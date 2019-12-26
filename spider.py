import requests as r
from bs4 import BeautifulSoup
import json
import re
import jieba
import wordcloud as wc
from imageio import imread

#通过chrome开发者工具，分析歌手页内容，发现所需信息均在下述url的页面中
basic_info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong69405645034824&g_tk=480556310&loginUin=574294857&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22000keDtj2Um0rT%22%2C%22begin%22%3A0%2C%22num%22%3A10%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D'

def find_basic_info(url):
	res_1 = r.get(url)
	res_1.encoding = res_1.apparent_encoding
	songs = json.loads(res_1.text)
	for song in songs['singerSongList']['data']['songList']:
		add_to_file('歌曲:' + song['songInfo']['name'])
		find_lyric(song['songInfo']['mid'],str(song['songInfo']['id']))

def find_lyric(mid,id):
	#歌词页面中发现，歌词内容文件的Request url是动态变化的，变化参数为musicid；其中parameters也只有musicid为变化参数
	url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid='+id+'&-=jsonp1&g_tk=480556310&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
	paramters = {
	'nobase64':'1',
	'musicid': id,
	'-':'jsonp1',
	'g_tk':'480556310',
	'loginUin':'0',
	'hostUin':'0',
	'format':'json',
	'inCharset':'utf8',
	'outCharset':'utf-8',
	'notice':'0',
	'platform':'yqq.json',
	'needNewCode':'0'
	}
	#分析发现，request headers中referer参数动态变化，起到防盗链的作用，但变化的参数实际为mid的值
	headers = {
	'user-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'referer':'https://y.qq.com/n/yqq/song/{}.html'.format(mid)
	}

	res_2 = r.get(url=url,params=paramters,headers=headers)
	res_2.encoding = res_2.apparent_encoding
	extract_lyric(res_2.text)

def extract_lyric(text):
	lyric = json.loads(text)
	a = lyric['lyric'].replace('[','<')
	b = a.replace(']','>')
	c = b.replace(';','')
	content = re.sub(u'\\<.*?\\>|\\&#\\d+','\n',c)
	add_to_file('歌词:' + content + '\n')

def add_to_file(text):
	f = open('newpants.txt','at')
	f.write(text+'\n')

def analyse(path):
	mk = imread('logo.png')
	#设置宋体为词云的字体格式，scale用于调整词云图片清晰度
	w = wc.WordCloud(font_path="/Library/Fonts/Songti.ttc",background_color='white',mask=mk,scale=2)

	f = open(path,'rt').read()

	w.generate(' '.join(jieba.lcut(f)))
	w.to_file('wordcloud.png')

def main():
	path = 'newpants.txt'
	find_basic_info(basic_info_url)
	analyse(path)

main()



