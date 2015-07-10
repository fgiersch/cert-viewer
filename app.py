from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

staticImgs = {
	"qrcodeImg": "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",
	"logoImg": "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",
	"signatureImg": "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"
	}

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/hierarchy')
def test():
	return "trial"

@app.route('/<id>')
def award(id=None):
	if id:
		recipient = mongo.db.awards.find_one({"_id": ObjectId(id)})
		print recipient
		if recipient:
			award = {
				"qrcodeImg": staticImgs["qrcodeImg"],
				"logoImg": staticImgs["logoImg"],
				"signatureImg": staticImgs["signatureImg"],
				"name": recipient["name"],
				"title": recipient["title"],
				"organization": recipient["organization"],
				"year": recipient["year"],
				"text": recipient["schema:text"]
			}
			return render_template('award.html', award=award)
		else:
			return id
	else:
		return "Error, please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)