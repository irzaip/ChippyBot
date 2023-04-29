import re

#text = "This is the first sentence. This is the second sentence. This is the third sentence."
text = ""

with open('ayahku.txt', 'r') as file:
    # Read the contents of the file into a variable
    text = file.readlines()

text = ' '.join(str(e) for e in text)

def get_only_first_word_count(input, word_count=500):
    #sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', input)
    sentences = re.split(r'(?<=[^.?!]) +(?=[a-zA-Z])', input)

    max_word_count = word_count
    current_word_count = 0
    index = 0

    for sentence in sentences:
        words = sentence.split()
        word_count = len(words)
        if current_word_count + word_count <= max_word_count:
            current_word_count += word_count
            index += 1
        else:
            break
    
    print(index)
    return sentences[0:index], sentences[index:]


a,b = get_only_first_word_count(input=text, word_count=500)

print("A:",a)
print(" --------------------------------")
print("B:", b)