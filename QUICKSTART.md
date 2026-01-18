# Quick Start Guide

## Running the Blog to Podcast Application

### Step 1: Install Dependencies

First, make sure you have Python 3.8 or higher installed. Then install all required packages:

```bash
pip install -r requirements.txt
```

Or if you're using Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

### Step 2: Run the Application

Navigate to the project directory and run:

```bash
streamlit run app.py
```

Or if streamlit is not in your PATH:

```bash
python3 -m streamlit run app.py
```

### Step 3: Access the Application

The application will automatically open in your default web browser at:
- **URL**: `http://localhost:8501`

If it doesn't open automatically, you can manually navigate to that URL.

### Step 4: Use the Application

1. **Choose Input Method**:
   - **URL**: Paste a Forrester blog post URL
   - **Paste Text**: Directly paste blog content

2. **Adjust Settings** (optional):
   - Voice speed, language

3. **Click "Generate Podcast"**

4. **Download Results**:
   - Podcast (MP3 file)

### Troubleshooting

#### Issue: "streamlit: command not found"
**Solution**: Install streamlit or use `python3 -m streamlit run app.py`

#### Issue: Import errors
**Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

#### Issue: TTS not working
**Solution**: 
- gTTS requires internet connection
- Check your internet connection
- Try with shorter text content

### Alternative: Using a Virtual Environment (Recommended)

For a cleaner setup, use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Testing

To run the test suite:

```bash
python3 -m pytest tests/
```

Or run individual tests:
```bash
python3 -m unittest tests.test_blog_fetcher
python3 -m unittest tests.test_podcast_generator
```
