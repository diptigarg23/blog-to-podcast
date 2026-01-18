"""
Reusable UI components for Streamlit application.
"""

import streamlit as st
from typing import Optional
import os

def display_progress_bar(message: str, progress: float = 0.0):
    """Display a progress bar with message."""
    if progress > 0:
        st.progress(progress)
    st.info(message)

def display_result_card(title: Optional[str], content: any, file_path: Optional[str] = None,
                       download_label: Optional[str] = None, file_type: Optional[str] = None):
    """Display a result card with download option."""
    if title:
        st.subheader(title)
    
    if file_path and os.path.exists(file_path):
        if file_type == 'audio':
            audio_file = open(file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            audio_file.close()
        elif file_type == 'image':
            st.image(file_path, use_container_width=True)
        
        if download_label:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
                st.download_button(
                    label=download_label,
                    data=file_bytes,
                    file_name=os.path.basename(file_path),
                    mime=file_type or 'application/octet-stream'
                )
    else:
        st.info("Content will appear here after generation")

def display_attribution(metadata: dict):
    """Display attribution information."""
    st.markdown("---")
    st.markdown("### Attribution")
    
    if metadata.get('title'):
        st.markdown(f"**Title:** {metadata['title']}")
    
    if metadata.get('author'):
        st.markdown(f"**Author:** {metadata['author']}")
    
    if metadata.get('date'):
        st.markdown(f"**Date:** {metadata['date']}")
    
    if metadata.get('url'):
        st.markdown(f"**Source:** [{metadata['url']}]({metadata['url']})")
    
    st.markdown("*Content used with attribution for educational/portfolio purposes.*")

def display_legal_disclaimer():
    """Display legal disclaimer."""
    st.markdown("---")
    with st.expander("Legal Disclaimer", expanded=False):
        st.markdown("""
        **Legal Disclaimer**

        This application is for educational and portfolio demonstration purposes. 
        Content from Forrester blog posts is used with proper attribution and in 
        accordance with fair use principles for educational purposes.

        - All content is attributed to its original source
        - This tool does not claim ownership of Forrester content
        - Users are responsible for ensuring their use complies with Forrester's Terms of Use
        - For commercial use, please obtain proper licensing from Forrester

        For more information, please refer to:
        - [Forrester Terms of Use](https://www.forrester.com/policies/terms-of-use/)
        - [Forrester Citation Policy](https://www.forrester.com/policies/citations-policy/)
        """)

def display_error_message(error: Exception, context: str = ""):
    """Display error message in a user-friendly way."""
    st.error(f"❌ Error {context}: {str(error)}")
    with st.expander("Technical Details"):
        st.exception(error)

def display_success_message(message: str):
    """Display success message."""
    st.success(f"✅ {message}")

def display_warning_message(message: str):
    """Display warning message."""
    st.warning(f"⚠️ {message}")

def create_sidebar_settings():
    """Create sidebar settings panel."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Podcast settings
        st.subheader("Podcast Settings")
        voice_speed = st.slider("Voice Speed", 0.5, 2.0, 1.0, 0.1)
        language = st.selectbox("Language", 
                               ["en", "es", "fr", "de", "it", "pt", "zh", "ja"],
                               index=0)
        st.info("Using Google Text-to-Speech (gTTS)")
        
        return {
            'voice_speed': voice_speed,
            'language': language
        }

def display_loading_spinner(message: str):
    """Display loading spinner with message."""
    return st.spinner(message)
