from typing import Dict, List, Optional
import whisper
import os

class WhisperService:
    def __init__(self):
        self.models = {}

    def _get_model(self, model_size: str) -> whisper.Whisper:
        """
        Get or load a Whisper model of specified size.
        
        Args:
            model_size: Size of the model (tiny, base, small, medium, large)
            
        Returns:
            whisper.Whisper: Loaded Whisper model
        """
        if model_size not in self.models:
            self.models[model_size] = whisper.load_model(model_size)
        return self.models[model_size]

    def transcribe(
        self,
        audio_path: str,
        model_size: str = "base",
        language: Optional[str] = None
    ) -> Dict:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path: Path to the audio file
            model_size: Size of the Whisper model to use
            language: Language of the audio (optional)
            
        Returns:
            Dict: Transcription result containing segments and other metadata
        """
        model = self._get_model(model_size)
        
        # Prepare options for transcription
        options = {
            "language": language,
            "verbose": False
        }
        
        # check audio file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Whisper: Audio file not found: {audio_path}")
        
        print(f"Whisper: Transcribing audio file: {audio_path} with model size: {model_size}")
        
        # Perform transcription
        result = model.transcribe(audio_path, language=options["language"], verbose=options["verbose"])
        return result 