import spacy
from typing import List, Tuple
import webvtt

class EnhancedPreprocessor:
    def __init__(self, nlp_model: str = "en_core_web_sm"):
        self.nlp = spacy.load(nlp_model)

    def _str_to_timestamp_milliseconds(self, time_str: str) -> float:
        hours, minutes, seconds = time_str.split(":")
        seconds, milliseconds = seconds.split(".")
        return (int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds))

    def _clean_text(self, text: str) -> str:
        doc = self.nlp(text)
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

    def _parse_vtt_segments(self, vtt_path: str) -> List[Tuple[float, float, float, str]]:
        if not vtt_path:
            raise FileNotFoundError(f"Transcript file not found: {vtt_path}")
        
        segments = []
        vtt_content: webvtt.WebVTT = webvtt.read(file=vtt_path)
        
        previous_segment_text = None  # To track the previous segment text

        for idx, transcript_segment in enumerate(vtt_content):
            # Get start and end times in milliseconds
            start_ms = self._str_to_timestamp_milliseconds(transcript_segment.start)
            end_ms = self._str_to_timestamp_milliseconds(transcript_segment.end)
            
            # Compute mid timestamp
            mid_ms = (start_ms + end_ms) / 2
            
            # Preprocess the text
            cleaned_text = self._clean_text(transcript_segment.text)

            # Check for duplicates
            if cleaned_text == previous_segment_text:
                continue  # Skip this segment if it's a duplicate

            # Update previous segment text
            previous_segment_text = cleaned_text

            # Append to segments
            segments.append((start_ms, mid_ms, end_ms, cleaned_text))

        return segments

if __name__ == "__main__":
    # Path to your VTT file
    vtt_file_path = "path/to/your/transcript.vtt"  # Update this path

    # Create an instance of EnhancedPreprocessor
    preprocessor = EnhancedPreprocessor()

    # Process the VTT segments
    try:
        segments = preprocessor._parse_vtt_segments(vtt_file_path)
        for segment in segments:
            print(segment)  # Print each segment (start, mid, end, cleaned text)
    except Exception as e:
        print(f"Error processing VTT file: {str(e)}")