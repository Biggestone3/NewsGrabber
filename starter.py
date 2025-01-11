from flask import Flask, render_template, request
import feedparser
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key="AIzaSyAguJg4_viVEz_d7tcLuWJiQ8RGHX-bYns")

app = Flask(__name__)

def summarize(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Please summarize the following text: {text}")
    return response.text

@app.route("/")
def home():
    feed_url = "https://www.aljazeera.com/rss"
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:5]:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": None,
        }

        response = requests.get(entry.link)
        soup = BeautifulSoup(response.text, "html.parser")
        article_content = soup.find("div", class_="wysiwyg wysiwyg--all-content")

        if article_content:
            text = article_content.get_text(strip=True, separator="\n")
            article["summary"] = summarize(text)
        else:
            article["summary"] = "No text associated with news article."

        articles.append(article)

    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
