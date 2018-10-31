from socket import *
import json
from pymongo import MongoClient

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 9876))
s.listen(1)
print("start to receive")

class MongoDBManagement:
     def __init__(self):
	self.client = MongoClient('localhost',27017)
	self.db = self.client['CordinatesCollection']
	self.collection_student = self.db['cordinatescondition']


count = 0
mongDB = MongoDBManagement()
while True:
	con, addr = s.accept()
	data1 = con.recv(1024)
	data = json.loads(data1)
	con.send("having received data")
	mongDB.collection_student.insert_one({
		"x":data[0],
		"y":data[1]
	})
	print(data[0],data[1])
  			
	if data == '':
		con.close()
		break




