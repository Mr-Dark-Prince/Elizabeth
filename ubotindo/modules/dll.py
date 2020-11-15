import pafy, pickledb
from googlesearch import search

db = pickledb.load('meta.db', False)

def dl(input):
	search_input = input
	for song_url in search('youtube.com: '+search_input, tld="co.in", num=1, stop=1, pause=1):
		vid = pafy.new(song_url)
		bestaudio = vid.getbestaudio()
		bestaudio.download(filepath=vid.title+'.mp3')
		title = vid.title
		artist = vid.author
		views = vid.viewcount
		durat = vid.duration[3:]
		db.set('artist', artist)
		db.set('title', title)
		db.set('views', views)
		db.set('durat', durat)
		db.set('uri', song_url)
		db.dump
