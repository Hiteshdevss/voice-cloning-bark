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

# Function to generate audio using Bark AI
def bark_generate(text, device):
    audio_array = generate_audio(text, device=device)  # Ensure to use the correct device
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
        output_file = bark_generate(text, device)  # Call the Bark generation function with the device
        return jsonify({"output_file": output_file})  # Return the output file path
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Command line language selection (optional)
    print("Choose a language:")
    print("1. English")
    print("2. Hindi")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        language_choice = "english"
        print("You selected English.")
    elif choice == '2':
        language_choice = "hindi"
        print("You selected Hindi.")
    else:
        print("Invalid choice, defaulting to English.")
        language_choice = "english"

    # Start the Flask app
    app.run(debug=True)
