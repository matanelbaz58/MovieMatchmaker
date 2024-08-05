from flask import Flask
from api_endpoints import api_endpoints

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_endpoints)
    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)