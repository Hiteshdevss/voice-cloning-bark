from flask import Flask, request, jsonify
import torchaudio
import os
from bark import generate_audio, SAMPLE_RATE
import numpy as np
import soundfile as sf

app = Flask(__name__)

# Function to generate audio using Bark AI
def bark_generate(text):
    audio_array = generate_audio(text)  # Generate audio from the text input
    output_path = "./output_bark.wav"  # Path for the output file
    sf.write(output_path, audio_array, SAMPLE_RATE)  # Save the output as a WAV file
    return output_path

# API route for Bark voice generation
@app.route('/bark-generate', methods=['POST'])
def generate_voice():
    data = request.get_json()  # Get the JSON payload from the request
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        output_file = bark_generate(text)  # Call the Bark generation function
        return jsonify({"output_file": output_file})  # Return the output file path
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
