import os

from flask import Flask


def create_app(test_config=None):
    """application factory function. creates and configures the app."""
    # create and configure the app
    # __name__ =  of current py module
    # tells app that config files are relative to instance folder

    app = Flask(__name__, instance_relative_config=True)

    # set default configs that app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)  # overrides default configs from config.py
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # endure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')  # @app decorator creates a connection between the URL/hello and the function below
    def hello():

        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
