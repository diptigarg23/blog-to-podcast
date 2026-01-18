"""
Audio post-processing utilities.
"""

import os
import tempfile
from typing import Optional
from pydub import AudioSegment
from pydub.effects import normalize

def normalize_audio(audio_path: str, output_path: Optional[str] = None) -> str:
    """
    Normalize audio volume.
    
    Args:
        audio_path: Path to input audio file
        output_path: Path to save normalized audio (optional)
        
    Returns:
        Path to normalized audio file
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        normalized = normalize(audio)
        
        if output_path is None:
            output_path = audio_path
        
        normalized.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Error normalizing audio: {e}")
        return audio_path

def remove_silence(audio_path: str, silence_thresh: float = -50.0, 
                   min_silence_len: int = 100) -> str:
    """
    Remove silence from audio.
    
    Args:
        audio_path: Path to input audio file
        silence_thresh: Silence threshold in dB
        min_silence_len: Minimum silence length in ms
        
    Returns:
        Path to processed audio file
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        
        # Remove silence at beginning and end
        audio = audio.strip_silence(silence_thresh=silence_thresh, 
                                    min_silence_len=min_silence_len)
        
        output_path = os.path.join(tempfile.gettempdir(), 
                                   f"processed_{os.path.basename(audio_path)}")
        audio.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Error removing silence: {e}")
        return audio_path

def adjust_speed(audio_path: str, speed_factor: float, 
                 output_path: Optional[str] = None) -> str:
    """
    Adjust audio playback speed.
    
    Args:
        audio_path: Path to input audio file
        speed_factor: Speed multiplier (0.5 to 2.0)
        output_path: Path to save processed audio (optional)
        
    Returns:
        Path to processed audio file
    """
    try:
        if speed_factor == 1.0:
            return audio_path
        
        audio = AudioSegment.from_file(audio_path)
        
        # Change speed by changing frame rate
        new_sample_rate = int(audio.frame_rate * speed_factor)
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
        audio = audio.set_frame_rate(audio.frame_rate)
        
        if output_path is None:
            output_path = os.path.join(tempfile.gettempdir(), 
                                       f"speed_{speed_factor}_{os.path.basename(audio_path)}")
        
        audio.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Error adjusting speed: {e}")
        return audio_path

def merge_audio_files(audio_files: list, output_path: str) -> str:
    """
    Merge multiple audio files into one.
    
    Args:
        audio_files: List of audio file paths
        output_path: Path to save merged audio
        
    Returns:
        Path to merged audio file
    """
    try:
        combined = AudioSegment.empty()
        
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                try:
                    audio = AudioSegment.from_file(audio_file)
                    combined += audio
                    # Add small pause between chunks
                    combined += AudioSegment.silent(duration=500)  # 0.5 second pause
                except Exception as e:
                    print(f"Error loading audio file {audio_file}: {e}")
                    raise
        
        combined.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Error merging audio files: {e}")
        # If merge fails, return the first audio file as fallback
        if audio_files and os.path.exists(audio_files[0]):
            return audio_files[0]
        return output_path

def add_metadata(audio_path: str, title: str, artist: str = "Blog to Podcast", 
                 album: str = "Generated Podcasts") -> str:
    """
    Add metadata to audio file.
    
    Args:
        audio_path: Path to audio file
        title: Title of the podcast
        artist: Artist name
        album: Album name
        
    Returns:
        Path to audio file with metadata
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        # Note: pydub doesn't support ID3 tags directly
        # For full metadata support, would need mutagen or similar
        # For now, just return the file path
        return audio_path
    except Exception as e:
        print(f"Error adding metadata: {e}")
        return audio_path

def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file in seconds.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0.0

def get_audio_info(audio_path: str) -> dict:
    """
    Get information about audio file.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dictionary with audio information
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        return {
            'duration': len(audio) / 1000.0,
            'frame_rate': audio.frame_rate,
            'channels': audio.channels,
            'sample_width': audio.sample_width,
            'file_size': os.path.getsize(audio_path)
        }
    except Exception as e:
        print(f"Error getting audio info: {e}")
        return {}
