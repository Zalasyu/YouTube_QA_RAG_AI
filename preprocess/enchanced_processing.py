from typing import List, Tuple
import webvtt
from pydantic_models.models import VideoModel
from tqdm import tqdm
class EnhancedPreprocessor:
    def __init__(self):
        pass

    def _str_to_timestamp_milliseconds(self, time_str: str) -> float:
        hours, minutes, seconds = time_str.split(":")
        seconds, milliseconds = seconds.split(".")
        return (int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds))
    
    
    def _parse_vtt_segments(self, video_data: VideoModel) -> List[Tuple[float, float, float, str]]:
        """
        Parse the WebVTT segments from the transcript file and  extract segment timings.


        Args:
            video_data (VideoData): The video data with the transcript path.

        Returns:
            List[Tuple[float, float, float]]: List of segment timings in the format (start_ms, mid_ms, end_ms)
        """

        if not video_data.transcript_path_vtt:
            raise FileNotFoundError(f"Transcript file not found: {video_data.transcript_path_vtt}")

        segments = []
        segments_text = []
        vtt_content: webvtt.WebVTT = webvtt.read(file=video_data.transcript_path_vtt)

        for idx, transcript_segment in tqdm(enumerate(vtt_content)):

            # SKip segment with only one line
            if len(transcript_segment.text.splitlines()) == 1:
                continue

            # Check if the next segment's first line matches the current segment's last line
            # If so then remove the second line
            # Check if there is a next segment
            if idx < len(vtt_content) - 1:
                next_transcript_segment = vtt_content[idx + 1]
                if transcript_segment.text.splitlines()[-1] == next_transcript_segment.text.splitlines()[0]:
                    transcript_segment.text = transcript_segment.text.splitlines()[0]

            # Get the start and end times in milliseconds
            start_ms = self._str_to_timestamp_milliseconds(transcript_segment.start)
            end_ms = self._str_to_timestamp_milliseconds(transcript_segment.end)
            mid_ms = (start_ms + end_ms) / 2

            # Add the segment to the list
            segments.append((start_ms, mid_ms, end_ms, transcript_segment.text))
            segments_text.append(transcript_segment.text)
            # Create the transcript text
            transcript_text = " ".join(segments_text)

        # Remove the last segment
        if len(segments) > 0:
            segments.pop()

        return transcript_text, segments


if __name__ == "__main__":
    # Path to your VTT file
    vtt_file_path = "/home/zalasyu/Documents/projects/youtube_qa_rag_ai/data/raw/transcripts/The_5_Essential_Components_of_Wine_-_A_Beginner_s_Guide_SYQk0wj0hE0.en.vtt.en.vtt"  # Update this path

    # Create an instance of EnhancedPreprocessor
    preprocessor = EnhancedPreprocessor()

    # Create a VideoModel
    # Create a dummy VideoModel object
    dummy_video_model = VideoModel(
    id="dummy_video_1",
    video_url="http://example.com/dummy_video",
    title="Dummy Video Title",
    video_path="/path/to/dummy_video.mp4",
    transcript_path_vtt="data/raw/transcripts/The_5_Essential_Components_of_Wine_-_A_Beginner_s_Guide_SYQk0wj0hE0.en.vtt.en.vtt",
    topics=["example", "dummy", "test"]
)

    # Process the VTT segments
    transcript_text, segments = preprocessor._parse_vtt_segments(dummy_video_model)
    print(transcript_text)
    for segment in segments:
        print(segment)  # Print each segment (start, mid, end, cleaned text)