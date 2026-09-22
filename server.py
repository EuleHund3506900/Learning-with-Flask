from flask import Flask, render_template, redirect, url_for
from blueprints.app import app_bp
from blueprints.dev import dev_bp

app = Flask(__name__)


@app.route("/")
def hello():
  print(app.url_map)
  return redirect(url_for("app.courses"))


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


if __name__ == "__main__":
  
  app.run(debug=True)