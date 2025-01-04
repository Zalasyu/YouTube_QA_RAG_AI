from pathlib import Path

from pydantic_models.models import VideoModel
from services.transcript_downloader import TranscriptDownloader
from utils.logger import logger


def main():
    
    logger.info("Starting main")
    
    # Base path for raw data
    base_download_path = Path("data/raw")
    base_download_path.mkdir(parents=True, exist_ok=True)

    # Base path for processed data
    base_processed_path = Path("data/processed")
    base_processed_path.mkdir(parents=True, exist_ok=True)
    
    # Download video
    downloader = TranscriptDownloader(base_download_path)
    video_model = downloader.download_transcript_with_video("https://www.youtube.com/watch?v=SYQk0wj0hE0")
    logger.info(f"Downloaded video: {video_model}")

    # Process video
    # preprocessor = TranscriptProcessor(base_processed_path)
    # preprocessor.process_transcript(video_model)

    # Setup vector store
    
    # Add video segments to vector store
    
    # Do a retrieval
    
    logger.info("Done")
    
if __name__ == "__main__":
    main()