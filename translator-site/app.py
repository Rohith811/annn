from flask import Flask, render_template, request, jsonify
import requests
import certifi

app = Flask(__name__)

# Language code to full name mapping
LANGUAGE_NAMES = {
    "cat_valencia_uni_iec2017": "Catalan",
    "spa": "Spanish",
    "fra": "French",
    "deu": "German",
    "glg": "Galician",
    "hbs_HR": "Serbo-Croatian",
    "cat_iec2017": "Catalan",
    "hbs_SR": "Serbia",
    "cat": "Catalan"
    # Add more as needed
}

# Fetch supported languages from Apertium API
def get_supported_language_pairs():
    try:
        response = requests.get(
            "https://apertium.org/apy/listPairs",
            verify=False  # Disable SSL for debugging
        )
        response.raise_for_status()
        pairs = response.json().get("responseData", [])
        return {pair['targetLanguage'] for pair in pairs if pair['sourceLanguage'] == 'eng'}
    except Exception as e:
        print(f"Error fetching language pairs: {e}")
        return set()

# Get supported languages with full names
SUPPORTED_LANGUAGES = {
    code: LANGUAGE_NAMES.get(code, code) for code in get_supported_language_pairs()
}

@app.route('/')
def index():
    return render_template('index.html', supported_languages=SUPPORTED_LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    language = data.get('language')

    try:
        url = f"https://apertium.org/apy/translate?q={text}&langpair=en|{language}"
        response = requests.get(url, verify=False)
        response.raise_for_status()

        translated_text = response.json().get('responseData', {}).get('translatedText', 'Translation failed.')
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({'translated_text': 'Error during translation.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
