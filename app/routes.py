from flask import Blueprint, render_template, request, jsonify, url_for
import concurrent.futures
import os

from scripts.get_news import get_news
from scripts.stocks import get_stock_update
from scripts.get_summary import get_summary
from scripts.main import generate_voice

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/generate', methods=['POST'])
def generate():
    # Run stock and news functions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_news = executor.submit(get_news)
        future_stocks = executor.submit(get_stock_update)

        news_result = future_news.result()
        stocks_result = future_stocks.result()

    combined = f"{news_result}\n\n{stocks_result}"
    summary = get_summary(combined)

    audio_path = generate_voice(summary)
    audio_url = url_for('static', filename=f'audio/{os.path.basename(audio_path)}')

    return jsonify({'summary': summary, 'audio_path': audio_url})
