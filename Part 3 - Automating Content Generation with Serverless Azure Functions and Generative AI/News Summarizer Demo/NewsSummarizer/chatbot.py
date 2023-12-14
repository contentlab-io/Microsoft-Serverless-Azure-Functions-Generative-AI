from .openai_client import client

def determine_intent(user_input, conversation_history=None):
    system_message = "You are a helpful assistant who can categorize the user's intent based on their input. Based on the following user input, determine if the user is trying to: 1. Ask for a news summary, 2. Query about a specific news detail, 3. Set a parameter for news summary, or 4. Generate content based on the summary.?"

    messages = conversation_history if conversation_history else []
    messages.extend([
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ])

    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages
    )

    descriptive_intent = response.choices[0].message.content
    categorized_intent = categorize_intent(descriptive_intent)
    return categorized_intent, messages

def categorize_intent(descriptive_intent):
    CUSTOMIZATION_KEYWORDS = ["short", "long", "brief", "detailed", "start with", "end with", "focus on"]
    CONTENT_GEN_KEYWORDS = ["write", "report", "aggregate", "action", "track", "event", "analyze", "insights"]

    if "news summary" in descriptive_intent.lower():
        return "Ask for news summary"
    elif "specific news detail" in descriptive_intent.lower() or "question" in descriptive_intent.lower():
        return "Query about a specific news detail"
    elif any(keyword in descriptive_intent.lower() for keyword in CUSTOMIZATION_KEYWORDS):
        return "Set a parameter for news summary"
    elif any(keyword in descriptive_intent.lower() for keyword in CONTENT_GEN_KEYWORDS):
        return "Generate content"
    else:
        return "General inquiry"

def handle_followup_question(conversation_history, followup_question):
    # Construct a more directive system message
    system_message = "Based on the summarized article in the conversation history, directly answer the user's follow-up question."

    # Insert the follow-up question into the conversation history
    messages = conversation_history + [
        {"role": "system", "content": system_message},
        {"role": "user", "content": followup_question}
    ]

    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages
    )

    # Extract the model's response
    answer = response.choices[0].message.content
    return answer, conversation_history


def handle_custom_summary_request(user_input, article_text, conversation_history):
    # Construct a prompt for Davinci using the user's instructions and the article text
    prompt_for_davinci = f"Based on the following user instructions: '{user_input}', please generate a summary of the article below:\n\n{article_text}"

    # Call to Davinci model for summarization
    davinci_response = client.completions.create(
        model="NewsSummarizer",
        prompt=prompt_for_davinci,
        max_tokens=250  # Adjust based on your requirements
    )

    custom_summary = davinci_response.choices[0].text.strip()

    # Integrate the Davinci summary back into the conversation history for continuity
    system_summary_message = f"Here is a custom summary based on your instructions:\n{custom_summary}"
    conversation_history.append({"role": "system", "content": system_summary_message})

    return custom_summary, conversation_history

def generate_content(conversation_history, user_query):
    # Construct a summary of the recent conversation
    conversation_summary = " ".join([f"{entry['role']} says: {entry['content']}" for entry in conversation_history[-10:]])

    # Craft a prompt that combines the recent conversation and user query
    prompt = f"Based on the recent conversation: '{conversation_summary}', generate content that addresses the following user query: '{user_query}'. The content should be informative, relevant to the query, and make use of the information in the conversation."

    # Call to your custom model for content generation
    response = client.completions.create(
        model="CustomNewsSummary",
        prompt=prompt,
        max_tokens=500,
        top_p=1,
        frequency_penalty=1,
        best_of=3,
        stop=["\n"]
    )

    generated_content = response.choices[0].text.strip()
    return generated_content