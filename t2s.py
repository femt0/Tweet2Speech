#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API
from gtts import gTTS
import json
import soundcloud
 
tw_access_token = ""
tw_access_token_secret = ""
tw_consumer_key = ""
tw_consumer_secret = ""
sc_client_id = ""
sc_client_secret = ""
sc_username = ""
sc_password = ""
target_id = ""
audio_dir = ""
file_prefix = ""
 
class StdOutListener(StreamListener):
    def __init__(self, api, sc):
        self.api = api
        self.sc = sc
        self.count = 0
 
    def on_data(self, data):
        jsondata = json.loads(data)

        if 'text' in jsondata and 'retweeted_status' not in jsondata and ('in_reply_to_status_id' not in jsondata or not jsondata['in_reply_to_status_id']):
            text = jsondata['text']
            if 'display_text_range' in jsondata:
                range = jsondata['display_text_range']
                text = text[range[0]:range[1]]
 
            if len(text) > 0:
                print(text)
                self.count += 1
                tts = gTTS(text, lang='fr')
                filepath = audio_dir + file_prefix + '.mp3'
                with open(filepath, 'wb') as f:
                    tts.write_to_fp(f)
                track = self.sc.post('/tracks', track={
                    'title': file_prefix + str(self.count),
                    'asset_data': open(filepath, 'rb')
                })
                print(track.permalink_url)
                api.update_status('@' + jsondata['user']['screen_name'] + ' ' + track.permalink_url, jsondata['id_str'])
                
        return True
 
    def on_error(self, status):
        print(status)
        if status == 420:
            #returning False in on_data disconnects the stream
            return False

sc  = soundcloud.Client(
    client_id=sc_client_id,
    client_secret=sc_client_secret,
    username=sc_username,
    password=sc_password
)

auth = OAuthHandler(tw_consumer_key, tw_consumer_secret)
auth.set_access_token(tw_access_token, tw_access_token_secret)
api = API(auth)
listener = StdOutListener(api, sc)
stream = Stream(auth, listener)
stream.filter(follow=[target_id])
 