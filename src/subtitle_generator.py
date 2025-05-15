from typing import List, Tuple, Dict

class SubtitleGenerator:
    def __init__(self):
        self.max_chars_per_line = 60
        self.max_lines = 2

    def split_text(self, text: str) -> List[str]:
        """
        Split text into lines based on character limits.
        
        Args:
            text: Text to split
            
        Returns:
            List[str]: List of text lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= self.max_chars_per_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines

    def generate_subtitles(self, transcription: Dict) -> List[Tuple[Tuple[float, float], str]]:
        """
        Generate subtitles from Whisper transcription.
        
        Args:
            transcription: Whisper transcription result
            
        Returns:
            List[Tuple[Tuple[float, float], str]]: List of ((start_time, end_time), text) tuples
        """
        subtitles = []
        
        for segment in transcription["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"].strip()
            
            # Split text into lines
            lines = self.split_text(text)
            formatted_text = "\n".join(lines)
            
            # if the number of lines is greater than 2, split into multiple subtitles
            if len(lines) > self.max_lines:
                time_total = end_time - start_time
                for i in range(0, len(lines), self.max_lines):

                    # Calculate start and end time for each segment
                    segment_start = start_time + (i * time_total / len(lines))
                    segment_end = start_time + ((i + self.max_lines) * time_total / len(lines))
                    start_time = segment_start
                    end_time = segment_end
                    
                    if end_time > segment["end"]:
                        end_time = segment["end"]
                    
                    # Create subtitle text for the current segment
                    subtitle_text = "\n".join(lines[i:i + self.max_lines])
                    subtitles.append(((start_time, end_time), subtitle_text))
            else:
                # Create tuple in the format ((start_time, end_time), text)
                subtitles.append(((start_time, end_time), formatted_text))
        
        return subtitles 