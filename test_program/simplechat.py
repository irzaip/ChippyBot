import random

# Define the responses for the chatbot
responses = {
    "hello": ["Hi there!", "Hello!", "Greetings!"],
    "how are you": ["I'm doing well, thanks for asking.", "Not too bad, thanks.", "I'm fine, how are you?"],
    "what's your name": ["My name is ChatBot.", "I go by the name ChatBot.", "People call me ChatBot."],
    "default": ["Sorry, I don't understand. Can you please rephrase your question?", "I'm not sure what you're asking. Can you please clarify?", "I don't know the answer. Can we talk about something else?"]
}

# Define a function to generate the chatbot's response
def generate_response(user_input):
    # Convert user input to lowercase
    user_input = user_input.lower()
    
    # Check if user input is a key in the responses dictionary
    if user_input in responses:
        return random.choice(responses[user_input])
    else:
        return random.choice(responses["default"])

# Define a function to run the chatbot
def run_chatbot():
    print("Hi, I'm ChatBot. How can I help you today?")
    
    # Loop through the conversation until the user types "bye"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("ChatBot: Goodbye! Have a nice day.")
            break
        else:
            response = generate_response(user_input)
            print("ChatBot:", response)

# Call the run_chatbot function to start the chatbot
run_chatbot()