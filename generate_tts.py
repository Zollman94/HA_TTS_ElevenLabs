import requests
import os
import hashlib
import sys

API_KEY = "<ELEVENLAB_TOKEN>"
CHUNK_SIZE = 1024
URL = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
HA_URL = "http://<HA_IP>:8123/api/states/sensor.latest_tts_filename"
HA_TOKEN = "<HA_TOKEN>"

def generate_tts(input_text):
    # Create a unique filename based on the text input
    text_hash = hashlib.md5(input_text.encode()).hexdigest()
    filename = f"/config/www/tts/{text_hash}.mp3"
    filename_ha = f"{text_hash}.mp3"
    
    # Check if the file already exists
    if os.path.exists(filename):
        # Output filename if it exists
        update_ha_sensor(filename_ha)
        return filename
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }

    data = {
        "text": input_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.4,
            "style": 0.2,
        }
    }

    response = requests.post(URL, json=data, headers=headers)

    # Create .mp3 out of api response
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        # Output filename after saving
        update_ha_sensor(filename_ha)
        return filename
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Send file name as state of sensor to Home Assistant
def update_ha_sensor(filename):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "state": filename,
        "attributes": {
            "friendly_name": "Latest TTS Filename"
        }
    }
    response = requests.post(HA_URL, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to update Home Assistant sensor: {response.status_code} - {response.text}")

if __name__ == "__main__":
    input_text = sys.argv[1]
    generate_tts(input_text)
