import spacy
from typing import List, Tuple
import webvtt
from pydantic import BaseModel

# Define VideoSegmentModel as a Pydantic model
class VideoSegmentModel(BaseModel):
    start_ms: float
    mid_ms: float
    end_ms: float
    transcript: str

# Define VideoModel as a Pydantic model
class VideoModel(BaseModel):
    id: str
    video_url: str
    title: str
    video_path: str
    transcript_path_vtt: str

class EnhancedPreprocessor:
    def __init__(self, nlp_model: str = "en_core_web_sm"):
        self.nlp = spacy.load(nlp_model)

    def _str_to_timestamp_milliseconds(self, time_str: str) -> float:
        """Convert a string in the format of "HH:MM:SS.sss" to a timestamp in milliseconds."""
        hours, minutes, seconds = time_str.split(":")
        seconds, milliseconds = seconds.split(".")
        return (int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds))

    def _clean_text(self, text: str) -> str:
        """Apply NLP preprocessing to clean and tokenize the text."""
        doc = self.nlp(text)
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

    def _parse_vtt_segments(self, vtt_path: str) -> List[Tuple[float, float, str]]:
        """Parse the WebVTT file, extract segment timings, and preprocess the text."""
        if not vtt_path:
            raise FileNotFoundError(f"Transcript file not found: {vtt_path}")
        
        segments = []
        vtt_content: webvtt.WebVTT = webvtt.read(file=vtt_path)
        
        previous_segment_text = None  # To track the previous segment text

        for idx, transcript_segment in enumerate(vtt_content):
            # Get start and end times in milliseconds
            start_ms = self._str_to_timestamp_milliseconds(transcript_segment.start)
            end_ms = self._str_to_timestamp_milliseconds(transcript_segment.end)
            
            # Preprocess the text
            cleaned_text = self._clean_text(transcript_segment.text)

            # Check for duplicates
            if cleaned_text == previous_segment_text:
                continue  # Skip this segment if it's a duplicate

            # Update previous segment text
            previous_segment_text = cleaned_text

            # Append to segments
            segments.append((start_ms, end_ms, cleaned_text))

        return segments

    def generate_video_segments(self, segments: List[Tuple[float, float, str]]) -> List[VideoSegmentModel]:
        """Generate a list of VideoSegmentModel objects from the segments."""
        video_segments = []
        
        for start_ms, end_ms, cleaned_text in segments:
            mid_ms = (start_ms + end_ms) / 2  # Calculate mid timestamp
            video_segment = VideoSegmentModel(
                start_ms=start_ms,
                mid_ms=mid_ms,
                end_ms=end_ms,
                transcript=cleaned_text
            )
            video_segments.append(video_segment)
        
        return video_segments

    def process_video(self, video_data: VideoModel) -> List[VideoSegmentModel]:
        """Process the video and return a list of VideoSegmentModel objects."""
        # Parse the VTT segments
        segments = self._parse_vtt_segments(video_data.transcript_path_vtt)
        
        # Generate video segments
        video_segments = self.generate_video_segments(segments)
        
        return video_segments

if __name__ == "__main__":
    # Create an instance of VideoModel
    video_data = VideoModel(
        id="SYQk0wj0hE0",
        video_url="https://www.youtube.com/watch?v=SYQk0wj0hE0",
        title="The 5 Essential Components of Wine: A Beginner's Guide",
        video_path="data/raw/videos/The_5_Essential_Components_ofWine-_A_Beginner_s_Guide_SYQk0wj0hE0.mp4",
        transcript_path_vtt="data/raw/transcripts/The_5_Essential_Components_ofWine-_A_Beginner_s_Guide_SYQk0wj0hE0.vtt"
    )

    # Create an instance of EnhancedPreprocessor
    preprocessor = EnhancedPreprocessor()

    # Initialize video_segments variable
    video_segments = []
