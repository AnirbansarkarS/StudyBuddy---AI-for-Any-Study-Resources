from pydantic import BaseModel, Field
from typing import List, Optional

class ResourceQuery(BaseModel):
    query: str = Field(..., description="Search query (e.g., 'cybersecurity', 'machine learning')")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")

class TopicQuery(BaseModel):
    topic: str = Field(..., description="Specific topic to search")
    top_k: int = Field(10, ge=1, le=50)

class PlatformQuery(BaseModel):
    platform: str = Field(..., description="Platform filter (YouTube, GitHub, Website, etc.)")
    query: Optional[str] = Field("", description="Optional search query")
    top_k: int = Field(5, ge=1, le=20)

class Resource(BaseModel):
    name: str
    topic: str
    subtopic: str
    url: str
    platform: str
    description: str
    source_repo: Optional[str] = None

class ResourceResponse(BaseModel):
    query: str
    total_results: int
    resources: List[Resource]