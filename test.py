from flask import Flask, request, jsonify
import torchaudio
import os
from bark import generate_audio, SAMPLE_RATE
import numpy as np
import soundfile as sf
import torch  # Make sure to import torch

app = Flask(__name__)

# Set device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Supported languages (for informational purposes, not used in function)
LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "portuguese": "pt",
    "russian": "ru",
    "italian": "it",
    # Add other supported languages here
}

# Function to generate audio using Bark AI
def bark_generate(text, device):
    audio_array = generate_audio(text)  # Remove the language parameter
    output_path = "./output_bark.wav"  # Path for the output file
    sf.write(output_path, audio_array, SAMPLE_RATE)  # Save the output as a WAV file
    return output_path

# API route for Bark voice generation
@app.route('/bark-generate', methods=['POST'])
def generate_voice():
    data = request.get_json()  # Get the JSON payload from the request
    text = data.get('text')
    language_choice = data.get('language', 'english')  # Default to English if no language is provided

    if not text:
        return jsonify({"error": "Text is required"}), 400

    if language_choice not in LANGUAGES:
        return jsonify({"error": "Unsupported language"}), 400

    try:
        output_file = bark_generate(text, device)  # Call the Bark generation function with device
        return jsonify({"output_file": output_file})  # Return the output file path
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Command line language selection (optional)
    print("Choose a language:")
    for i, lang in enumerate(LANGUAGES.keys(), 1):
        print(f"{i}. {lang.capitalize()}")

    choice = input("Enter the number corresponding to your choice: ")

    if choice.isdigit() and 1 <= int(choice) <= len(LANGUAGES):
        language_choice = list(LANGUAGES.keys())[int(choice) - 1]
        print(f"You selected {language_choice.capitalize()}.")
    else:
        print("Invalid choice, defaulting to English.")
        language_choice = "english"

    # Start the Flask app
    app.run(debug=True)
