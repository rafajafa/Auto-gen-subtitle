import os
import argparse
from pathlib import Path
from typing import Optional

from video_processor import VideoProcessor
from whisper_service import WhisperService
from subtitle_generator import SubtitleGenerator


class VideoSubtitleApp:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.whisper_service = WhisperService()
        self.subtitle_generator = SubtitleGenerator()

    def process_video(
        self,
        input_video_path: str,
        output_video_path: Optional[str],
        model_size: str = "base",
        language: Optional[str] = None
    ) -> bool:
        """
        Process a video file to add subtitles.
        
        Args:
            input_video_path: Path to the input video file
            output_video_path: Path where the output video will be saved (optional, will choose folder in input video file if none given)
            model_size: Size of the Whisper model to use (tiny, base, small, medium, large)
            language: Language of the video (optional, will auto-detect if not specified)
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        audio_path = None  # Initialize audio_path to None for cleanup
        try:
            # Validate input paths
            if not os.path.exists(input_video_path):
                raise FileNotFoundError(f"Input video not found: {input_video_path}")
            
            # if no output video path is provided, use input path           
            if not output_video_path:
                output_video_path = os.path.join(
                    os.path.dirname(input_video_path),
                    f"subtitled_{os.path.basename(input_video_path)}"
                )
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_video_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Extract audio from video
            audio_path = self.video_processor.extract_audio(input_video_path)
            
            assert os.path.exists(audio_path), "Audio extraction failed."
            
            print(f"Extracted audio to: {audio_path}")
            
            # Transcribe audio using Whisper
            transcription = self.whisper_service.transcribe(
                audio_path,
                model_size=model_size,
                language=language
            )
            
            # Generate subtitles
            subtitles = self.subtitle_generator.generate_subtitles(transcription)
              
            # Add subtitles to video
            self.video_processor.add_subtitles(
                input_video_path,
                output_video_path,
                subtitles
            )
            
            # Remove temporary files
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            print(f"Successfully processed video. Output saved to: {output_video_path}")
            return True
            
        except Exception as e:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            print(f"Error processing video: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Add subtitles to video using OpenAI Whisper"
        )
    parser.add_argument("input_video", help="Path to input video file")
    parser.add_argument("--output_video", help="Path to output video file")
    parser.add_argument("--model", 
                        default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)"
                        )
    parser.add_argument("--language", help="Language of the video (optional)")
    
    args = parser.parse_args()
    
    app = VideoSubtitleApp()
    success = app.process_video(
        args.input_video,
        args.output_video,
        model_size=args.model,
        language=args.language
    )
    
    if not success:
        print("Failed to process video.")

if __name__ == "__main__":
    main() 