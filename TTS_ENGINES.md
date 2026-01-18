# Text-to-Speech (TTS) Engine Used for Podcast Generation

The application uses **Google Text-to-Speech (gTTS)** to convert blog text into audio podcasts.

## TTS Engine

### **gTTS (Google Text-to-Speech)**
- **Library**: `gtts` (gTTS Python library)
- **Type**: Online service (requires internet connection)
- **Quality**: Good, natural-sounding voices
- **Languages**: Supports 100+ languages
- **Pros**: 
  - Easy to use
  - Good quality voices
  - Wide language support
  - Free to use (no API key required)
- **Cons**: 
  - Requires internet connection
  - Rate limits may apply for heavy use
  - No offline capability

## How It Works

1. **Text Processing**: Blog content is cleaned and sanitized
2. **Chunking**: Long text is split into chunks (max 4500 characters per chunk)
3. **TTS Generation**: Each chunk is converted to audio using gTTS
4. **Audio Merging**: Multiple chunks are merged into a single audio file
5. **Post-Processing**: 
   - Speed adjustment (if requested)
   - Volume normalization
   - Format conversion to MP3

## Default Settings

- **TTS Engine**: gTTS (Google Text-to-Speech)
- **Default Language**: English (en)
- **Default Speed**: 1.0x (normal speed)
- **Output Format**: MP3

## Troubleshooting

### If podcast generation fails:

1. **Check Internet Connection**:
   - gTTS requires an active internet connection
   - Ensure you're connected to the internet
   - Check if Google's TTS service is accessible

2. **Check Error Messages**:
   - The app shows detailed error messages
   - Check the browser console for technical details

3. **Try Shorter Content**:
   - Very long content may hit rate limits
   - Try with shorter blog posts first

4. **Verify gTTS Installation**:
   - Ensure gTTS is installed: `pip install gtts`
   - Check if there are any import errors

## Technical Details

- **Chunk Size**: 4500 characters per chunk (to avoid TTS API limits)
- **Audio Format**: MP3 (compatible with most players)
- **Sample Rate**: Standard gTTS quality
- **Bitrate**: Standard MP3 quality

## About gTTS

gTTS (Google Text-to-Speech) is a free, open-source Python library that provides an interface to Google's Text-to-Speech API. It's widely used and reliable for converting text to speech. No API key or authentication is required, making it perfect for portfolio projects and educational use.
