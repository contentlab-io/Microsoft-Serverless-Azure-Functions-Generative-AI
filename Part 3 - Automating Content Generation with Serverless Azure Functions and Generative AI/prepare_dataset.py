import csv
import json
import random

# Define the path to your CSV file
csv_file_path = 'train.csv'

# Open and read the CSV file
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    
    # Assuming 'article' and 'highlights' are column names
    articles = [{'article': row['article'], 'highlights': row['highlights']} for row in reader]

# Sample a subset of articles if the dataset is too large
sample_size = int(0.01 * len(articles))  # Adjust this to get a file size under 100 MB
sampled_articles = random.sample(articles, sample_size)

# Convert to JSONL with an improved prompt for summarization
with open('train.jsonl', 'w', encoding='utf-8') as jsonl_file:
    for article in sampled_articles:
        data = {
            "prompt": "Summarize this article: " + article['article'],
            "completion": article['highlights']
        }
        jsonl_file.write(json.dumps(data) + '\n')

print("File conversion complete.")