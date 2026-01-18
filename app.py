"""
Main Streamlit application for Blog to Podcast Platform.
"""

import streamlit as st
import os
from config import APP_NAME, APP_VERSION, SHOW_LEGAL_DISCLAIMER
from blog_fetcher import fetch_blog_content, fetch_from_text
from podcast_generator import generate_podcast
from audio_processor import get_audio_duration
from ui_components import (
    create_sidebar_settings, display_result_card, display_attribution,
    display_legal_disclaimer, display_error_message, display_success_message,
    display_warning_message, display_loading_spinner
)
from legal_compliance import apply_excerpt_limits, get_legal_disclaimer

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    </style>
""", unsafe_allow_html=True)

def main_page():
    """Main application page."""
    st.markdown(f'<p class="main-header">🎙️ {APP_NAME}</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform Forrester blog posts into engaging podcasts</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📝 Input Options")
        input_method = st.radio(
            "Choose input method:",
            ["URL", "Paste Text"],
            help="Select how you want to provide the blog content"
        )
        
        if input_method == "URL":
            blog_url = st.text_input(
                "Enter Forrester Blog URL:",
                placeholder="https://www.forrester.com/blog/...",
                help="Paste the URL of the Forrester blog post you want to convert"
            )
            blog_text = None
        else:
            blog_url = None
            blog_text = st.text_area(
                "Paste Blog Content:",
                height=200,
                placeholder="Paste the blog post content here...",
                help="Copy and paste the blog post content directly"
            )
        
        # Settings
        settings = create_sidebar_settings()
        
        # Legal disclaimer in sidebar
        if SHOW_LEGAL_DISCLAIMER:
            with st.expander("Legal Notice"):
                st.markdown(get_legal_disclaimer())
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Blog Content")
        
        if st.button("🚀 Generate Podcast", type="primary"):
            if (input_method == "URL" and blog_url) or (input_method == "Paste Text" and blog_text):
                try:
                    # Fetch or use blog content
                    with display_loading_spinner("Processing your blog post..."):
                        if input_method == "URL":
                            blog_data = fetch_blog_content(blog_url)
                        else:
                            blog_data = fetch_from_text(blog_text)
                    
                    if not blog_data or not blog_data.get('content'):
                        display_error_message(
                            Exception("Failed to fetch or process blog content"),
                            "Content Processing"
                        )
                        return
                    
                    # Apply excerpt limits if enabled
                    content = apply_excerpt_limits(blog_data['content'])
                    metadata = blog_data.get('metadata', {})
                    
                    # Store in session state
                    st.session_state['blog_content'] = content
                    st.session_state['blog_metadata'] = metadata
                    
                    # Generate podcast
                    with display_loading_spinner("🎙️ Generating podcast..."):
                        podcast_path = generate_podcast(
                            content,
                            language=settings['language'],
                            speed=settings['voice_speed'],
                            title=metadata.get('title'),
                            author=metadata.get('author')
                        )
                    
                    if podcast_path and os.path.exists(podcast_path):
                        st.session_state['podcast_path'] = podcast_path
                        audio_duration = get_audio_duration(podcast_path)
                        display_success_message(f"Podcast generated successfully (Duration: {audio_duration:.1f}s)")
                        # Check if this might be a partial podcast (merge may have failed)
                        if len(content) > 4500:
                            st.info("ℹ️ **Note**: For long content, installing ffmpeg may be required for full audio merging. Install with: `brew install ffmpeg` (macOS) or `apt-get install ffmpeg` (Linux)")
                        st.rerun()
                    else:
                        error_msg = "Podcast generation failed. Note: gTTS requires an internet connection."
                        display_error_message(
                            Exception(error_msg),
                            "Podcast Generation"
                        )
                        # Try to provide more helpful error info
                        st.info("💡 **Troubleshooting Tips:**\n"
                               "- Check your internet connection (gTTS requires internet)\n"
                               "- Try with shorter text content\n"
                               "- Check the browser console for detailed error messages")
                    
                except Exception as e:
                    display_error_message(e, "Generation")
            else:
                display_warning_message("Please provide a blog URL or paste the blog content.")
        
        # Display blog content
        if 'blog_content' in st.session_state:
            st.text_area(
                "Extracted Content:",
                st.session_state['blog_content'],
                height=300,
                disabled=True
            )
            
            # Display attribution
            if 'blog_metadata' in st.session_state:
                display_attribution(st.session_state['blog_metadata'])
    
    with col2:
        st.header("🎙️ Generated Podcast")
        
        # Podcast section
        if 'podcast_path' in st.session_state and st.session_state['podcast_path'] is not None and os.path.exists(st.session_state['podcast_path']):
            display_result_card(
                None,
                None,
                st.session_state['podcast_path'],
                "📥 Download Podcast",
                "audio"
            )
        else:
            st.info("Podcast will appear here after generation")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p>Built with ❤️ using Streamlit | {APP_NAME} v{APP_VERSION}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    """Main application entry point."""
    # Initialize session state
    if 'blog_content' not in st.session_state:
        st.session_state['blog_content'] = None
    if 'blog_metadata' not in st.session_state:
        st.session_state['blog_metadata'] = None
    if 'podcast_path' not in st.session_state:
        st.session_state['podcast_path'] = None
    
    # Run main page
    main_page()

if __name__ == "__main__":
    main()
