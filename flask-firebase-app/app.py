from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import sys
sys.path.append('..')
from main import run_pipeline
# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')
@app.route('/submit', methods=['POST'])
def handle_submit():
    data = {
        'name': request.form.get('name'),
        'pronouns': request.form.get('pronouns'),
        'age': request.form.get('age'),
        'reflection': request.form.get('reflection'),
        'morning': {
            'news': request.form.getlist('morning_news[]'), # This is in a list
            'news_detail': request.form.get('morning_news_detail'),
            'stocks': request.form.get('morning_stocks'), # This is a string
            'stock_detail': request.form.get('morning_stock_detail'),
            'wisdom': request.form.get('morning_wisdom'),
            'tone': request.form.get('morning_tone'),
            'reminders': request.form.get('morning_reminders'), 
            'ritual': request.form.get('morning_ritual')
        },
        # },
        # 'evening': {
        #     'news': request.form.getlist('evening_news[]'),
        #     'news_detail': request.form.get('evening_news_detail'),
        #     'stocks': request.form.get('evening_stocks'),
        #     'stock_detail': request.form.get('evening_stock_detail'),
        #     'wisdom': request.form.get('evening_wisdom'),
        #     'tone': request.form.get('evening_tone'),
        #     'reminders': request.form.get('evening_reminders'),
        #     'ritual': request.form.get('evening_ritual')
        # }
        'timestamp': datetime.utcnow()
    }

    db.collection('users').document().set(data)

    return redirect('/success')

@app.route('/success')
def success():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Success</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 text-gray-900 flex items-center justify-center min-h-screen">
        <div class="text-center bg-white p-10 rounded-xl shadow-md space-y-6 max-w-md">
            <h2 class="text-2xl font-semibold">Thanks! 🪥✨</h2>
            <p class="text-gray-600">Your brushing preferences were saved successfully.</p>
            <form action="/next" method="post">
                <button type="submit"
                        class="mt-4 w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition">
                    Next
                </button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/latest')
def latest_user():
    users_ref = db.collection('users').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docs = users_ref.stream()
    latest_doc = next(docs, None)

    if latest_doc:
        user_data = latest_doc.to_dict()
        return f"<pre>{user_data}</pre>"
    else:
        return "No users found."

@app.route('/next', methods=['POST'])
def next_step():
    # insert the code to run the audio
    users_ref = db.collection('users').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docs = users_ref.stream()
    latest_doc = next(docs, None)

    if latest_doc:
        user_data = latest_doc.to_dict()
        run_pipeline(user_data) # This runs the main pipeline with the user data
        return "loading audio..."
    else:
        return "No users found."
