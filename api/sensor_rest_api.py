from flask import Flask
from flask import json
from pymongo import MongoClient 

app = Flask(__name__)
connection = MongoClient()
db = connection.alarmpi
db.authenticate("user", "pswd")

def process(col):
	result = list(db[col].find().sort("date", -1).limit(10000))
	for element in result: element.pop("_id")
	return result

@app.route("/light")
def light():
	return json.dumps(process("light"))

@app.route("/temperature")
def temperature():
	return json.dumps(process("temperature"))

@app.route("/humidity")
def humidity():
	return json.dumps(process("humidity"))

if __name__ == "__main__":
	app.run(host='0.0.0.0')
