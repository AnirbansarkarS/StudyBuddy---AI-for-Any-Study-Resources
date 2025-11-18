from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Optional

class EmbeddingManager:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._embeddings = None
    
    @property
    def embeddings(self):
        """Lazy load embeddings"""
        if self._embeddings is None:
            print(f"🔄 Loading embedding model: {self.model_name}")
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("✅ Embedding model loaded")
        return self._embeddings

embedding_manager = EmbeddingManager()