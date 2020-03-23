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

@server_bp.route('/upload_p', methods=['GET', 'POST'])
def upload_csv_p():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        bulk = [Portfolio(date = row[1],
                travel_product = row[2],
                sessions_ac = row[3],
                bookings_ac = row[4],
                revenue_ac = float(row[5]),
                spend_ac = row[6],
                day_month = row[7],
                day_week = row[8],
                week = row[9],
                month = row[10],
                quarter = row[11],
                year=row[12],
                sessions_aa = row[13],
                bookings_aa = row[14],
                revenue_aa = float(row[15]),
                spend_aa = row[16],
                category = row[17],
                birst_category = row[18],
                ga_category = row[19])
                for row in csv_reader]
        db.session.bulk_save_objects(bulk)
        db.session.commit()
        return redirect(url_for('main.upload_csv_p'))
    return """
            <form method='post' action='/upload_p' enctype='multipart/form-data'>
              Upload a test file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """
