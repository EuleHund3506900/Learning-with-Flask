from flask import Blueprint, render_template, url_for
import gh_md_to_html
from bs4 import BeautifulSoup
from markupsafe import Markup

dev_bp = Blueprint('dev', __name__, url_prefix='/dev')

@dev_bp.route("/md")
def md():
    html = gh_md_to_html.main('sample_md.md', core_converter="OFFLINE",)

    
    parsedHTML = "<"+ html.replace(html.split('div')[0], "")
    print(parsedHTML)

    return render_template('app/markdown.html', markdown=(parsedHTML) )