import streamlit as st
import os
import tempfile
from pathlib import Path
import time
import sys

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import VideoSubtitleApp

def main():
    st.set_page_config(
        page_title="Video Subtitle Generator",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Video Subtitle Generator")
    st.markdown("Upload a video file and generate subtitles using OpenAI Whisper")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_size = st.selectbox(
            "Whisper Model Size",
            ["tiny", "base", "small", "medium", "large"],
            index=1,  # default to base
            help="Larger models are more accurate but slower, make sure your gpu has sufficent VRAM to run the model."
        )
        
        # Language selection
        language = st.selectbox(
            "Language (Optional)",
            ["Auto-detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Japanese", "Korean", "Chinese"],
            help="Leave as 'Auto-detect' for automatic language detection."
        )
        
        # Font file selection
        font_file = st.file_uploader(
            "Font File (Optional)",
            type=['ttf', 'otf'],
            help="Upload a custom font file. Leave empty to use default Arial."
        )
        
        # Show model info
        st.markdown("---")
        st.markdown("**Model Information:**")
        model_info = {
            "tiny": "Fastest, least accurate",
            "base": "Good balance of speed and accuracy",
            "small": "More accurate than base",
            "medium": "High accuracy, slower",
            "large": "Highest accuracy, slowest"
        }
        st.info(f"**{model_size.title()}**: {model_info[model_size]}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Video")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'],
            help="Supported formats: MP4, AVI, MOV, MKV, WMV, FLV"
        )
        
        if uploaded_file is not None:
            # Display video info
            file_size = uploaded_file.size / (1024 * 1024)  # MB
            st.info(f"📊 File: {uploaded_file.name} ({file_size:.1f} MB)")
            
            # Show video preview
            st.video(uploaded_file)
    
    with col2:
        st.header("🎯 Processing")
        
        if uploaded_file is not None:
            if st.button("🚀 Generate Subtitles", type="primary", use_container_width=True):
                process_video(uploaded_file, model_size, language, font_file)
        else:
            st.info("👆 Upload a video file to start")

def process_video(uploaded_file, model_size, language, font_file):
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            status_text.text("📥 Saving uploaded file...")
            progress_bar.progress(10)
            
            input_path = os.path.join(temp_dir, uploaded_file.name)
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
            # Determine output path
            output_filename = f"subtitled_{uploaded_file.name}"
            output_path = os.path.join(temp_dir, output_filename)
            
            # Handle font file
            font_path = None
            if font_file is not None:
                font_path = os.path.join(temp_dir, font_file.name)
                with open(font_path, "wb") as f:
                    f.write(font_file.getbuffer())
            
            # Convert language selection
            language_code = None
            if language != "Auto-detect":
                language_map = {
                    "English": "en",
                    "Spanish": "es",
                    "French": "fr",
                    "German": "de",
                    "Italian": "it",
                    "Portuguese": "pt",
                    "Russian": "ru",
                    "Japanese": "ja",
                    "Korean": "ko",
                    "Chinese": "zh"
                }
                language_code = language_map.get(language)
            
            # Initialize app
            app = VideoSubtitleApp()
            status_text.text("🔄 Processing video...")
            
            # Process the video
            success = app.process_video(
                input_video_path=input_path,
                output_video_path=output_path,
                model_size=model_size,
                language=language_code,
                font_file=font_path,
                progress_bar=progress_bar,
                status_text=status_text
            )
            
            if success and os.path.exists(output_path):
                progress_bar.progress(100)
                status_text.text("✅ Processing complete!")
                
                # Read the output file for download
                with open(output_path, "rb") as f:
                    video_bytes = f.read()
                
                # Create download button
                st.success("🎉 Subtitles generated successfully!")
                st.download_button(
                    label="📥 Download Video with Subtitles",
                    data=video_bytes,
                    file_name=output_filename,
                    mime="video/mp4",
                    use_container_width=True
                )
                
                # Show file size
                output_size = len(video_bytes) / (1024 * 1024)  # MB
                st.info(f"📊 Output file size: {output_size:.1f} MB")
                
            else:
                st.error("❌ Failed to process video. Please check the console for errors.")
                
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main() 