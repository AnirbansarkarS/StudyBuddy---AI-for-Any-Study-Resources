from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever
from core.vectorstore import vectorstore_manager
from typing import List, Dict

class ResourceRecommender:
    def __init__(self):
        self.vectorstore = vectorstore_manager.vectorstore
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )
    
    def search_resources(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for resources using vector similarity"""
        results = self.vectorstore.similarity_search(query, k=top_k)
        
        resources = []
        for doc in results:
            resources.append({
                'name': doc.metadata['name'],
                'topic': doc.metadata['topic'],
                'subtopic': doc.metadata['subtopic'],
                'url': doc.metadata['url'],
                'platform': doc.metadata['platform'],
                'description': doc.metadata['description'],
                'source_repo': doc.metadata['source_repo']
            })
        
        return resources
    
    def search_by_topic(self, topic: str, top_k: int = 10) -> List[Dict]:
        """Search resources by specific topic"""
        results = self.vectorstore.similarity_search(
            f"Topic: {topic}",
            k=top_k
        )
        
        resources = []
        seen_urls = set()
        
        for doc in results:
            url = doc.metadata['url']
            if url not in seen_urls:
                seen_urls.add(url)
                resources.append({
                    'name': doc.metadata['name'],
                    'topic': doc.metadata['topic'],
                    'subtopic': doc.metadata['subtopic'],
                    'url': doc.metadata['url'],
                    'platform': doc.metadata['platform'],
                    'description': doc.metadata['description']
                })
        
        return resources
    
    def search_by_platform(self, platform: str, query: str = "", top_k: int = 5) -> List[Dict]:
        """Filter resources by platform (YouTube, GitHub, etc.)"""
        search_query = f"{query} Platform: {platform}" if query else f"Platform: {platform}"
        results = self.vectorstore.similarity_search(search_query, k=top_k * 2)
        
        resources = []
        for doc in results:
            if doc.metadata['platform'].lower() == platform.lower():
                resources.append({
                    'name': doc.metadata['name'],
                    'topic': doc.metadata['topic'],
                    'url': doc.metadata['url'],
                    'platform': doc.metadata['platform'],
                    'description': doc.metadata['description']
                })
                
                if len(resources) >= top_k:
                    break
        
        return resources

recommender = ResourceRecommender()