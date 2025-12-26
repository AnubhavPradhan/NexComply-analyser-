"""
Embeddings utility module.

Provides functions for generating and managing embeddings for documents.
"""
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger


class EmbeddingGenerator:
    """
    Generate embeddings for text documents using sentence transformers.
    
    Attributes:
        model: The sentence transformer model for generating embeddings.
        model_name: Name of the embedding model.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model to use.
        """
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully")
    
    def generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text documents to embed.
            batch_size: Number of texts to process in each batch.
            show_progress: Whether to show progress bar.
            
        Returns:
            np.ndarray: Array of embeddings with shape (n_texts, embedding_dim).
        """
        if not texts:
            logger.warning("Empty text list provided for embedding generation")
            return np.array([])
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text document to embed.
            
        Returns:
            np.ndarray: Embedding vector.
        """
        return self.generate_embeddings([text], batch_size=1, show_progress=False)[0]
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings.
        
        Returns:
            int: Dimension of the embedding vectors.
        """
        return self.model.get_sentence_embedding_dimension()
