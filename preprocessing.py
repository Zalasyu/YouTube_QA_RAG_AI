import spacy
from typing import List, Tuple
import webvtt

class EnhancedPreprocessor:
    def __init__(self, nlp_model: str = "en_core_web_sm"):
        
        #Initialize the EnhancedPreprocessor with an NLP model.
        
        self.nlp = spacy.load(nlp_model)

    def _str_to_timestamp_milliseconds(self, time_str: str) -> float:
        
        #Convert a string in the format of "HH:MM:SS.sss" to a timestamp in milliseconds.
        
        hours, minutes, seconds = time_str.split(":")
        seconds, milliseconds = seconds.split(".")
        return (
            int(hours) * 3600000  # hours to ms
            + int(minutes) * 60000  # minutes to ms
            + int(seconds) * 1000  # seconds to ms
            + int(milliseconds)  # already ms
        )

    def _clean_text(self, text: str) -> str:
        #Apply NLP preprocessing to clean and tokenize the text.
        
        doc = self.nlp(text)
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

    def _parse_vtt_segments(self, vtt_path: str) -> List[Tuple[float, float, float, str]]:
        
        #Parse the WebVTT file, extract segment timings, and preprocess the text.
        
        if not vtt_path:
            raise FileNotFoundError(f"Transcript file not found: {vtt_path}")

        segments = []
        vtt_content: webvtt.WebVTT = webvtt.read(file=vtt_path)

        for idx, transcript_segment in enumerate(vtt_content):
            # Get start and end times in milliseconds
            start_ms = self._str_to_timestamp_milliseconds(transcript_segment.start)
            end_ms = self._str_to_timestamp_milliseconds(transcript_segment.end)
            mid_ms = (start_ms + end_ms) / 2

            # Preprocess the text
            cleaned_text = self._clean_text(transcript_segment.text)

            # Append to segments
            segments.append((start_ms, mid_ms, end_ms, cleaned_text))

        return segments