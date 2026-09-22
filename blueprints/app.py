from flask import Blueprint, render_template

app_bp = Blueprint('app', __name__, url_prefix='/app')

@app_bp.route("/courses")
def courses():
  return render_template('app/courses.html')

@app_bp.route("/home")
def home():
  return render_template('app/home.html')




