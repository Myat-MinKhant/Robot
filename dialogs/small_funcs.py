from modules.global_vars import GLOBALS
import random

def introduce():
    return f"My name is {GLOBALS['bot_name']}. I am a humanoid robot. You can ask me anything!"

def greet():
    responses = ["Hey there!", "Hello!", "Hello there!", "Greetings!", "Hi"]
    return random.choice(responses)

def ask_about_day():
    responses = ["How was your day?", "Anything exciting happen today?", "Tell me about your day?", "How are you?", "How are you doing?"]
    return random.choice(responses)

def goodbye():
    responses = ["See you later!", "Until next time!", "Take care and see you later!", "Goodbye! Have a great day.", "Have a nice day!", "Well, good luck with the rest of your day."]
    return random.choice(responses)

def is_asking_suggest(command):
    keywords = ["recommend", "suggest", "help"]
    return any(keyword in command for keyword in keywords)

def is_positive_feedback(command):
    positive_keywords = ["thanks", "thank you", "appreciate it", "good", "great", "awesome", "fantastic", "amazing", "okay", "i will"]
    return any(keyword in command for keyword in positive_keywords)

def is_negative_feedback(command):
    negative_keywords = ["already seen", "don't like", "don't watch", "hate", "not a fan of", "another"]
    return any(keyword in command for keyword in negative_keywords)

def respond_to_city(city):
    if city == "yangon":
        return "Oh, Yangon! That's fascinating! I've heard it's a city with a rich cultural heritage."
    elif city == "korea":
        return "Nice! Korea, such a dynamic country! The blend of tradition and modernity is truly impressive."
    elif city == "japan":
        return "I love Japan! Your country's unique blend of tradition and technology has always left me in awe."
    elif city == "india":
        return "India is so diverse! What region are you from, and can you share some interesting aspects of your culture?"
    elif city == "thailand":
        return "Thailand, the land of smiles! The warmth and friendliness of the people there must make it a wonderful place to be. It is known for its beautiful beaches and vibrant culture."
    elif city == "malaysia":
        return "Malaysia is a melting pot of cultures. What's your favorite thing about the cultural diversity there, and do you have any must-try local dishes?"
    elif city == "singapore":
        return "Singapore is a city-state with a dynamic skyline and a melting pot of cultures. It must be an exciting place to live!"
    elif city == "france":
        return "France is a amazing place. I've heart it's known for its art, cuisine, and romantic ambiance. Do you have a favorite French dish or place in mind?"
    elif city == "italy":
        return "Italy's history, architecture, and of course, the food, make it an irresistible destination. Do you have a favorite Italian dish?"
    elif city == "australia":
        return "Australia is known for its stunning landscapes and unique wildlife. It's on my bucket list to explore the Outback someday!"
 
################################# Response With User Info ##########################################

def respond_to_name(name):
    return f" {name}, Nice to meet you!"

def respond_to_know_name(name):
    return f"Yes, you are {name}!"

def set_dialog_with_probability(probability):
    if random.random() < probability:
        GLOBALS['dialog'] = True
    else:
        GLOBALS['dialog'] = False

    return GLOBALS['dialog']