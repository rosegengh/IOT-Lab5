
from socket import *
import json
from pymongo import MongoClient
import pickle
import time
import numpy 
filename = 'neural network.sav'
loaded_model = pickle.load(open(filename,'rb'))

x = numpy.array([])

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8818))
s.listen(1)
PrePredict = []
print("start to receive")
while True:
	con, addr = s.accept()
    	data1 = con.recv(1024)
    	data = json.loads(data1)
    	print(data)
	#print(x.toString())
	if(len(x)==0):
		con.send('No output yet')
	else:
		con.send(x.tostring())
		print(x.tostring())

	if(not(data[0]==0 and data[1] == 0)):
		PrePredict.append(data[0])
		PrePredict.append(data[1])
	else:
		PrePredict = []
	if(len(PrePredict) == 24):
		print(PrePredict)
		#print(loaded_model.predict([PrePredict]))
		x=loaded_model.predict([PrePredict])
		#print(type(loaded_model.predict([PrePredict])))
		time.sleep(1)
		PrePredict = []
    	if data == None:
		print('close')
       		con.close()
     	   	break


