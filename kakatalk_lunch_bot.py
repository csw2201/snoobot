
from flask import Flask
from flask_restful import Api


from resources.keyboard import Keyboard
from resources.message import Message



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)


@app.route('/')
def hello_world():
    
    return 'Hello World!'


api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')

if __name__ == '__main__':
    app.run()
