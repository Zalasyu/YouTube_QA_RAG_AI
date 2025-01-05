from typing import Any, List, Optional, Union
from pathlib import Path

import lancedb
from lancedb.pydantic import pydantic_to_schema
from langchain_community.vectorstores.lancedb import LanceDB
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from pydantic_models.models import VideoSegmentModel
from utils.logger import logger


class LanceDBYT(LanceDB):
    """LanceDB vector store for video segments with LangChain integration."""
    
    def __init__(
        self,
        connection: Optional[Any] = None,
        embedding: Optional[Embeddings] = None,
        uri: Optional[str] = "/data/multimodal_lancedb",
        vector_key: str = "embeddings",
        id_key: str = "video_segment_id",
        text_key: str = "enriched_transcript",
        table_name: str = "video_segments",
    ) -> None:
        """Initialize LanceDB vector store.
        
        Args:
            connection: LanceDB connection
            embedding: LangChain embedding function
            uri: Path to LanceDB database
            vector_key: Name of vector column
            id_key: Name of ID column
            text_key: Name of text column
            table_name: Name of table
        """
        if connection is None:
            connection = lancedb.connect(uri)
        
        super().__init__(
            connection=connection,
            embedding=embedding,
            vector_key=vector_key,
            id_key=id_key,
            text_key=text_key,
            table_name=table_name,
        )
        
        self.table = None
    
    def create_video_segments_table(self, video_segments: List[VideoSegmentModel]) -> None:
        """Create table for video segments if it doesn't exist.
        
        Args:
            video_segments: List of video segment models to initialize table with
        """
        try:
            # Create schema from Pydantic model
            schema = pydantic_to_schema(VideoSegmentModel)
            
            # Create table if it doesn't exist
            if self._table_name not in self._connection.table_names():
                logger.info(f"Creating new table: {self._table_name}")
                self.table = self._connection.create_table(
                    self._table_name,
                    schema=schema,
                    mode="overwrite"
                )
                logger.info(f"Table created: {self.table}")
                
                # Add initial data if provided
                if video_segments:
                    self.add_video_segments(video_segments)
            else:
                logger.info(f"Using existing table: {self._table_name}")
                self.table = self._connection.open_table(self._table_name)

            return self.table
                
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise
    
    def add_video_segments(self, video_segments: List[VideoSegmentModel]) -> None:
        """Add video segments to the table.
        
        Args:
            video_segments: List of video segment models to add
        """
        try:
            logger.info(f"Adding {len(video_segments)} video segments to table: {self.table}")
            
            # Convert models to dictionaries
            records = [segment.model_dump() for segment in video_segments]
            
            # Add to table
            self.table.add(records)
            logger.info(f"Added {len(records)} video segments to table")

            return self.table
            
        except Exception as e:
            logger.error(f"Error adding video segments: {e}")
            raise

        