#Rembember to install beautifulsoup
#pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import json

class WebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_links = set()
        self.links = []
        self.images = []

    def get_page_content(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def extract_links_and_images(self, html_content):
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                self.links.append(link['href'])
            for img in soup.find_all('img', src=True):
                self.images.append(img['src'])

    def crawl_page(self, url):
        if url not in self.visited_links:
            print(f"Crawling: {url}")
            html_content = self.get_page_content(url)
            if html_content:
                self.extract_links_and_images(html_content)
                self.visited_links.add(url)

    def save_results_to_json(self):
        results = {
            "links": list(set(self.links)),
            "images": list(set(self.images))
        }
        with open("index.json", "w") as index_file:
            json.dump(results, index_file, indent=2)
        print("Results saved to index.json")

    def crawl_site(self, max_pages=10):
        queue = [self.base_url]

        while queue and len(self.visited_links) < max_pages:
            current_url = queue.pop(0)
            self.crawl_page(current_url)

            # Extract links from the current page and add them to the queue
            html_content = self.get_page_content(current_url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_url = link['href']
                    if absolute_url.startswith(self.base_url) and absolute_url not in self.visited_links:
                        queue.append(absolute_url)

        self.save_results_to_json()

if __name__ == '__main__':
    # Replace 'https://example.com' with the target website URL
    base_url = input("Enter the website URL: ")
    
    # Create an instance of WebCrawler and crawl the site (adjust max_pages as needed)
    web_crawler = WebCrawler(base_url)
    web_crawler.crawl_site(max_pages=10)
