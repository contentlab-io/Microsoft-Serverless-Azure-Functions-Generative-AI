import logging
import azure.functions as func

from .news_processing import get_random_article, summarize_news


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    dataset_file_path = 'NewsSummarizer/train.csv'  # Adjust as needed
    selected_article = get_random_article(dataset_file_path)

    if selected_article:
        summary = summarize_news(selected_article)
        return func.HttpResponse(summary, status_code=200)
    else:
        return func.HttpResponse("No news article available for summarization.", status_code=200)
