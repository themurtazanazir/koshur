import requests
from bs4 import BeautifulSoup
import random


def get_simple_wikipedia_articles(num_articles=50):
    url = "https://simple.wikipedia.org/wiki/Special:Random"
    articles = []
    total_chars = 0
    char_limit = 500000

    for _ in range(num_articles):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the article title
        title = soup.find(id="firstHeading").text

        # Get the article content
        content = soup.find(id="mw-content-text")
        paragraphs = content.find_all("p")

        article_text = f"Title: {title}\n\n"
        for p in paragraphs:
            article_text += p.text + "\n"

        # Check if we're within the character limit
        if total_chars + len(article_text) > char_limit:
            break

        articles.append(article_text)
        total_chars += len(article_text)
        print(f"Collected article: {title} ({len(article_text)} characters)")
        print(f"Total characters so far: {total_chars}")

    return articles, total_chars


# Gather articles
articles, total_chars = get_simple_wikipedia_articles()

# Combine all articles into one text
all_text = "\n\n".join(articles)

# Save the text to a file
with open("simple_english_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"\nTotal articles collected: {len(articles)}")
print(f"Total characters: {total_chars}")
print("Text saved to simple_english_text.txt")
