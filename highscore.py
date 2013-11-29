from pymongo import MongoClient
import datetime

client = MongoClient()
db = client['highscores']
scores = db['scores']

#eventually this line of code wont be there. here for testing purposes.
db.scores.remove()

#the following code will eventually be replaced
#with grabbing the real life results
score1 = {"user": "jeremy",
         "numclicks": 34,
         "time": 34, 
         "date": datetime.datetime.utcnow()}

score2 = {"user": "maia",
         "numclicks": 23,
         "time": 31, 
         "date": datetime.datetime.utcnow()}

score3 = {"user": "chris",
          "numclicks": 48,
          "time": 16,
          "date": datetime.datetime.utcnow()}

score4 = {"user": "shaan",
          "numclicks": 50,
          "time": 45,
          "date": datetime.datetime.utcnow()}
          

scores.insert(score1)
scores.insert(score2)
scores.insert(score3)
scores.insert(score4)

cursor = db.scores.find(limit=50).sort("time")
results = [line for line in cursor]

for dict in results:
    print "user:" + str(dict["user"]) + "~~~ time:" + str(dict["time"])




