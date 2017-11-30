from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import sys
import json
import os
import datetime
import psycopg2
from datetime import datetime
from flask_heroku import Heroku
import app_sfmc_functions

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


heroku = Heroku(app)
db = SQLAlchemy(app)


class Basic(db.Model):
	__tablename__ = 'basic'
	id = db.Column(db.Integer, primary_key=True)
	testcol = db.Column(db.String(1000), unique=False, nullable=True)

	@property
	def serialize(self):
		return{
			'id' : self.id,
			'testcol' : self.testcol,
		}

	def __init__(self):
		self.id = self.id
		self.testcol = self.testcol

	def __repr__(self):
		return '<testcol {}>'.format(self.testcol)

class sfmc_access(db.Model):
	__tablename__ = 'sfmc_access'
	id = db.Column(db.Integer, primary_key=True)
	access_token = db.Column(db.String(255), nullable=False)
	expires_in = db.Column(db.Integer, nullable=False)
	begin_datetime = db.Column(db.DateTime, nullable=True)
	expiry_datetime = db.Column(db.DateTime, nullable=True)

	@property
	def serialize(self):
		return{
			'id' : self.id,
			'access_token' : self.access_token,
			'expires_in' : self.expires_in,
			'begin_datetime' : self.begin_datetime,
			'expiry_datetime' : self.expiry_datetime,
		}

	def __init__(self):
		self.id = self.id
		self.access_token = self.access_token
		self.expires_in = self.expires_in
		self.begin_datetime = self.begin_datetime
		self.expiry_datetime = self.expiry_datetime

	def __repr__(self):
		return '<token {}>'.format(self.access_token)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello Sam</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

@app.route('/testapi', methods=['GET'])
def test():
	bas = db.session.query(Basic)
	return jsonify(Basics = [b.serialize for b in bas]), 200

@app.route('/testapipost', methods=['GET'])
def testpost():
	newBasic = Basic()
	db.session.add(newBasic)
	db.session.commit()
	bas = db.session.query(Basic)
	return jsonify(Basics = [b.serialize for b in bas]), 200


@app.route('/testapi/<basicId>', methods=['GET'])
def testId(basicId):

	bas = db.session.query(Basic).filter_by(id=basicId)
	return jsonify(Basics = [b.serialize for b in bas]), 200

@app.route('/testSFMCpipe/auth')
def SFMCAuthTest():
	current_auth = db.session.query(sfmc_access).order_by(sfmc_access.id.desc()).limit(1)

	if current_auth.length == 1:
		token = current_auth
	else:
		token = app_sfmc_functions.SFMC_authenticate()

		tokenToAdd = sfmc_access()
		tokenToAdd.access_token=token['authToken']
		tokenToAdd.expires_in=token['expiresIn']
		tokenToAdd.begin_datetime = datetime.utcnow()
		db.session.add(tokenToAdd)
		db.session.commit()


	return jsonify(token=token.access_token,expires_in=token.expires_in), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)