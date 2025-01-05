from pathlib import Path

from handlers.transcribe_video_handler import TranscribeVideoHandler
from handlers.transcript_available_handler import TranscriptAvailableHandler
from pydantic_models.models import VideoModel
from services.audio_downloader import AudioDownloader
from services.transcript_downloader import TranscriptDownloader
from utils.logger import logger


class YouTubeScraper:
    def __init__(self, base_download_path: Path, medium: str = "YouTube"):

        # Base Path
        self.base_download_path: Path = base_download_path

        # Paths
        self.video_download_path: Path = Path(base_download_path, f"videos/{medium}")
        self.audio_download_path: Path = Path(base_download_path, f"audios/{medium}")
        self.transcript_download_path: Path = Path(base_download_path, f"transcripts/{medium}")
        self.description_download_path: Path = Path(base_download_path, f"descriptions/{medium}")

        # Services
        self.transcript_downloader = TranscriptDownloader(transcript_download_path=self.transcript_download_path)
        self.audio_downloader = AudioDownloader(audio_download_path=self.audio_download_path)

        # Handlers
        self.handler_chain: TranscriptAvailableHandler = self._build_handler_chain()

    def _build_handler_chain(self) -> "TranscriptAvailableHandler":
        """
        Builds a handler chain for the YouTube video processing pipeline.

        The handler chain consists of the following handlers in order:
        1. TranscriptAvailableHandler: Checks if a transcript is available for the video
        2. TranscribeVideoHandler: Transcribes the video using the Whisper model
        3. NoSpeechDetectedHandler: Generates a description for the video if no speech was detected

        Returns:
            TranscriptAvailableHandler: The head of the handler chain
        """
        # Create the handlers
        transcript_available_handler = TranscriptAvailableHandler(transcript_download_path=self.transcript_download_path)
        transcribe_video_handler = TranscribeVideoHandler(transcript_download_path=self.transcript_download_path)

        # Build the handler chain
        transcript_available_handler.set_next(handler=transcribe_video_handler)

        return transcript_available_handler

    def scrape_video(self, video_url: str) -> VideoModel:
        """
        Downloads a YouTube video

        Args:
            video_url (str): The URL of the YouTube video

        Returns:
            Video: The downloaded video
        """
        logger.info(f"Processing {video_url}")

        # Step 1: Download video and audio
        video_data: VideoData = self.video_downloader.download_video(video_url=video_url)

        # Step 2: Download audio
        self.audio_downloader.download_audio(video_url=video_url, video_data=video_data)
        logger.info(f"The video data:\n{video_data}")

        # Step 3: Scrape the transcript, or transcribe the video or generate a description
        video_data = self.handler_chain.handle(video_data=video_data)

        return video_data
