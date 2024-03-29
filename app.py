import os
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__, static_url_path='/static') 

@app.route('/', methods=['GET'])
def show_ratings():
    ratings = app.config.get('RATINGS', {})
    return render_template('index.html', ratings=ratings)

@app.route('/update-ratings', methods=['POST'])
def update_ratings():
    print("Expected API Key:", os.environ.get('API_KEY'))
    api_key = request.headers.get('API-Key')
    if api_key != os.environ.get('API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401

    ratings = request.get_json()
    if ratings is None:
        return jsonify({'error': 'Bad request'}), 400

    app.config['RATINGS'] = ratings.get('ratings', {})
    return jsonify({'message': 'Ratings updated successfully'}), 200

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename, cache_timeout=31536000)
