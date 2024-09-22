from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import tempfile
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'en')

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=language)
            tts.save(fp.name)
            return send_file(fp.name, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3")
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)