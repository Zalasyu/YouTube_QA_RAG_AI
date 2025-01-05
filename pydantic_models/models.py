from typing import Optional

from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from pydantic import Field

model = get_registry().get("huggingface").create(name='sentence-transformers/all-MiniLM-L6-v2')

# Define VideoSegmentData as a Pydantic model
class VideoSegmentModel(LanceModel):
    id: int
    parent_video_id: str
    parent_video_path: str  # Changed from Path to str for compatibility with PyArrow
    parent_vtt_path: str
    video_segment_path: str
    video_segment_transcript_path: str
    page_content: str
    metadata: dict
    start_ms: float
    mid_ms: float
    end_ms: float
    embeddings: Vector(model.ndims()) # type: ignore


# Define VideoData as a LanceModel for use with LanceDB
class VideoModel(LanceModel):
    id: str
    video_url: str
    title: str
    video_path: str
    transcript_path_vtt: str = ""
    topics: list[str] = []

    def __str__(self) -> str:
        """Return a pretty formatted string representation of the video model."""
        return (
            f"VideoModel(\n"
            f"  id: {self.id}\n"
            f"  title: {self.title}\n"
            f"  video_url: {self.video_url}\n" 
            f"  video_path: {self.video_path}\n"
            f"  transcript_path_vtt: {self.transcript_path_vtt}\n"
            f"  topics: {self.topics}\n"
            f")"
        )
