from flask import Blueprint
from io import TextIOWrapper
import csv

from flask import request, redirect, url_for
from app.extensions import db
from .models import User, Portfolio

server_bp = Blueprint('main', __name__)

@server_bp.route('/')
def index():
    return 'Hello World!'

@server_bp.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        bulk = [User(username=row[0], email=row[1]) for row in csv_reader]
        db.session.bulk_save_objects(bulk)
        db.session.commit()
        return redirect(url_for('main.upload_csv'))
    return """
            <form method='post' action='/upload' enctype='multipart/form-data'>
              Upload a csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """
