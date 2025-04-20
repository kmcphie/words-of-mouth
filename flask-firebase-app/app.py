from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def handle_submit():
    data = {
        'name': request.form.get('name'),
        'pronouns': request.form.get('pronouns'),
        'age': request.form.get('age'),
        'reflection': request.form.get('reflection'),
        'morning': {
            'news': request.form.getlist('morning_news[]'),
            'news_detail': request.form.get('morning_news_detail'),
            'stocks': request.form.get('morning_stocks'),
            'stock_detail': request.form.get('morning_stock_detail'),
            'wisdom': request.form.get('morning_wisdom'),
            'tone': request.form.get('morning_tone'),
            'reminders': request.form.get('morning_reminders'),
            'ritual': request.form.get('morning_ritual')
        },
        'evening': {
            'news': request.form.getlist('evening_news[]'),
            'news_detail': request.form.get('evening_news_detail'),
            'stocks': request.form.get('evening_stocks'),
            'stock_detail': request.form.get('evening_stock_detail'),
            'wisdom': request.form.get('evening_wisdom'),
            'tone': request.form.get('evening_tone'),
            'reminders': request.form.get('evening_reminders'),
            'ritual': request.form.get('evening_ritual')
        }
    }

    db.collection('users').document().set(data)
    return redirect('/success')

@app.route('/success')
def success():
    return "<h2>Thanks! Your brushing preferences were saved successfully 🪥✨</h2>"
