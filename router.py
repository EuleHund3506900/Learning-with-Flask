from blueprints.app import app_bp
from blueprints.dev import dev_bp
from blueprints.auth import auth_bp
from flask import redirect, url_for

class Router:
    def __init__(self, app):
        self.app = app
        self.register_blueprints()
        self.register_routes()

    def register_blueprints(self):
        self.app.register_blueprint(app_bp)
        self.app.register_blueprint(dev_bp)
        self.app.register_blueprint(auth_bp)

    def register_routes(self):
        @self.app.route("/")
        def hello():
            return redirect(url_for('app.home'))

        @self.app.route("/github-css.css")
        def ghcss():
            return self.app.send_static_file('github-css.css')