from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import sys
import json
import os
from datetime import datetime
from flask_heroku import Heroku
app = Flask(__name__)



DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PW = os.environ.get('DATABASE_PW')
DATABASE_DB = os.environ.get('DATABASE_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

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
			'testcol' : self.testcol
		}

	def __init__(self):
		self.id = self.id
		self.testcol = self.testcol

	def __repr__(self):
		return '<testcol {}>'.format(self.testcol)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello Miguel</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

@app.route('/testapi', methods=['GET'])
def test():

	bas = db.session.query.all(Basic)
	return jsonify(Basic = [Basic.serialize for basic in bas])


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)