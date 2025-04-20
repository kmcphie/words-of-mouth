from gtts import gTTS
import os
from datetime import datetime

def generate_voice(text):
    # Ensure the audio directory exists
    output_dir = "static/audio"
    os.makedirs(output_dir, exist_ok=True)

    # Use timestamp to avoid file name clashes
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"voice_{timestamp}.mp3"
    filepath = os.path.join(output_dir, filename)

    # Generate the voice
    tts = gTTS(text)
    tts.save(filepath)

    return filepath
