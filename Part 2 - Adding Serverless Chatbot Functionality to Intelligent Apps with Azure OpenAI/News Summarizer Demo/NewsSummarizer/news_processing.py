import csv
import random
from .openai_client import client

def get_random_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        articles = [row['article'] for row in reader]
    return random.choice(articles)

def summarize_news(text):
    max_length = 2000
    truncated_text = text[:max_length]

    response = client.completions.create(
        model="NewsSummarizer",
        prompt=f"Summarize the key points of the following news article in a concise and coherent manner: \n\n{truncated_text}\n\n",
        temperature=0.3,
        max_tokens=250,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        best_of=3,
        stop=["\n"]
    )
    return response.choices[0].text.strip()
