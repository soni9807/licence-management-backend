from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.routes.licence import licenceBP

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(licenceBP)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
