from flask import Flask, render_template, request, jsonify, send_file
from podcastfy.client import generate_podcast
import os
from dotenv import load_dotenv
import tempfile
import shutil

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tts_model = request.form.get('tts_model', 'gemini')

        # Check if this is a news podcast request
        if request.form.get('mode') == 'news':
            news_topic = request.form.get('news_topic')

            try:
                # Generate news podcast using the new method
                result = generate_podcast(
                    topic=news_topic,
                    tts_model=tts_model
                )

                # Create static/audio directory if it doesn't exist
                os.makedirs(os.path.join(app.static_folder, 'audio'), exist_ok=True)

                # Generate a unique filename
                filename = f"podcast_{os.urandom(8).hex()}.mp3"
                static_file_path = os.path.join(app.static_folder, 'audio', filename)

                # If result is just a file path (string)
                if isinstance(result, str):
                    # Copy the generated file to static location
                    shutil.copy2(result, static_file_path)

                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': 'News podcast generated successfully'
                    })
                else:
                    # Handle object response
                    shutil.copy2(result.audio_path, static_file_path)

                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': result.details if hasattr(result, 'details') else 'News podcast generated successfully'
                    })

            except Exception as e:
                return jsonify({'error': str(e)}), 400

        else:
            # Handle custom podcast generation
            urls = request.form.get('urls', '').split(',')
            podcast_name = request.form.get('podcast_name')
            podcast_tagline = request.form.get('podcast_tagline')
            user_instructions = request.form.get('user_instructions')

            try:
                # Generate custom podcast
                result = generate_podcast(
                    urls=urls,
                    podcast_name=podcast_name,
                    podcast_tagline=podcast_tagline,
                    user_instructions=user_instructions,
                    tts_model=tts_model
                )

                # Check if result is a string (error message) or dict (success)
                if isinstance(result, str):
                    return jsonify({'error': result}), 400

                # Create static/audio directory if it doesn't exist
                os.makedirs(os.path.join(app.static_folder, 'audio'), exist_ok=True)

                # Generate a unique filename
                filename = f"podcast_{os.urandom(8).hex()}.mp3"
                static_file_path = os.path.join(app.static_folder, 'audio', filename)

                # Copy the generated file to static location
                shutil.copy2(result.audio_path, static_file_path)

                return jsonify({
                    'audio_url': f'/audio/{filename}',
                    'details': result.details if hasattr(result, 'details') else 'Podcast generated successfully'
                })

            except Exception as e:
                return jsonify({'error': str(e)}), 400

    return render_template('index.html')

# Add a route to serve audio files
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(os.path.join(app.static_folder, 'audio', filename))

if __name__ == '__main__':
    app.run(debug=True)
