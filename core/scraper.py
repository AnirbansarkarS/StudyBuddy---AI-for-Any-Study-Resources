import requests
import re
from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd
from github import Github
from app.config import settings

class GitHubScraper:
    def __init__(self, github_token: str = None):
        self.github_token = github_token or settings.github_token
        self.gh = Github(self.github_token) if self.github_token else None
    
    def fetch_raw_content(self, repo: str, file_path: str) -> str:
        """Fetch raw file content from GitHub"""
        url = f"https://raw.githubusercontent.com/{repo}/main/{file_path}"
        
        # Try 'main' branch first, then 'master'
        response = requests.get(url)
        if response.status_code == 404:
            url = url.replace('/main/', '/master/')
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"❌ Failed to fetch {repo}/{file_path}")
            return ""
    
    def parse_markdown_links(self, content: str, repo: str) -> List[Dict]:
        """Extract resources from markdown content"""
        lines = content.split('\n')
        resources = []
        current_topic = "General"
        current_subtopic = None
        
        for line in lines:
            # Detect main topics (## Header)
            if line.startswith('## '):
                current_topic = line.replace('## ', '').strip()
                current_topic = re.sub(r'[#*`]', '', current_topic)
                current_subtopic = None
            
            # Detect subtopics (### Header)
            elif line.startswith('### '):
                current_subtopic = line.replace('### ', '').strip()
                current_subtopic = re.sub(r'[#*`]', '', current_subtopic)
            
            # Extract links [text](url)
            if '[' in line and '](' in line:
                matches = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', line)
                for name, url in matches:
                    # Skip internal links
                    if url.startswith('#'):
                        continue
                    
                    # Extract description (text after link)
                    description = ""
                    if ' - ' in line:
                        parts = line.split(' - ', 1)
                        if len(parts) > 1:
                            description = parts[1].strip()
                            description = re.sub(r'\[.*?\]\(.*?\)', '', description)
                    
                    # Determine platform
                    platform = "Website"
                    if 'youtube.com' in url or 'youtu.be' in url:
                        platform = "YouTube"
                    elif 'github.com' in url:
                        platform = "GitHub"
                    elif 'coursera.org' in url:
                        platform = "Coursera"
                    elif 'udemy.com' in url:
                        platform = "Udemy"
                    
                    resources.append({
                        'source_repo': repo,
                        'topic': current_topic,
                        'subtopic': current_subtopic or current_topic,
                        'name': name.strip(),
                        'url': url.strip(),
                        'description': description.strip(),
                        'platform': platform
                    })
        
        return resources
    
    def scrape_all_repos(self) -> pd.DataFrame:
        """Scrape all configured GitHub repos"""
        all_resources = []
        
        for repo, files in settings.target_files.items():
            print(f"📥 Scraping {repo}...")
            
            for file_path in files:
                print(f"  └─ {file_path}")
                content = self.fetch_raw_content(repo, file_path)
                
                if content:
                    resources = self.parse_markdown_links(content, repo)
                    all_resources.extend(resources)
                    print(f"     ✅ Found {len(resources)} resources")
        
        df = pd.DataFrame(all_resources)
        print(f"\n🎉 Total resources scraped: {len(df)}")
        return df
    
    def save_to_csv(self, df: pd.DataFrame, output_path: str = "./data/raw/resources.csv"):
        """Save scraped data to CSV"""
        df.to_csv(output_path, index=False)
        print(f"💾 Saved to {output_path}")