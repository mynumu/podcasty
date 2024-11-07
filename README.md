# AI Podcast Generator 🎙️

A modern web application that automatically generates engaging podcast conversations from URLs using AI. Powered by [podcastfy.ai](http://podcastfy.ai).

![AI Podcast Generator Screenshot](screenshot.png)

## ✨ Features

- **URL Processing**: Paste multiple URLs to generate content from various sources
- **Multiple TTS Options**:
  - Google TTS (GEMINI)
  - OpenAI TTS
  - ElevenLabs TTS
- **Customizable Settings**:
  - Word count
  - Creativity level
  - Conversation styles
  - Dialogue structure
  - Engagement techniques
- **Persistent Settings**: All settings are saved locally
- **Modern UI**: Clean, responsive interface with Apple-inspired design
- **Real-time Preview**: URL previews with favicons
- **Progress Indicator**: Visual feedback during generation

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Pipenv
- One of the following API keys:
  - Google (Gemini) API key
  - OpenAI API key
  - ElevenLabs API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/giulioco/podcastfy-ui.git
cd podcastfy-ui
```

2. Install dependencies:

```bash
pipenv install
```

3. Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

4. Run the application:

```bash
pipenv shell

export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

5. Open `http://localhost:5000` in your browser

## 🛠️ Configuration

### Advanced Settings

The application supports various customization options:

```python
conversation_config = {
    'word_count': 4000,
    'creativity': 0.7,
    'conversation_style': [
        'Engaging', 'Fast-paced', 'Enthusiastic', 'Educational'
    ],
    'dialogue_structure': [
        'Topic Introduction', 'Summary of Key Points',
        'Discussions', 'Q&A Session', 'Farewell Messages'
    ],
    'engagement_techniques': [
        'Rhetorical Questions', 'Personal Testimonials',
        'Quotes', 'Anecdotes', 'Analogies', 'Humor'
    ]
}
```

### Environment Variables

Required environment variables:

- `GEMINI_API_KEY`: For Google's Gemini model
- `OPENAI_API_KEY`: For OpenAI's services
- `ELEVENLABS_API_KEY`: For ElevenLabs TTS

## 📁 Project Structure

```
podcast-generator/
├── app.py              # Flask application
├── Pipfile            # Dependencies
├── Pipfile.lock       # Locked dependencies
├── static/            # Static files
│   └── audio/         # Generated podcasts
├── templates/         # HTML templates
│   └── index.html     # Main UI template
├── data/             # Data directory
│   └── audio/        # Temporary audio files
└── .env              # Environment variables
```

## 🚀 Deployment

### Deploy to Render

1. Fork this repository
2. Create a new Web Service on Render
3. Use these settings:
   - Build Command: `pip install pipenv && pipenv install --deploy --ignore-pipfile`
   - Start Command: `pipenv run gunicorn app:app --bind 0.0.0.0:$PORT`
4. Add environment variables
5. Deploy!

## 💡 Usage Tips

1. **URL Input**:

   - Paste multiple URLs separated by newlines or commas
   - URLs are automatically parsed and displayed with favicons
   - Remove URLs by clicking the 'x' button

2. **API Keys**:

   - Keys are stored locally in your browser
   - Never transmitted except during podcast generation
   - Can be cleared using the "Clear Form" button

3. **Advanced Settings**:
   - Click "Advanced Settings" to customize generation
   - All settings persist across page reloads
   - Experiment with different combinations for optimal results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Powered by [podcastfy.ai](http://podcastfy.ai)
- UI inspired by Apple's design guidelines
- Icons from Google's favicon service

## 📧 Support

For support:

1. Check the [Issues](https://github.com/yourusername/podcast-generator/issues) page
2. Create a new issue
3. Contact support@podcastfy.ai

## 🔒 Security

- API keys are stored in browser's localStorage
- Keys are only used during podcast generation
- No data is permanently stored on servers
- Generated audio files are temporary

## 🚧 Known Issues

- Generation time varies with content length
- Some TTS services have rate limits
- Audio quality depends on chosen TTS provider

## 🗺 Roadmap

- [ ] Multiple language support
- [ ] Custom voice selection
- [ ] Batch processing
- [ ] Audio post-processing
- [ ] Podcast hosting integration
