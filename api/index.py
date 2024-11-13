from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create all required directories
required_dirs = [
    '/tmp/audio',
    './data/transcripts',
    './data/audio/tmp'
]

for directory in required_dirs:
    try:
        os.makedirs(directory, exist_ok=True)
        # Ensure proper permissions
        os.chmod(directory, 0o755)
    except Exception as e:
        print(f"Note: Could not create/modify directory {directory}: {e}")

app = Flask(__name__,
    template_folder='../templates',  # Point to templates directory
    static_folder='../static'        # Point to static directory
)

# Create a temp directory for audio files
TEMP_DIR = '/tmp/audio'

# Add near the top of the file
port = int(os.getenv("PORT", 8080))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Import heavy dependencies only when needed
        from podcastfy.client import generate_podcast
        import tempfile
        import shutil

        # Get API keys from form data
        os.environ['GEMINI_API_KEY'] = request.form.get('gemini_key', '')
        os.environ['OPENAI_API_KEY'] = request.form.get('openai_key', '')
        os.environ['ELEVENLABS_API_KEY'] = request.form.get('elevenlabs_key', '')

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

                # Generate a unique filename
                filename = f"podcast_{os.urandom(8).hex()}.mp3"
                output_path = os.path.join(TEMP_DIR, filename)

                # Handle different return types
                if isinstance(result, str) and os.path.isfile(result):
                    # If result is a file path
                    shutil.copy2(result, output_path)
                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': 'News podcast generated successfully'
                    })
                elif hasattr(result, 'audio_path'):
                    # If result is an object with audio_path
                    shutil.copy2(result.audio_path, output_path)
                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': result.details if hasattr(result, 'details') else 'News podcast generated successfully'
                    })
                else:
                    # If result is an error message
                    return jsonify({'error': str(result)}), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

        else:
            # Handle custom podcast generation
            urls = request.form.get('urls', '').split(',')

            # Create conversation config
            conversation_config = {
                'word_count': int(request.form.get('word_count', 4000)),
                'creativity': float(request.form.get('creativity', 0.7)),
                'conversation_style': request.form.getlist('conversation_style[]'),
                'roles_person1': request.form.get('roles_person1', 'Interviewer'),
                'roles_person2': request.form.get('roles_person2', 'Subject matter expert'),
                'dialogue_structure': request.form.getlist('dialogue_structure[]'),
                'podcast_name': request.form.get('podcast_name'),
                'podcast_tagline': request.form.get('podcast_tagline'),
                'output_language': 'English',
                'user_instructions': request.form.get('user_instructions'),
                'engagement_techniques': request.form.getlist('engagement_techniques[]'),
                'text_to_speech': {
                    'temp_audio_dir': TEMP_DIR,
                    'ending_message': "Thank you for listening to this episode.",
                    'default_tts_model': tts_model,
                    'audio_format': 'mp3'
                }
            }

            try:
                # Generate custom podcast with new config
                result = generate_podcast(
                    urls=urls,
                    conversation_config=conversation_config,
                    tts_model=tts_model
                )

                # Generate a unique filename
                filename = f"podcast_{os.urandom(8).hex()}.mp3"
                output_path = os.path.join(TEMP_DIR, filename)

                # Handle different return types
                if isinstance(result, str) and os.path.isfile(result):
                    # If result is a file path
                    shutil.copy2(result, output_path)
                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': 'Podcast generated successfully'
                    })
                elif hasattr(result, 'audio_path'):
                    # If result is an object with audio_path
                    shutil.copy2(result.audio_path, output_path)
                    return jsonify({
                        'audio_url': f'/audio/{filename}',
                        'details': result.details if hasattr(result, 'details') else 'Podcast generated successfully'
                    })
                else:
                    # If result is an error message
                    return jsonify({'error': str(result)}), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

    return render_template('index.html')

# Add a route to serve audio files
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(os.path.join(TEMP_DIR, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
