# Home Assistant Text-to-Speech (TTS) Integration

This project integrates ElevenLabs Text-to-Speech (TTS) service into Home Assistant, allowing you to generate TTS messages and play them on specified media players. The script leverages the ElevenLabs API to generate audio files and stores them locally for playback.

## Table of Contents
- [Script Explanation](#script-explanation)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)


## Script Explanation
### generate_tts.py
- This script generates TTS audio using the ElevenLabs API and updates a Home Assistant sensor with the latest TTS filename.

### Imports:
- **requests, os, hashlib, and sys** modules are imported for handling API requests, file operations, hashing, and command-line arguments.
  
### Constants:

- **API_KEY, CHUNK_SIZE, URL, HA_URL, and HA_TOKEN** are defined for API access and file handling.
  
### generate_tts(input_text):
- Generates a unique filename based on the input text hash.
- Checks if the file already exists to avoid redundant API calls.
- Sends a POST request to the ElevenLabs API to generate TTS audio.
- Saves the audio file locally and updates the Home Assistant sensor with the new filename.
  
### update_ha_sensor(filename):
- Sends a POST request to Home Assistant to update the latest_tts_filename sensor with the new filename.

## Installation

1. **Clone the Repository:**
   - Download or clone this repository to your local machine.

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Place the Script:**
   - Move the `generate_tts.py` script to the `/config/scripts/` directory of your Home Assistant setup.
   
    ```bash
    mv generate_tts.py /config/scripts/
    ```

3. **Create TTS Directory:**
   - Create a directory named `tts` in the `/config/www/` directory.
   
    ```bash
    mkdir -p /config/www/tts
    ```

4. **Edit Configuration.yaml:**
   - Add the following sensor configuration to your `configuration.yaml` file:
   
    ```yaml
    sensor:
      - platform: template
        sensors:
          latest_tts_filename:
            friendly_name: "Latest TTS Filename"
            value_template: "{{ states('sensor.latest_tts_filename') }}"
    ```

## Configuration

1. **Update Tokens and URLs:**
   - Open the `generate_tts.py` script and replace the placeholders `<ELEVENLAB_TOKEN>`, `<HA_TOKEN>`, and `<HA_IP>` with your actual ElevenLabs API token, Home Assistant Long-Lived Access Token, and Home Assistant IP address, respectively.

2. **Create Shell Command:**
   - Add the following shell command to your `configuration.yaml` file to allow Home Assistant to execute the TTS script:
   
    ```yaml
    shell_command:
      generate_tts: 'python3 /config/scripts/generate_tts.py "{{ text }}"'
    ```

3. **Add TTS Script:**
   - Replace `<HA_IP>` with your corresponding ip adress and add the following script to **Home Assistant**:
   
    ```yaml
    alias: TTS ElevenLabs
    sequence:
      - service: shell_command.generate_tts
        data:
          text: "{{ message }}"
      - delay:
          hours: 0
          minutes: 0
          seconds: 2
          milliseconds: 0
      - service: media_player.play_media
        target:
          entity_id: "{{ media }}"
        data:
          media_content_id: >-
            http://<HA_IP>:8123/local/tts/{{
            states('sensor.latest_tts_filename') }}
          media_content_type: audio/mp3
    fields:
      message:
        selector:
          text: null
        name: message
        description: Message for tts service
        default: No message input
        required: true
      media:
        selector:
          entity: {}
        name: media
        description: media.entity_id
        required: true
    ```

## Usage

To use the TTS script, call the `tts` service with the `message` and `media` fields. For example:
```yaml
service: script.tts
metadata: {}
data:
  message: Hello, world!
  media: media_player.livin_room_speaker
```

This will generate the TTS audio for the provided message and play it on the specified media player.
