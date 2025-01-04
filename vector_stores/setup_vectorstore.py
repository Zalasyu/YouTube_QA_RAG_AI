from pathlib import Path
from lancedb.embeddings import get_registry
from vector_stores.lancedb_yt import LanceDBYT
from pydantic_models.models import VideoSegmentModel
from utils.logger import logger

# Initialize embedding function
embeddings = get_registry().get("huggingface").create(name='facebook/bart-base')
logger.info(f"Embedding function initialized: {embeddings}")

# Initialize vector store
vector_store = LanceDBYT(
    uri=str(Path("data/lancedb")),
    embedding=embeddings,
    vector_key="embeddings",
    text_key="enriched_transcript"
)

# Create some example video segments
video_segments = [
    VideoSegmentModel(
        id=1,
        parent_video_id="video1",
        parent_video_path="/path/to/video1.mp4",
        parent_audio_path="/path/to/audio1.mp3",
        parent_vtt_path="/path/to/transcript1.vtt",
        video_segment_path="/path/to/segment1.mp4",
        video_segment_transcript_path="/path/to/segment1_transcript.txt",
        frame_path="/path/to/frame1.jpg",
        transcript="Original transcript text",
        enriched_transcript="Enriched transcript with context",
        duration_ms=5000.0,
        start_ms=0.0,
        mid_ms=2500.0,
        end_ms=5000.0,
        embeddings=[0.0] * 1536  # This will be replaced by actual embeddings
    )
]

# Create table and add segments
vector_store.create_video_segments_table(video_segments)

# Example search
results = vector_store.similarity_search_with_score(
    query="What is discussed in this video?",
    k=4
)

for doc, score in results:
    print(f"Score: {score}")
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}\n")