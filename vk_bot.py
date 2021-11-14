import json
import random


class VkBot:

    def __init__(self):
        pass

    def bot(self, question):

        with open('BOT_CONFIG.json', 'r', encoding='utf-8') as f:
            BOT_CONFIG = json.load(f)
        answer = []
        for intent in BOT_CONFIG['intents'].keys():
            for example in BOT_CONFIG['intents'][intent]['examples']:
                if example == question.lower():
                    answer.append(random.choice(BOT_CONFIG['intents'][intent]['responses']))
                    answer.append(intent)
                    return answer

        if len(answer) < 1:
            answer.append(random.choice(BOT_CONFIG['failure_phrases']))
            answer.append(None)
            return answer