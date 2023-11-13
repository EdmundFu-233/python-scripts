"""Simple HTML to Markdown converter"""
import re
from html.parser import HTMLParser

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_code = False
        self.in_list = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3', 'h4'): self.result.append('#' * int(tag[1]) + ' ')
        elif tag == 'strong': self.result.append('**')
        elif tag == 'em': self.result.append('*')
        elif tag == 'code': self.result.append('`')
        elif tag == 'li': self.result.append('- ')
        elif tag == 'br': self.result.append('\n')
        elif tag == 'hr': self.result.append('\n---\n')
    
    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'p', 'li'): self.result.append('\n')
        elif tag == 'strong': self.result.append('**')
        elif tag == 'em': self.result.append('*')
        elif tag == 'code': self.result.append('`')
    
    def handle_data(self, data):
        self.result.append(data)
    
    def convert(self, html: str) -> str:
        self.feed(html)
        return ''.join(self.result).strip()

if __name__ == "__main__":
    converter = HTMLToMarkdown()
    html = "<h1>Hello</h1><p>This is <strong>bold</strong> text</p>"
    print(converter.convert(html))
