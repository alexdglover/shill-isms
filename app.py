import os
import random
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import load_only

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

# Initialize tables
db.create_all()

@app.route('/', methods=['GET'])
def index():
  # Get random phrase from each table
  adjective = Adjective.query.options(load_only('id')).offset(
    func.floor(
      func.random() * db.session.query(func.count(Adjective.id))
    )
  ).limit(1).all()
  noun = Noun.query.options(load_only('id')).offset(
    func.floor(
      func.random() * db.session.query(func.count(Noun.id))
    )
  ).limit(1).all()
  print(str(adjective))
  print(str(noun))
  return '{} {}'.format(str(adjective), str(noun))

@app.route('/noun/<phrase>', methods=['POST'])
def add_noun(phrase):
  new_noun = Noun(phrase)
  # try:
  db.session.add(new_noun)
  db.session.commit()
  return 'OK'
  # except:
  #   return 'Error when writing to database', 500

@app.route('/adjective/<phrase>', methods=['POST'])
def add_adjective(phrase):
  new_adjective = Adjective(phrase)
  # try:
  db.session.add(new_adjective)
  db.session.commit()
  return 'OK'
  # except:
  #   return 'Error when writing to database', 500

if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
