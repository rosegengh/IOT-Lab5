import pymongo
import numpy
import pprint
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
from pymongo import MongoClient
from sklearn.svm import SVC
client = MongoClient('localhost',27017)
db = client['CordinatesCollection']
collection = db['cordinatescondition']
posts = db.posts
CDATA = []
CDATATRAIN = []
#pprint(db.command("serverStatus"))
for record in collection.find({}):
	#pprint.pprint(record)
	CDATA.append([record['x'],record['y']])
#print(CDATA)
i = 0
count = 0


while i<len(CDATA):
	CDATASUB = []
	j = i
	if(CDATA[i][0] == 0 and CDATA[i][1]==0):
		count = 0
	while(not(CDATA[j][0] == 0 and CDATA[j][1]== 0)):
		if(count < 15):
			CDATASUB.append(CDATA[j][0])
			CDATASUB.append(CDATA[j][1])
			count = count + 1
		j = j + 1
	if(len(CDATASUB)!=0):
		CDATATRAIN.append(CDATASUB)
	i = j + 1
	
#for k in range(0, len(CDATATRAIN)):
#	print(CDATATRAIN[k])

length = len(sorted(CDATATRAIN,key=len,reverse=True)[0])
#x = []
#CDATATRAIN.append([])
#for xi in CDATATRAIN:
#	for i in range(0,length-len(xi)/2):
#		xi = xi + [1]
#		xi = xi + [-9]
#	x.append(xi)
#x = numpy.array(x)
x = numpy.array([xi + [1]*(length-len(xi))for xi in CDATATRAIN])
#x = numpy.array(CDATATRAIN)
#cnm.append(x)
y = numpy.array(['C','C','C','C','C','C','C','C','C','C','O','O','O','O','O','O','O','O','O','O','L','L','L','L','L','L','L','L'
	,'L','L','U','U','U','U','U','U','U','U','U','U','M','M','M','M','M','M','M','M','M','M','B','B','B','B','B','B','B','B','B'
	,'B','I','I','I','I','I','I','I','I','I','I','A','A','A','A','A','A','A','A','A','A'])
#for i in range(0,len(CDATATRAIN)):
#	print(CDATATRAIN[i])
print(x)
print(len(x))
print(len(y))
print(length)
#print(CDATATRAIN)
clf = SVC(gamma='auto')
clf.fit(x, y) 
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)

#print(clf.predict([[1,2,1,9,4,-9,2,16,0,7,-9,9,0,-12,2,-9,0,-3,11,-15,23,-12,28,-4,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9,1,-9]]))

#filename = 'Final.sav'
#pickle.dump(clf, open(filename, 'wb'))
#filename = 'neural network3.sav'
#pickle.dump(clf, open(filename, 'wb'))
