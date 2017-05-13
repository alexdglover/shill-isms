import os

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class Noun(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  phrase = db.Column(db.String(255))

  def __init__(self, phrase):
    self.phrase = phrase

class Adjective(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  phrase = db.Column(db.String(255))

  def __init__(self, phrase):
    self.phrase = phrase


@app.route('/', methods=['GET'])
def index():
  return 'Hello world'

@app.route('/noun', methods=['POST'])
def add_noun():
  new_noun = Noun(phrase)
  try:
    db.session.add(new_noun)
    db.session.commit()
    return 200
  except:
    return 500

@app.route('/adjective/', methods=['POST'])
def add_adjective():
  new_adjective = Adjective(phrase)
  try:
    db.session.add(new_adjective)
    db.session.commit()
    return 200
  except:
    return 500

if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
