from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pandas as pd
from typing import List
from core.embeddings import embedding_manager
from app.config import settings

class VectorStoreManager:
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or settings.vector_db_path
        self.embeddings = embedding_manager.embeddings
        self._vectorstore = None
    
    def create_documents(self, df: pd.DataFrame) -> List[Document]:
        """Convert DataFrame to LangChain Documents"""
        documents = []
        
        for _, row in df.iterrows():
            # Create rich text content
            content = f"""
Topic: {row['topic']}
Subtopic: {row['subtopic']}
Resource: {row['name']}
Description: {row['description']}
Platform: {row['platform']}
URL: {row['url']}
            """.strip()
            
            metadata = {
                'source_repo': row['source_repo'],
                'topic': row['topic'],
                'subtopic': row['subtopic'],
                'name': row['name'],
                'url': row['url'],
                'platform': row['platform'],
                'description': row['description']
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    
    def build_vectorstore(self, df: pd.DataFrame):
        """Build and persist vector store"""
        print("🔨 Building vector store...")
        
        documents = self.create_documents(df)
        print(f"📄 Created {len(documents)} documents")
        
        # Create vector store
        self._vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"✅ Vector store created at {self.persist_directory}")
        return self._vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store"""
        if self._vectorstore is None:
            print("📂 Loading vector store...")
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("✅ Vector store loaded")
        return self._vectorstore
    
    @property
    def vectorstore(self):
        """Get or load vector store"""
        if self._vectorstore is None:
            return self.load_vectorstore()
        return self._vectorstore

vectorstore_manager = VectorStoreManager()