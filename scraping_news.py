import requests
from bs4 import BeautifulSoup
import os
import re

base_url = "https://iisia.or.id"
list_url = "https://iisia.or.id/news?page="
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.46'
}

output_dir = "News"
scraped_links_file = "scraped_links.txt"

os.makedirs(output_dir, exist_ok=True)

def get_soup(url):
    response = requests.get(url, headers=headers, verify=True)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

def get_post_description(url):
    try:
        soup = get_soup(url)
        article_tag = soup.find('article')
        if article_tag:
            text_parts = []
            for elem in article_tag.find_all(['p', 'br']):
                if elem.name == 'p':
                    text_parts.append(elem.get_text(strip=True))
                elif elem.name == 'br':
                    text_parts.append('')
            return '\n'.join(text_parts)
        return ""
    except Exception as e:
        print(f"Failed to retrieve description: {e}")
        return ""

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

if os.path.exists(scraped_links_file):
    with open(scraped_links_file, 'r') as f:
        scraped_links = set(line.strip() for line in f)
else:
    scraped_links = set()

new_links_found = False

for page_num in range(1, 2):
    print(f"Checking page {page_num}")
    soup = get_soup(f"{list_url}{page_num}")
    posts = soup.find_all('div', class_='box-post')

    for post in posts:
        title_tag = post.find('h4')
        link_tag = post.find('div', href=True)

        if not (title_tag and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag['href']

        full_url = link if link.startswith("http") else base_url + link

        if full_url in scraped_links:
            print(f"Already scraped: {full_url}")
            continue

        print(f"Scraping new article: {title}")
        content = get_post_description(full_url)

        safe_title = sanitize_filename(title)
        txt_path = os.path.join(output_dir, f"{safe_title}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{content}")

        scraped_links.add(full_url)
        new_links_found = True

if new_links_found:
    with open(scraped_links_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(scraped_links))

print("Check completed.")
