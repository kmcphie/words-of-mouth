# from flask import Flask, request, jsonify
# from stocks import prepare_morning_content
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# @app.before_request
# def handle_options_request():
#     if request.method == 'OPTIONS':
#         return '', 200

# @app.route('/api/stock-summary', methods=['POST'])
# def stock_summary():
    # data = request.get_json()
    # user_id = data.get('user_id')
    # summary = prepare_morning_content(user_id)
    # return jsonify({'stock_summary': summary})

# if __name__ == '__main__':
#     app.run(debug=True, port=5050)


from flask import Flask, request, jsonify
from flask_cors import CORS
from stocks import prepare_morning_content

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/stock-summary', methods=['POST', 'OPTIONS'])
def stock_summary():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    print(f"Received data: {data}")
    user_id = data.get('user_id')
    summary = prepare_morning_content(user_id)
    return jsonify({'stock_summary': summary})

if __name__ == '__main__':
    app.run(debug=True, port=5050)