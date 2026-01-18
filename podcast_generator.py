"""
Advanced TTS and audio generation for podcast creation.
"""

import os
import tempfile
from typing import Optional
from config import (
    DEFAULT_LANGUAGE, DEFAULT_VOICE_SPEED,
    MAX_AUDIO_CHUNK_SIZE, AUDIO_FORMAT
)
from utils import chunk_text_by_sentences, sanitize_text
from audio_processor import merge_audio_files, normalize_audio, adjust_speed, add_metadata

def generate_with_gtts(text: str, language: str, output_path: str) -> bool:
    """Generate audio using gTTS."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_path)
        return True
    except Exception as e:
        print(f"gTTS error: {e}")
        return False

def generate_podcast(text: str, language: str = DEFAULT_LANGUAGE, 
                    speed: float = DEFAULT_VOICE_SPEED,
                    title: Optional[str] = None,
                    author: Optional[str] = None) -> Optional[str]:
    """
    Generate a podcast (MP3 audio file) from blog text using Google Text-to-Speech (gTTS).
    
    Args:
        text: The blog content text
        language: Language code (e.g., 'en', 'es', 'fr')
        speed: Speech speed multiplier (0.5 to 2.0)
        title: Podcast title for metadata
        author: Author name for metadata
        
    Returns:
        Path to the generated MP3 file, or None if failed
    """
    # Clean the text
    cleaned_text = sanitize_text(text)
    
    if not cleaned_text:
        return None
    
    # Split into chunks if needed
    if len(cleaned_text) > MAX_AUDIO_CHUNK_SIZE:
        chunks = chunk_text_by_sentences(cleaned_text, MAX_AUDIO_CHUNK_SIZE)
    else:
        chunks = [cleaned_text]
    
    audio_files = []
    temp_dir = tempfile.gettempdir()
    
    # Generate audio for each chunk using gTTS
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        
        temp_file = os.path.join(temp_dir, f"chunk_{i}.mp3")
        success = generate_with_gtts(chunk, language, temp_file)
        
        if success and os.path.exists(temp_file):
            audio_files.append(temp_file)
        else:
            print(f"Failed to generate audio for chunk {i} using gTTS")
    
    if not audio_files:
        print(f"ERROR: No audio files generated. Total chunks: {len(chunks)}")
        return None
    
    # Merge audio files if multiple chunks
    if len(audio_files) == 1:
        final_audio_path = audio_files[0]
    else:
        merge_output_path = os.path.join(temp_dir, 'blog_podcast_merged.mp3')
        merged_path = merge_audio_files(audio_files, merge_output_path)
        
        # Check if merge was successful (merged_path will be merge_output_path if successful, or first chunk if failed)
        if merged_path == merge_output_path and os.path.exists(merged_path) and os.path.getsize(merged_path) > 0:
            # Merge succeeded
            final_audio_path = merged_path
            # Clean up individual chunk files
            for f in audio_files:
                try:
                    if f != final_audio_path:
                        os.unlink(f)
                except:
                    pass
        else:
            # Merge failed (likely due to missing ffmpeg), use returned path (first chunk)
            print("WARNING: Audio merge failed (ffmpeg may be required). Using first chunk only.")
            final_audio_path = merged_path  # This should be audio_files[0] from fallback
            # Clean up other chunk files
            for f in audio_files[1:]:
                try:
                    os.unlink(f)
                except:
                    pass
    
    # Apply speed adjustment if needed
    if speed != 1.0:
        speed_adjusted_path = os.path.join(temp_dir, 'blog_podcast_speed.mp3')
        adjust_speed(final_audio_path, speed, speed_adjusted_path)
        if os.path.exists(speed_adjusted_path):
            if final_audio_path != audio_files[0]:  # Don't delete if it was the original chunk
                try:
                    os.unlink(final_audio_path)
                except:
                    pass
            final_audio_path = speed_adjusted_path
    
    # Normalize audio
    normalize_audio(final_audio_path, final_audio_path)
    
    # Add metadata if provided
    if title:
        add_metadata(final_audio_path, title, artist=author or "Blog to Podcast")
    
    # Rename to final output path
    output_path = os.path.join(temp_dir, 'blog_podcast.mp3')
    if final_audio_path != output_path:
        try:
            if os.path.exists(output_path):
                os.unlink(output_path)
            os.rename(final_audio_path, output_path)
        except:
            output_path = final_audio_path
    
    return output_path
