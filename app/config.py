from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Learning Resource API"
    app_version: str = "1.0.0"
    vector_db_path: str = "./data/vectorstore"
    openai_api_key: Optional[str] = None
    github_token: Optional[str] = None
    
    # GitHub repos to scrape
    github_repos: list = [
        "EbookFoundation/free-programming-books",
        "sindresorhus/awesome",
        "ossu/computer-science",
        "kamranahmedse/developer-roadmap",
        "jwasham/coding-interview-university",
    ]
    
    # Files to scrape from repos
    target_files: dict = {
        "EbookFoundation/free-programming-books": [
            "books/free-programming-books-subjects.md",
            "books/free-programming-books-langs.md",
        ],
        "sindresorhus/awesome": ["readme.md"],
        "ossu/computer-science": ["README.md"],
        "kamranahmedse/developer-roadmap": ["README.md"],
        "jwasham/coding-interview-university": ["README.md"],
    }
    
    class Config:
        env_file = ".env"

settings = Settings()