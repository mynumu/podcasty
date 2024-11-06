import click
from podcastfy.client import generate_podcast
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@click.command()
@click.option('--urls', '-u', required=True, help='Comma-separated URLs')
@click.option('--podcast-name', '-n', default='Debug Podcast', help='Name of the podcast')
@click.option('--podcast-tagline', '-t', default='Debug Tagline', help='Podcast tagline')
@click.option('--user-instructions', '-i', default='', help='Additional instructions')
@click.option('--tts-model', '-m', default='gemini', help='TTS model to use (gemini, edge, openai, or elevenlabs)')
def generate(urls, podcast_name, podcast_tagline, user_instructions, tts_model):
    """Generate a podcast from URLs using the command line."""

    # Convert comma-separated URLs to list
    url_list = [url.strip() for url in urls.split(',')]

    # Set up the configuration dictionary
    conversation_config = {
        'word_count': 800,
        'conversation_style': ['Engaging', 'Fast-paced', 'Enthusiastic', 'Educational'],
        'roles_person1': 'Interviewer',
        'roles_person2': 'Subject matter expert',
        'dialogue_structure': ['Topic Introduction', 'Summary of Key Points', 'Discussions', 'Q&A Session', 'Farewell Messages'],
        'podcast_name': podcast_name,
        'podcast_tagline': podcast_tagline,
        'output_language': 'English',
        'user_instructions': user_instructions,
        'engagement_techniques': ['Rhetorical Questions', 'Personal Testimonials', 'Quotes', 'Anecdotes', 'Analogies', 'Humor'],
        'creativity': 0.7,
        'text_to_speech': {
            'temp_audio_dir': './data/audio/tmp/',
            'ending_message': "Thank you for listening to this episode. Don't forget to subscribe to our podcast for more interesting conversations.",
            'default_tts_model': tts_model,
            'audio_format': 'mp3'
        }
    }

    try:
        result = generate_podcast(
            urls=url_list,
            conversation_config=conversation_config,
            tts_model=tts_model
        )
        click.echo("Podcast generated successfully!")
        click.echo(result)
    except Exception as e:
        click.echo(f"Error generating podcast: {str(e)}", err=True)

if __name__ == '__main__':
    generate()
