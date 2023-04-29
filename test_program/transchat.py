import torch
import transformers

# Load the pre-trained GPT-2 model
model_name = 'gpt2'
tokenizer = transformers.GPT2Tokenizer.from_pretrained(model_name)
model = transformers.GPT2LMHeadModel.from_pretrained(model_name)

# Set the device to GPU if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Set the maximum length of the input text and the number of responses to generate
max_length = 1024
num_responses = 1

def chatbot(text):
    # Encode the input text and add special tokens
    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')
    input_ids = input_ids.to(device)

    # Generate responses using the model
    output = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_return_sequences=num_responses
    )

    # Decode the generated responses and return them as a list
    responses = [tokenizer.decode(output[i], skip_special_tokens=True) for i in range(num_responses)]
    return responses

def run_chatbot():
    print("Hi, I'm ChatBot. How can I help you today?")
    
    # Loop through the conversation until the user types "bye"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("ChatBot: Goodbye! Have a nice day.")
            break
        else:
            response = chatbot(user_input)
            #response = generate_response(user_input)
            print("ChatBot:", response)

run_chatbot()