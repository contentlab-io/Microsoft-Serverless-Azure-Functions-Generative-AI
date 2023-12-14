import requests

def send_request(text, history, url="http://localhost:7071/api/NewsSummarizer"):
    """Send a request to the Azure Function."""
    headers = {'Content-Type': 'application/json'}
    data = {'text': text, 'conversation_history': history}
    response = requests.post(url, headers=headers, json=data)
    return response.text  # Receive plain text response

def main():
    print("Chatbot Tester. Type 'quit' to exit.")
    conversation_history = []  # Initialize conversation history

    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            break

        print()  # Newline after user input for readability

        assistant_response = send_request(user_input, conversation_history)
        print("Assistant:", assistant_response)

        print()  # Newline after AI response for readability

        # Update conversation history, keeping only the last 5 interactions
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": assistant_response})
        conversation_history = conversation_history[-10:]  # Keep only last 5 pairs of interactions

if __name__ == "__main__":
    main()
