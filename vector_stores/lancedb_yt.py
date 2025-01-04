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
            if self.table_name not in self.connection.table_names():
                logger.info(f"Creating new table: {self.table_name}")
                self.table = self.connection.create_table(
                    self.table_name,
                    schema=schema,
                    mode="create"
                )
                
                # Add initial data if provided
                if video_segments:
                    self.add_video_segments(video_segments)
            else:
                logger.info(f"Using existing table: {self.table_name}")
                self.table = self.connection.open_table(self.table_name)
                
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise
    
    def add_video_segments(self, video_segments: List[VideoSegmentModel]) -> None:
        """Add video segments to the table.
        
        Args:
            video_segments: List of video segment models to add
        """
        try:
            if not self.table:
                raise ValueError("Table not initialized. Call create_video_segments_table first.")
            
            # Convert models to dictionaries
            records = [segment.model_dump() for segment in video_segments]
            
            # Add to table
            self.table.add(records)
            logger.info(f"Added {len(records)} video segments to table")
            
        except Exception as e:
            logger.error(f"Error adding video segments: {e}")
            raise
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter_condition: Optional[str] = None
    ) -> List[tuple[Document, float]]:
        """Search for similar video segments.
        
        Args:
            query: Query text
            k: Number of results
            filter_condition: SQL-style filter condition
            
        Returns:
            List of (document, score) tuples
        """
        try:
            # Get embeddings for query
            query_embedding = self.embedding.embed_query(query)
            
            # Build search query
            search_query = self.table.search(query_embedding)
            if filter_condition:
                search_query = search_query.filter(filter_condition)
            
            # Execute search
            results = search_query.limit(k).to_list()
            
            # Convert to documents
            docs_and_scores = []
            for result in results:
                # Create metadata
                metadata = {
                    "video_segment_id": result["id"],
                    "parent_video_id": result["parent_video_id"],
                    "start_ms": result["start_ms"],
                    "end_ms": result["end_ms"],
                    "frame_path": result["frame_path"],
                    "video_segment_path": result["video_segment_path"]
                }
                
                # Create document
                doc = Document(
                    page_content=result[self.text_key],
                    metadata=metadata
                )
                
                docs_and_scores.append((doc, result["_distance"]))
                
            return docs_and_scores
            
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            raise
