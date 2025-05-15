import os
import tempfile
from typing import List, Tuple
import psutil

from moviepy import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip

class VideoProcessor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        video = VideoFileClip(video_path)
        audio_path = os.path.join(self.temp_dir, "temp_audio.wav")
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        video.close()
        return audio_path

    # def finalise_subtitles(
    #     self,
    #     subtitles: List[Tuple[Tuple[float, float], str]],
    #     video_size: Tuple[int, int]
    # ) -> List[Tuple[Tuple[float, float], str]]:
    #     subtitles_clip = []
    #     for subtitle in subtitles:
    #         video_width, video_height = video_size
            
    
    def add_subtitles(
        self,
        input_video_path: str,
        output_video_path: str,
        subtitles: List[Tuple[Tuple[float, float], str]]
    ) -> None:
        """
        Add subtitles to video and save the result.
        
        Args:
            input_video_path: Path to the input video
            output_video_path: Path where the output video will be saved
            subtitles: List of ((start_time, end_time), text) tuples
        """
        # Load video first to get dimensions
        video = VideoFileClip(input_video_path)
        video_width, video_height = video.size
        
        # Try to find font file in current directory or system fonts
        font_file_path = os.path.join(os.getcwd(), 'ARIAL.TTF')
        if not os.path.exists(font_file_path):
            # return error if font file not found
            raise FileNotFoundError(f"Font file not found at {font_file_path}. Please ensure the font file is present.")
            
            
        print(f'Font file path: {font_file_path}')
        
        # Create a generator that yields subtitles
        generator = lambda txt: TextClip(
            text=txt,
            font=font_file_path,
            font_size=video_height // 22,  # Scale font size based on video height
            color='white',
            stroke_color='black',
            stroke_width=2,
            size=(video_width, video_height),  # Use video width and height
            method='caption',
            text_align='center',
            vertical_align='bottom',
        )
        
        # Create subtitles clip
        subtitles_clip = SubtitlesClip(subtitles=subtitles, make_textclip=generator)
        
        # Composite video with subtitles
        result = CompositeVideoClip([video, subtitles_clip])
        
        num_cpus = psutil.cpu_count(logical=False)
        
        # Write the result
        result.write_videofile(
            output_video_path,
            codec='libx264',
            fps=video.fps,
            audio_codec='aac',
            temp_audiofile=os.path.join(self.temp_dir, 'temp-audio.m4a'),
            remove_temp=True,
            threads=num_cpus/2,
        )
        
        # Clean up
        video.close()
        result.close() 