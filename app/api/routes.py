from fastapi import APIRouter, HTTPException
from app.models import ResourceQuery, TopicQuery, PlatformQuery, ResourceResponse, Resource
from core.chain import recommender

router = APIRouter()

@router.post("/search", response_model=ResourceResponse)
async def search_resources(query: ResourceQuery):
    """Search for learning resources"""
    try:
        results = recommender.search_resources(query.query, query.top_k)
        
        return ResourceResponse(
            query=query.query,
            total_results=len(results),
            resources=[Resource(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/topic", response_model=ResourceResponse)
async def search_by_topic(query: TopicQuery):
    """Search resources by specific topic"""
    try:
        results = recommender.search_by_topic(query.topic, query.top_k)
        
        return ResourceResponse(
            query=query.topic,
            total_results=len(results),
            resources=[Resource(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/platform", response_model=ResourceResponse)
async def search_by_platform(query: PlatformQuery):
    """Filter resources by platform"""
    try:
        results = recommender.search_by_platform(
            query.platform,
            query.query,
            query.top_k
        )
        
        return ResourceResponse(
            query=f"{query.query} on {query.platform}" if query.query else query.platform,
            total_results=len(results),
            resources=[Resource(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}