from flask import Flask, jsonify, render_template, request
import hashlib
from pymongo import MongoClient
import datetime
import jwt
client = MongoClient('mongodb+srv://[비밀번호 보호]@cluster0.qwbpf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)
SECRET_KEY = 'hello guys'


@app.route('/')
def home():
    return render_template('sign_up.html')

@app.route('/post')
def posts():
    return render_template('index.html')
    
@app.route('/sign_up', methods=["POST"])
def sign_up():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        'email': email_receive,
        'password' : pw_hash
    }
    db.user.insert_one(doc)
    return jsonify({'msg':'회원가입 완료!'})

@app.route('/log_in', methods=["POST"])
def log_in():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'email':email_receive , 'password': pw_hash})
    if result is not None:
        payload = {
            'id' : str(result['_id']),
            'email' : email_receive,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY,algorithm='HS256')
        return jsonify({'result' : 'success', 'token' : token})
    else:
        return jsonify({'result' : 'fail' , 'msg' : '아이디/ 비밀번호가 일치하지 않습니다.'})
@app.route('/push_post', methods=["POST"])
def push_post():
    email_receive = request.form['email_give']
    comment_receive = request.form['comment_give']
    doc = {
        'email': email_receive,
        'comment' : comment_receive
    }
    db.posts.insert_one(doc)
    return jsonify({'msg' : '저장완료!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)