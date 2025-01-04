from pathlib import Path
from yt_dlp import DownloadError, YoutubeDL
from yt_dlp.utils import sanitize_filename
from pydantic_models.models import VideoModel
from utils.logger import logger

class TranscriptDownloader:
    def __init__(self, base_path: Path):
        self.base_path: Path = base_path
        self.video_download_path: Path = base_path / "videos"
        self.transcript_download_path: Path = base_path / "transcripts"

        # Create directories if they don't exist
        self.video_download_path.mkdir(parents=True, exist_ok=True)
        self.transcript_download_path.mkdir(parents=True, exist_ok=True)

    def download_transcript_with_video(self, youtube_url: str) -> VideoModel:
        """
        Downloads the transcript and video of a YouTube video.

        Args:
            youtube_url (str): The URL of the YouTube video

        Returns:
            VideoData: The downloaded video details
        """
        logger.info(f"Checking for transcript availability: {youtube_url}")

        # Step 1: Check for transcript availability
        ydl_opts_check = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

        try:
            with YoutubeDL(ydl_opts_check) as ydl:
                info_dict = ydl.extract_info(youtube_url, download=False)

                # Check if subtitles or automatic captions are available
                if not info_dict.get("subtitles") and not info_dict.get("automatic_captions"):
                    logger.info("No transcript available. Skipping download.")
                    return None
        
                logger.info("Transcript available. Proceeding with download.")

                # Prepare filenames
                sanitized_title = sanitize_filename(info_dict["title"], restricted=True)
                video_id = info_dict["id"]
                base_filename = f"{sanitized_title}_{video_id}"
                
                # Define paths
                video_path = self.video_download_path / f"{base_filename}.mp4"
                transcript_path = self.transcript_download_path / f"{base_filename}.vtt"

        except DownloadError as e:
            logger.error(f"Error during transcript check: {e}")
            raise

        # Step 2: Download video
        ydl_opts_download = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": {
                "default": f"{self.video_download_path}/%(title)s_%(id)s.%(ext)s",
                "subtitle": f"{self.transcript_download_path}/%(title)s_%(id)s.en.vtt",
            },
            "writesubtitles": True,  # Download subtitles if available
            "writeautomaticsub": True,  # Download automatic captions if available
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "restrictfilenames": True,
            "merge_output_format": "mp4",
            "quiet": True,
        }

        try:
            with YoutubeDL(ydl_opts_download) as ydl:
                info_dict = ydl.extract_info(youtube_url, download=True)

                logger.info(f"Downloaded {info_dict['title']}")
                logger.info(f"Video path: {video_path}")
                logger.info(f"Transcript path: {transcript_path}")
                logger.info(f"Video ID: {info_dict['id']}")
                logger.info(f"Video URL: {info_dict['webpage_url']}")
                logger.info(f"Title: {info_dict['title']}")
                logger.info(f"Description: {info_dict['description']}")

                return VideoModel(
                    id=info_dict['id'],
                    video_url=info_dict['webpage_url'],
                    title=info_dict['title'],
                    video_path=str(video_path),
                    transcript_path_vtt=str(transcript_path),
                )
        except DownloadError as e:
            logger.error(f"Error during video download: {e}")
            raise

if __name__ == "__main__":
    downloader = TranscriptDownloader(Path("data/raw"))
    downloader.download_transcript_with_video("https://www.youtube.com/watch?v=SYQk0wj0hE0")
