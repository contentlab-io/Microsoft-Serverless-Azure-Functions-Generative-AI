import logging
import azure.functions as func

from .news_processing import get_random_article, summarize_news
from .chatbot import determine_intent, handle_followup_question, handle_custom_summary_request, generate_content

def main(req: func.HttpRequest) -> func.HttpResponse:
    dataset_file_path = 'NewsSummarizer/test.csv'
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    user_input = req_body.get('text')
    conversation_history = req_body.get('conversation_history', [])[-5:] 

    if not user_input:
        try:
            req_body = req.get_json()
            user_input = req_body.get('text')
        except ValueError:
            pass

    if not user_input:
        return func.HttpResponse("Please provide some input.", status_code=400)

    intent, conversation_history = determine_intent(user_input, conversation_history)

    if intent == "Ask for news summary":
        selected_article = get_random_article(dataset_file_path)
        response_text = summarize_news(selected_article)
    elif intent in ["Query about a specific news detail", "General inquiry"]:
        response_text, conversation_history = handle_followup_question(conversation_history, user_input)
    elif intent == "Set a parameter for news summary":
        selected_article = get_random_article(dataset_file_path)
        response_text, conversation_history = handle_custom_summary_request(user_input, selected_article, conversation_history)
    elif intent == "Generate content":
        if conversation_history:
            response_text = generate_content(conversation_history, user_input)
        else:
            response_text = "No recent summary available for content generation."
    else:
        response_text = "Sorry, I didn't understand that."

    # Update conversation history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "system", "content": response_text})

    return func.HttpResponse(response_text, status_code=200)