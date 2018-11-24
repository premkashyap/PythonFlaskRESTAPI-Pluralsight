from flask import Flask, jsonify, request, Response
import json
from settings import *
import sqlalchemy
import os, jwt, datetime 
import pyodbc
from routes import *
from functools import wraps

app = Flask(__name__)

books = [
    {
        'name': '5 point someone',
        'price': 100,
        'author' : 'Chetan Bhugat',
        'isbn': 123
    },
    {
        'name':'The Krishna Key',
        'price': 200,
        'author': 'Ashwin Sanghi' ,
        'isbn': 456
    }
]

Users = [
    {
        'username': 'kashyap18.prem@gmail.com',
        'pwd': '15081987'
    },
    {
        'username': 'ani.gautam04@gmail.com',
        'pwd': '04041991'
    },
    {
        'username': 'A',
        'pwd': 'A'
    }
]

def match_username_pwd(_username, _pwd):
    for user in Users:
        if user['username'] == _username and user['pwd'] == _pwd:
            return True
        else :
            return False

def get_all_users():
    return Users

def add_user(_username, _pwd):
    Users.append({'username': _username, 'pwd': _pwd})



def initialize_app(app):
    app.config['local_db_connection_string'] = LOCAL_DATABASE_URI
    app.config['SECRET_KEY'] = 'meow'

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'err': 'Need a valid token to view this page'})
    return wrapper

@app.route('/')
def HelloWorld():
    return 'Hello World'

@app.route('/books')
@token_required
def get_books():
    return jsonify({'books':books})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value ={}
    for book in books:
        if book['isbn'] == isbn:
            return_value = book
    return jsonify(return_value)

@app.route('/books', methods=['POST'])
def add_books():
    request_payload = request.get_json()
    if validBookObjectForCreate(request_payload):
        new_book = {
            'name': request_payload['name'],
            'price': request_payload['price'],
            'author': request_payload['author'],
            'isbn': request_payload['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = 'books/' + str(new_book['isbn'])
        return response
    else:
        invalid_request = {
            'error': 'Invalid Json received',
            'hint': "Please send json object in 'name': '5 point someone', 'price': 100, 'author' : 'Chetan Bhugat', 'isbn': 123 format"
        }
        response = Response(json.dumps(invalid_request), 400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
def update_book_by_isbn(isbn):
    request_payload = request.get_json()
    if validBookObjectForUpdate(request_payload):
        for book in books:
            if book['isbn'] == isbn:
                book['name']= request_payload['name']
                book['price']=request_payload['price']
                book['author']=request_payload['author']
        response = Response("", 204, mimetype='application/json')
        response.headers['Location'] = 'books/' + str(book['isbn'])
        return response
    else:
        invalid_request = {
            'error': 'Invalid Json received',
            'hint': "Please send json object in 'name': '5 point someone', 'price': 100, 'author' : 'Chetan Bhugat', 'isbn': 123 format"
        }
        response = Response(json.dumps(invalid_request), 400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book_by_isbn(isbn):
    request_payload = request.get_json()
    for book in books:
        if book['isbn'] == isbn:
            if('name' in request_payload):
                book['name']= request_payload['name']
            if('price' in request_payload):
                book['price']=request_payload['price']
            if('author' in request_payload):
                book['author']=request_payload['author']
    response = Response("", 204, mimetype='application/json')
    response.headers['Location'] = 'books/' + str(book['isbn'])
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book_by_isbn(isbn):
    i = 0
    found = False
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            found = True
        i +=1
    if(found):
        response = Response("", 204, mimetype='application/json')
    else:
        response = Response(json.dumps({
            "Error": "ISBN not found. Unable to Delete"
        }), 404, mimetype='application/json')
    return response

@app.route('/users')
def get_users():
    return jsonify(query_db('Select * from Users'))


def validBookObjectForCreate(book):
    if ('name' in book and 'price' in book and 'author' in book and 'isbn' in book):
        return True
    else:
        return False

def validBookObjectForUpdate(book):
    if ('name' in book and 'price' in book and 'author' in book):
        return True
    else:
        return False

@app.route('/login', methods= ['POST'])
def get_token():
    request_payload = request.get_json()
    username = str(request_payload['username'])
    password = str(request_payload['password'])
    match = match_username_pwd(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm= 'HS256' )
        return token
    else:
        return Response('', 401, mimetype='application/json')

def main():
    initialize_app(app)
    # port = int(os.environ.get("PORT", 5000))
    app.run(port=5000)

# need to set it across the object
def db(sqlconnectionstring=LOCAL_DATABASE_URI):
	engine = sqlalchemy.create_engine(sqlconnectionstring)
	return engine.raw_connection()

def query_db(query, args=(), one=False):
    con = pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}',server = 'PKASHYAP02PC\SQLEXPRESS', database = 'Credentials')
    cur = con.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

if __name__ == '__main__':
    main()
    # print(match_username_pwd('kashyap18.prem@gmail.com', '15081987'))
    # print(get_all_users())