from flask import Flask, render_template, request, jsonify
import requests
from google.cloud import translate_v2 as google_translate

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    target_language = data.get("language")
    
    translator = google_translate.Client()
    try:
        translation = translator.translate(text, target_language=target_language)
        return jsonify({"translated_text": translation['translatedText']})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Translation service failed."}), 503

if __name__ == "__main__":
    app.run(debug=True)
