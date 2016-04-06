#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import pyvona
import json
import soundcloud

#Variables that contains the user credentials to access Twitter API 
tw_access_token = ""
tw_access_token_secret = ""
tw_consumer_key = ""
tw_consumer_secret = ""
iv_access_key="";
iv_access_secret="";
sc_client_id="";
sc_client_secret="";
sc_access_token="";
tw_target_id = ""
tw_target_name = ""

class StdOutListener(StreamListener):
	def __init__(self, voice, sc, api):
		self.voice = voice
		self.sc = sc
		self.api = api
		self.count = 0

	def on_data(self, data):
		jsondata = json.loads(data)
		print jsondata['text']
		if(jsondata['user']['screen_name'] == tw_target_name):
			self.count += 1	
			self.voice.fetch_voice(jsondata['text'].split(' ', 1)[1], 'audio/speech' + str(self.count) + '.mp3')
			track = self.sc.post('/tracks', track={
				'title': 'speech'+str(self.count),
				'asset_data': open('audio/speech'+str(self.count)+'.mp3', 'rb')
			})
			print track.permalink_url
			api.update_status('@' + jsondata['user']['screen_name'] + ' ' + track.permalink_url, jsondata['id_str'])

		return True

	def on_error(self, status):
		print status

auth = OAuthHandler(tw_consumer_key, tw_consumer_secret)
auth.set_access_token(tw_access_token, tw_access_token_secret)
api = tweepy.API(auth)
v = pyvona.create_voice(iv_access_key, iv_access_secret)
v.codec = 'mp3'
v.voice_name = 'Celine'
v.speechÂ_rate ='slow'
sc = soundcloud.Client(access_token=sc_access_token)
l = StdOutListener(v, sc, api)
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
stream.filter(follow=[tw_target_id])
