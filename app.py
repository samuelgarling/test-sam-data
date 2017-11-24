from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy
from json import dumps
from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test-sam-data.herokuapp.com/db'
db = SQLAlchemy(app)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    b = Basic("firstrunhopefullythisworks")
    db.session.add(b)
    db.session.commit()

    c = Basic.query.all()

    return """
    <h1>Hello Miguel</h1>
    <p>{tc}</p>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time, tc=c)

class Basic(db.Model):
	testcol = db.Column(db.String(1000))

	def __init__(self, testcol):
        self.testcol = testcol

    def __repr__(self):
        return '<testcol %r>' % self.testcol

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)