"""Simple RSS feed reader"""
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

class RSSReader:
    def __init__(self, url: str):
        self.url = url
        self.items = []
    
    def fetch(self):
        resp = requests.get(self.url)
        root = ET.fromstring(resp.content)
        channel = root.find('channel')
        for item in channel.findall('item'):
            self.items.append({
                'title': item.findtext('title', ''),
                'link': item.findtext('link', ''),
                'description': item.findtext('description', ''),
                'pub_date': item.findtext('pubDate', ''),
            })
        return self.items
    
    def display(self, limit: int = 5):
        for item in self.items[:limit]:
            print(f"\n{item['title']}")
            print(f"  {item['link']}")

if __name__ == "__main__":
    reader = RSSReader("https://news.ycombinator.com/rss")
    reader.fetch()
    reader.display()
