from flask import Flask

from awsconsolelogin import consolelogin_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(consolelogin_blueprint)
    return app
