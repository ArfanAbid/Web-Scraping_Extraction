# Scraping Medium Articles by reading CSV having URLs and then storing different parameters in different columns.
  
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = pd.read_csv("/url_technology.csv")
data.columns = ["urls"]

titles = []
subtitles = []
articles = []
authors = []
author_urls = []
claps = []
reading_times = []
image_sources = []
scraped_urls = []

# Number of URLs to Scrape
num_urls = 500

for i in range(num_urls):
    try:
        url_to_scrap = data.iloc[i]["urls"]
        print(f"Scraping {i+1}/{num_urls}: {url_to_scrap}")

        # Request the page
        response = requests.get(url_to_scrap, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url_to_scrap}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.find("h1").text.strip() if soup.find("h1") else "N/A"

        # Extract multiple subtitles
        subtitle_tags = soup.find_all("h2")  
        subtitles_list = [st.text.strip() for st in subtitle_tags]
        subtitle = ", ".join(subtitles_list) if subtitles_list else "N/A"

        # Extract article content
        article = " ".join([p.text.strip() for p in soup.find_all("p")])

        # Extract author name
        author_tag = soup.find("meta", {"name": "author"})
        author = author_tag["content"] if author_tag else "N/A"

        # Extract author profile URL 
        author_url_tag = soup.find("a", {"class": "ds-link", "href": True})
        author_url = author_url_tag["href"] if author_url_tag else "N/A"

        # Extract number of claps 
        claps_tag = soup.find("button", {"data-test-id": "clap-count"})
        claps_count = claps_tag.text.strip() if claps_tag else "0"

        # Extract reading time 
        reading_time_tag = soup.find("span", {"class": "readingTime"})
        reading_time = reading_time_tag["title"] if reading_time_tag else "N/A"

        # Extract multiple image sources 
        images = []
        for img in soup.find_all("img"):
            img_src = img.get("src") or img.get("data-src")  # Try 'src', then 'data-src'
            if img_src:
                images.append(img_src)
        images_str = ", ".join(images) if images else "N/A"

        # Append data to lists
        titles.append(title)
        subtitles.append(subtitle)
        articles.append(article)
        authors.append(author)
        author_urls.append(author_url)
        claps.append(claps_count)
        reading_times.append(reading_time)
        image_sources.append(images_str)
        scraped_urls.append(url_to_scrap)

        # Delay to avoid rate-limiting by Medium
        time.sleep(2)

    except Exception as e:
        print(f"Error scraping {url_to_scrap}: {e}")

# Create DataFrame
scraped_data = pd.DataFrame({
    "URL": scraped_urls,
    "Title": titles,
    "Subtitles": subtitles,
    "Article": articles,
    "Author": authors,
    "Author URL": author_urls,
    "Claps": claps,
    "Reading Time": reading_times,
    "Image Sources": image_sources
})

# Save to CSV
scraped_data.to_csv("medium_scraped_articles.csv", index=False, encoding="utf-8")
print("Scraping completed! Data saved in medium_scraped_articles.csv.")
