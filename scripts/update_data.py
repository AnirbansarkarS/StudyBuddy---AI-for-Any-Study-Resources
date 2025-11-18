import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scraper import GitHubScraper
from core.vectorstore import VectorStoreManager
import shutil

def main():
    print("🔄 Updating resource database...\n")
    
    # Backup old vectorstore
    if os.path.exists("./data/vectorstore"):
        shutil.move("./data/vectorstore", "./data/vectorstore_backup")
    
    # Scrape fresh data
    scraper = GitHubScraper()
    df = scraper.scrape_all_repos()
    scraper.save_to_csv(df, "./data/raw/resources.csv")
    
    # Rebuild vectorstore
    vectorstore_manager = VectorStoreManager()
    vectorstore_manager.build_vectorstore(df)
    
    print("\n✅ Database updated successfully!")

if __name__ == "__main__":
    main()