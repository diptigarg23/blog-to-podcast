# Blog to Podcast Platform

A simple Streamlit-based application that converts any blog posts into engaging podcasts. 

## Features

- 🎙️ **Podcast Generation**: Convert blog text to high-quality audio using Google Text-to-Speech (gTTS)
- 📝 **Flexible Input**: Support for both URL input and direct text pasting
- ⚙️ **Customizable Settings**: Adjust voice speed and language
- 📥 **Download Options**: Download generated podcasts
- ⚖️ **Legal Compliance**: Proper attribution and legal disclaimer handling

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```


## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. The application will open in your default web browser (typically at `http://localhost:8501`)

3. Choose your input method:
   - **URL**: Paste a Forrester blog post URL
   - **Paste Text**: Directly paste blog content

4. Adjust settings (optional):
   - **Podcast Settings**: Voice speed, language

5. Click "Generate Podcast" to process

6. Download your generated podcast (MP3)

## Project Structure

```
Blog_to_Podcast/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration management
├── blog_fetcher.py             # Blog content extraction
├── podcast_generator.py         # TTS and audio generation
├── audio_processor.py          # Audio post-processing
├── legal_compliance.py         # Legal handling
├── ui_components.py            # Reusable UI components
├── utils.py                    # Utilities
├── cache_manager.py            # Caching system
├── requirements.txt            # Dependencies
├── README.md                   # User documentation
├── PORTFOLIO_NOTES.md         # PM portfolio documentation
├── .gitignore                  # Git ignore rules
└── tests/                      # Test suite
    ├── test_blog_fetcher.py
    └── test_podcast_generator.py
```

## Technical Stack (Open-Source Only)

- **Frontend**: Streamlit (open-source web framework)
- **Scraping**: requests, BeautifulSoup4, lxml
- **TTS**: gTTS (Google Text-to-Speech)
- **Audio Processing**: pydub
- **Testing**: pytest

## Configuration

Edit `config.py` to customize:
- Audio quality settings
- Legal compliance settings
- Feature flags

## Legal Considerations

This application is for **educational and portfolio demonstration purposes**. 

- All content is attributed to its original source
- This tool does not claim ownership of Forrester content
- Users are responsible for ensuring their use complies with Forrester's Terms of Use
- For commercial use, please obtain proper licensing from Forrester


## License

This project is open source and available for personal use.

