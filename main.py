from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
import json
# from bson import ObjectId

app = Flask(__name__)


conn = MongoClient('mongodb://localhost:27017')
print(conn)
db = conn.tcc
twitter_new = db.twitter_new

app.config.FLASK_ENV = 'development'
app.config.SECRET_KEY = 'jhgrjhguivuiohnuiv34535324432'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        valor = data['data_valor']
        location = data['data_location']
        twitter_new.update_one({'location': location},{'$set': {'valor': valor}})
        print("valor: " + str(valor) + " location: " + str(location))
        message = twitter_new.find_one({'valor': {'$exists': False}}, {'_id': 0,'tweet_text': 1, "location": 1})
        message_location = {}
        message_location['message'] = message['tweet_text']
        message_location['location'] = message['location']

        return json.dumps(message_location, ensure_ascii=False)
    return render_template('index.html')

@app.route('/start',  methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        data = request.get_json()
        start = data['data_start']
        
        search = twitter_new.find_one({'valor': {'$exists': False} }, {'_id': 0,'tweet_text': 1, 'location': 1})
        message = search['tweet_text']
        location = search['location']
        
        message_location = {}
        message_location['message'] = message
        message_location['location'] = location
        return json.dumps(message_location)


if __name__ == "__main__":
    app.run(debug=True)