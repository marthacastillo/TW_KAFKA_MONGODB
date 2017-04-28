import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime
producer = KafkaProducer(bootstrap_servers='172.17.0.4:9092')

CONSUMER_KEY = '5SV6XgzYO8ddbbS4vnUv3noYt'
CONSUMER_SECRET = 'sQ80VoXyEyovd9SEwR0teaXg4JFiIRrr1a9fxOPz6rjvNv90nT'
ACCESS_KEY_TOKEN = '1661486214-wTnBKyYyykYIiRqwhLFtRSoXj70Zep6dYr6JdFS'
ACCESS_SECRET_TOKEN = 'EkXBBDJFnLl4eU4hza8JmgPFKmKOK2bd6llVSnKCzddHp'

class Listener(StreamListener):
    def on_error(self, status_code):
      if status_code == 420:
        return False 

    def on_data(self, data):
        json_load = json.loads(data)
        
        text= json_load['text']

        tw = datetime.strptime(json_load["created_at"].replace("+0000 ",""), "%a %b %d %H:%M:%S %Y").isoformat()
        usetw = datetime.strptime(json_load['user']['created_at'].replace("+0000 ",""), "%a %b %d %H:%M:%S %Y").isoformat()

        del json_load["created_at"]
        del json_load['user']['created_at']
        json_load["created_at"] = tw
        json_load['user']['created_at'] =usetw
        datatw = json.dumps (json_load, sort_keys = True, indent = 4, separators=[",",":"])

        print(usetw)
        print(text)
        producer.send('tw-marthacr', datatw.encode()) 
       
        
    
    


print("----------Reading tweets--------")

if __name__ == '__main__':
 escucha = Listener()
 auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
 auth.set_access_token(ACCESS_KEY_TOKEN, ACCESS_SECRET_TOKEN)
 stream = Stream(auth, escucha)
 stream.filter(track=['BBVA','BANCOMER','MEXICO'])
 