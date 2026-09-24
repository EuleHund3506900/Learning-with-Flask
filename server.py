from flask import Flask, render_template, redirect, url_for
from blueprints.app import app_bp
from blueprints.dev import dev_bp
from blueprints.auth import auth_bp
from database.db import create_user, init_db, verify_user

app = Flask(__name__)


@app.route("/")
def hello():
  res = verify_user("test3@example.com", "password1233")
  return str(res)


@app.route("/auth/register/")
def register():
  return render_template('auth/register.html')

@app.route("/github-markdown-css/github-css.css")
def ghcss():
  return app.send_static_file('github-css.css')

# register all app routes from blueprints/app.py
app.register_blueprint(app_bp)

# register all dev routes from blueprints/dev.py
app.register_blueprint(dev_bp)

# register all auth routes from blueprints/auth.py
app.register_blueprint(auth_bp)

if __name__ == "__main__":
  init_db()
  app.run(debug=True)