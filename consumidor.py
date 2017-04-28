from pymongo import MongoClient
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('tw-marthacr')
client = MongoClient('172.17.0.2', 27017)


db = client.mongo_tw

envia = db.tw
print("-----------Listening tweets----------")
for msg in consumer:
	raw = msg.value.decode('utf8')
	doc = json.loads(raw)
	texto= doc['text']
	print(texto)
	res = envia.insert_one(doc)
	
