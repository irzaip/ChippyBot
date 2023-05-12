from conversations import BotQuestion
import itertools


all_quest = []
all_quest.append(BotQuestion(1,"Siapakah presiden pertama?"))
all_quest.append(BotQuestion(2,"Siapakah presiden ke 2?"))
all_quest.append(BotQuestion(3,"siapakah presiden ke 3?"))

aq = iter(all_quest)

for i in aq:
    if not i.answer:
        print(i.question)
        i.answer = input(":")
        break

