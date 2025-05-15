# Video Subtitle Generator

A Python application that automatically adds subtitles to videos using OpenAI's Whisper model and moviepy.

## Features

- Automatic speech-to-text transcription using OpenAI Whisper (Optimize for English only for now)
- Support for multiple languages
- Configurable subtitle formatting
- Local processing (no internet connection required after initial setup)
- Multiple model size options for different accuracy/speed trade-offs

## Requirements

- Python 3.8 or higher
- FFmpeg
- OpenAI Whisper
- MoviePy
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd videoSubtitle
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (if not already installed):
- Windows: Download from https://ffmpeg.org/download.html and add to PATH
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

## Usage

Basic usage:
```bash
python src/main.py input_video.mp4
```

Advanced options:
```bash
python src/main.py input_video.mp4 --output_path output_video.mp4 --model large --language en
```

### Command Line Arguments

- `input_video`: Path to the input video file
- `output_video`: Path where the output video will be saved (optional, will output to the same directory as input video if not specified)
- `--model`: Whisper model size (tiny, base, small, medium, large) - default: base
- `--language`: Language of the video (optional, will auto-detect if not specified)

