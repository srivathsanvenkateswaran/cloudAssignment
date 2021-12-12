from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'
db = SQLAlchemy(app)   

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    key = db.Column(db.String(), unique=True, nullable=False)

    def repr(self):
        return f'username: {self.username}, key: {self.key}'

def generateAPI_KEY():
    import secrets
    key = secrets.token_urlsafe(16)
    return key

def getJsonFromFile(filename):
    import json
    import os, time
    lastModifiedTime = os.path.getmtime(f'results/{filename}')
    currentTime = time.time()
    if(currentTime-lastModifiedTime > 3600):
        # It has been more than an hour since the file has been updated 
        os.system('bash crawl.sh')
        # Here we need to update the logic for scrawling

    with open(f"results/{filename}" , 'r') as f:
        return json.loads(f.read())

def validateAPI_KEY(uname, API_KEY):
    temp = User.query.filter_by(username=uname).all()
    if len(temp)<=0:
        abort(404, message="User doesn't exist")
    else:
        return temp[0].key == API_KEY

class apiUser(Resource):
    def get(self, userName, CodeString):
        if(CodeString == "Enter your code string here"):
            temp = User.query.filter_by(username=userName).all()
            if len(temp)>0:
                return f"User {temp[0].username} already exists with API_KEY: {temp[0].key}", 201
            else:
                return f"User {userName} doesn't exist", 201
        else:
            return "You are unauthorized", 401
        
    
    def put(self, userName, CodeString):
        if(CodeString == "Enter your code string here"):
            temp = User.query.filter_by(username=userName).all()
            if len(temp)>0:
                return f"User {temp[0].username} already exists with API_KEY: {temp[0].key}", 201
            else:
                user = User()
                user.username = userName
                user.key = generateAPI_KEY()
                db.session.add(user)
                db.session.commit()
                return f"New user {user.username} with API_KEY: {user.key} created", 201
        else:
            return "You are unauthorized", 401

class Article(Resource):
    def get(self, userName, API_KEY):
        if(validateAPI_KEY(userName, API_KEY)):
            return {
                "status" : 'OK', 
                "response" : getJsonFromFile("finalArticleList.json") 
            }
        else:
            return{
                "status" : 'NOT OK',
                "error" : 'Invalid API_KEY'
            }
    


api.add_resource(Article, "/getNews/<string:userName>/<string:API_KEY>")   
api.add_resource(apiUser, "/createUser/<string:userName>/<string:CodeString>") 

if __name__ == "__main__":
    app.run(debug=True)
