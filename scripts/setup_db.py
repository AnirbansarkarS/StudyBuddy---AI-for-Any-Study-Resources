import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scraper import GitHubScraper
from core.vectorstore import VectorStoreManager

def main():
    print("🚀 Starting database setup...\n")
    
    # Step 1: Scrape GitHub repos
    scraper = GitHubScraper()
    df = scraper.scrape_all_repos()
    
    # Save raw data
    os.makedirs("./data/raw", exist_ok=True)
    scraper.save_to_csv(df, "./data/raw/resources.csv")
    
    # Step 2: Build vector store
    vectorstore_manager = VectorStoreManager()
    vectorstore_manager.build_vectorstore(df)
    
    print("\n✅ Database setup complete!")
    print(f"📊 Total resources indexed: {len(df)}")

if __name__ == "__main__":
    main()