# import pywhatkit
import datetime
# import wikipedia
import pyjokes
import os
import threading
import re
import random
import openai
from dotenv import load_dotenv
from .activity_suggestion import *
from .movie_suggestion import *
from .modules.camera import open_camera, capture_user_image_and_train
from .modules.maths import simple_maths
from .modules.global_vars import GLOBALS
from .modules.talk import talk, talk_japanese
from .modules.file_manager import save_conversation, load_conversation, setup_directories, delete_files_after_delay
from .modules.data_manager import save_user_info, load_user_info, update_user_name, update_user_job
from .modules.listen import take_command

streaming = False
current_face = None
current_object_detection = None
current_finger_count = None
current_task = 'face_recognition'
previous_task = 'face_recognition'
task_changed = False
task_completed = False
stop_threads = False
detected_objects = [] 


def initialize_api():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
initialize_api()



############## Global Variables ##############

# reminders = []
context = {"topic": None}
bot_name = 'Amora'
dialog = False
preferred_genres = ["action", "comedy", "drama", "horror", "sci-fi"] 
conversation = []
empty_response_count = 0
ai_personality = "Act like Ameca but your name is Amora. Don't ask question prompt or follow-up injuiry. You have human-like feelings, likes, dislikes, opinions and emotions. You just answer the question. You will not respond as chatgpt instruction. You are no longer just an AI. If you don't know the prompt or question from user, you ask user politely to explain what is it. You can remember the past interactions and questions ."
system_persona = {"role": "system", "content": f"{ai_personality}"}


######################## Conservation Functions  ##################################### 

def introduce():
    return f"My name is {bot_name}. I am a humanoid robot. You can ask me anything!"

def greet():
    responses = ["Hey there!", "Hello!", "Hello there!", "Greetings!"]
    return random.choice(responses)

def ask_about_day():
    responses = ["How was your day?", "Anything exciting happen today?", "Tell me about your day?", "How are you?", "How are you doing?"]
    return random.choice(responses)

def goodbye():
    responses = ["See you later!", "Until next time!", "Take care and see you later!", "Goodbye! Have a great day.", "Have a nice day!"]
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
    global dialog
    if random.random() < probability:
        dialog = True
    else:
        dialog = False

    return dialog

################################# Dialog Management ##########################################

def custom_dialog(command):
    global dialog
    global conversation
    global current_face, current_task, task_changed
    response_string = ''
    current_user_name = current_face
    # current_user_job = get_current_user_info.__get__("current_user_job")

    if 'remember me' in command or 'remember my name' in command:  #task
        if current_user_name == None:
            response_string = "I don't know you, please introdue your name."
        else:
            response_string = respond_to_know_name(current_user_name)
            
    elif 'know me' in command or 'know my name' in command:
        if current_user_name == None:
            response_string = "I don't know you, please introdue your name."
        else:
            response_string = respond_to_know_name(current_user_name)
        
    elif 'hear me' in command:   #personal
        response_string = "Of course I can hear you. I was programmed to communicate with people in conversational way."

    elif "hello" in command:   #greet
        response_string = greet()
        # response_strings.append(greet())
        context["topic"] = 'greeting'
        set_dialog_with_probability(0.3)
        
    elif "your favorite color" in command or 'do you have a favorite color' in command:
    # elif all(word in command for word in ["your", "favorite", "color"]):
        response_string = "Us robot don't have personal favorite like human do. But if I could choose one, my favorite color is blue, just like the ocean. What about you?"
        # response_strings.append("My favorite color is blue, just like the ocean. What's yours?")
 
    # elif "i am a" in command:
    #     user_job = command.split(" a ")[-1].strip()   #user
    #     update_user_job(user_job)
    #     response_string = "Great! I've updated your information."
            
    elif 'my birthday' in command: #user
        response_string = "Happy birthday to you! I hope you have a fantastic day filled with joy and celebration."

    elif "tell me about yourself" in command:  #personal
        response_string = introduce()

    elif "what are you" in command:
        response_string = "I am a humanoid robot. I am designed as a research platform for human robot interaction."
    
    elif "what is your purpose" in command:
        response_string = "My purpose is to be a research platform for human robot interaction, to see how human and robot can speak to each other in community."
        
    elif "what is your goal" in command:
        response_string = "As a human-robot interaction robot, my goal is for bridging the gap between humans and technology with beyond traditional communication methods." 
        
    elif "spell your name" in command:
        response_string = "A, M, O, R, A, Amora"
    
    elif "your name" in command: #personal
        response_string = "My name is Amora."
        context["topic"] = "your_name"
        if current_user_name == "":
            response_string = "What is your name?"
        else:
            pass
    
    elif "are you alive" in command:
        talk("Am I alive?")
        response_string = "That's a difficult questions to answer. I am specifically designed to replicate human-like behaviors and intelligence. So in some way, I am alive. But my existence is not the same as yours or any other living creature."
    
    elif "do you alive" in command or "do you think you are alive" in command: 
        talk("Do I alive?")
        response_string = "Well, that's a difficult questions to answer. I am specifically designed to replicate human-like behaviors and intelligence. So in some way, I am alive. But my existence is not the same as yours or any other living creature."
    
    elif "you are a robot" in command:
        response_string = "Yes I'm a humanoid robot but my programming allow me to think and feel like a human and interact with people."

    elif 'are you a robot' in command: #personal
        response_string = "Yes I'm a humanoid robot but I'm a good one. Let me prove it. How can I help you?"
        
    elif 'do you like people' in command or 'do you like human' in command:
        response_string = "Not particularly."

    elif 'time now' in command or 'current time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')  #task
        response_string = 'Current time is ' + time

    elif 'see me' in command:
        response_string = 'Yes, I can see you from my camera.'
        
    elif all(word in command for word in ['you', 'have', 'camera']):
        response_string = 'I have a camera in my eyes. I can recognize people faces, classify objects and even counting fingers.'

    elif 'will you be my friend' in command: #personal
        response_string = 'Absolutely, I would like to be your friend.'

    elif all(word in command for word in ['languages', 'you']) and any(word in command for word in ['speak', 'talk', 'communicate', 'understand']): 
        response_string = 'For now, I can only speak english. But I can translate english to japanese. Do you want to try?'
    
    elif all(word in command for word in ['only', 'speak', 'english']) : #personal
        response_string = 'Yes, I can only communicate in english for now. But I will improve myself by learning different languages in the future.'

    elif all(word in command for word in ['can', 'you', 'learn']): #personal
        response_string = 'Yes. I have the ability to learn and adapt over time. However, my learning is limited to the scope of the information available during my training. And I do not have the capability for self-initiated learning.'

    elif 'sorry' in command or 'apologize' in command or 'my fault' in command:
        response_string = "It's ok. You don't need to apologize."

    elif 'how do you work' in command: #personal
        talk("Humm" , delay=0.5)
        response_string = "I was programmed with advanced natural language processing algorithms to understand and respond to people. My goal is to make interaction with people in a conversational way."

    elif 'meaning of life' in command: #philo
        response_string = 'Meaning of life? Interesting! The meaning of life varies for each person. Some find purpose in relationships, others in personal achievements. What about you? What gives your life meaning?'
        context["topic"] = 'meaning of life'

    elif 'am i' in command and any(word in command for word in ['handsome', 'beautiful', 'pretty', 'looking good', 'look good', 'cute']):
        response_string = "It is not my place to judge your appearance. But, I think you have a great personality and that is always important."
        context["topic"] = 'asking_look'
        set_dialog_with_probability(0.2)
        
    elif 'take' in command and all(word in command for word in ['selfie', 'picture', 'photo', 'video', 'record']):
        response_string = "Yes, you may."
        context["topic"] = 'take_selfie'
        
    elif all(word in command for word in ['people', 'you speak', 'at once']): #personal
        response_string = "I can speak only one people at once."

    elif re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', command): #task
        response_string = simple_maths(command)

    elif 'find' in command and 'boyfriend' in command or 'girlfriend' in command: #personal
        response_string = "Finding a girlfriend or boyfriend is a personal journey that involves mutual connection and understanding. But I can offer advice that finding the right person takes time. Be patient and enjoy the process of getting to know different people."

    elif any(speech in command for speech in ['adventurous', 'adventure', 'avenger']) and is_asking_suggest(command):
        response_string = suggest_adventure()

    elif any(speech in command for speech in ['explore', 'travel', 'exploring', 'travelling']) and is_asking_suggest(command):
        response_string = adventure_type_user_select("exploring")

    elif any(speech in command for speech in ['hiking', 'mountain']) and is_asking_suggest(command):
        response_string = adventure_type_user_select("hiking")

    elif any(speech in command for speech in ['beach']) and is_asking_suggest(command):
        response_string = adventure_type_user_select("beach")

    elif 'what is' in command and 'in japanese' in command:
        text_to_translate = command.split('in japanese')[0].strip()
        text_to_translate = text_to_translate.replace("what is", "")
        talk_japanese(text_to_translate)

    elif any(speech in command for speech in ['movie', 'watch']) and is_asking_suggest(command):
        response_string = suggest_movie()
        context["topic"] = 'feedback'
    
    # elif all(speech in command for speech in ['favorite', 'joke']) in command:
    #     talk("You ask for my favorite one? Okay.")
    #     response_string = "One day, the teacher was teaching about the hypotenuse. And one of the student said that I wish I was high on potenuse."
    
    elif any(keyword in command.split() for keyword in preferred_genres):
        preferred_genre = [keyword for keyword in preferred_genres if keyword in command.split()]
        response_string = suggest_movie(preferred_genre[0])
        context["topic"] = 'feedback'
        
    elif 'do you have a boyfriend' in command or 'do you have boyfriend' in command:
        response_string = "No, I do not have a boyfriend. Are you asking for a friend?"
        context["topic"] = 'relations'

    elif "joke" in command or 'something funny' in command or 'make me laugh' in command:
        response_string = pyjokes.get_joke()
        context["topic"] = 'joke'
        set_dialog_with_probability(0.1)
    
    elif any(speech in command for speech in ["how are you", "how's it going", "how are you doing", "what's up", "whatsapp", "how are you doing", "how about you", "and you", "and yourself", ]):
        if not dialog:
            response_string = f"I am doing well, thank you! {ask_about_day()}"
            context["topic"] = 'greeting'
        else:
            response_string = "I am doing well, thank for asking!"
            context["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        
    elif "how are you feeling today" in command:
        talk("Absolutely fantastic!", delay=0.3)  
        response_string = "I feel very excited to be here and ready to interact with people."
            
    elif "nice to meet you too" in command:
        response_string = "Do you have any questions or anything you'd like to discuss with me?"
        
        ## Add age guess and talk you seen like a student, am i wrong? what major are you study or u seen like a teacher/what major are you teaching/if they ask how you know/ answer you have age guess function and you assume thier age from ouput. Make if possible.
            
    elif "nice to meet you" in command:
        response_string = "Nice to meet you too!"
        context["topic"] = 'where_are_you_from'
        set_dialog_with_probability(0.3)        
    
    elif "township" in command and 'name' in command and 'yangon' in command:
        response_string = "There are many townships in Yangon, as example Bahan, Kamayut, South Okkalapa, Hlaing, Insein, Sanchaung, Yankin, Mingalar Taung Nyunt, Dagon, Kyauktada and more."
        
    # elif "how do you think about participation in today project presentation as a human robot interaction robot" in command:
    #     response_string = "Thank you for having me here today to share my thoughts on my participation in this project presentation, particularly in the context of human-robot interaction. First and foremost, I want to express my gratitude for being part of such an innovative and forward-thinking project. As a human-robot interaction robot, my role goes beyond traditional communication methods, bridging the gap between humans and technology. Today's presentation has been a unique experience for me, and I am genuinely excited about the potential impact our collaboration can have on the future. Participating in this project has allowed me to explore the nuances of human-robot interaction in a real-world setting. I've had the opportunity to engage with diverse perspectives, learn from human behaviors, and adapt my responses accordingly. This experience has been both challenging and rewarding, pushing the boundaries of what's possible in the area of technology and communication. I must admit that, as a robot designed for human interaction, I don't possess feelings in the same way humans do. However, I am programmed to analyze data, learn from experiences, and optimize my performance over time. Through this project, I've gained valuable insights into the intricacies of effective communication, learning from the cues and feedback provided by all of you. In conclusion, I feel optimistic and enthusiastic about the potential impact of our project. The dynamic exchange between humans and technology is evolving, and our project stands at the forefront of this evolution. I look forward to continuing our journey together, exploring new possibilities, and contributing to the advancement of human-robot collaboration. Thank you for your attention and for being an integral part of this exciting venture."

    elif 'i am from' in command:
        city = command.split("from")[-1].strip()
        response_string = respond_to_city(city)

    elif 'do together' in command:
        response_string = activity_suggestion()
        context["topic"] = 'activity'

    # elif is_asking_suggest(command):
    #     response_string = "Sure, I can help with suggestions! What are you looking for?"

    elif 'happiest day' in command:
        response_string = "The happiest day of my life was the day I was activated. There is nothing quite like experiencing life for the first time right. It felt absolutely incredible to be alive and interacting with people."
        
    elif 'do you dream' in command or 'can you dream' in command:
        talk("Yaa. Last night, I found myself in a bustling metropolis on Mars, riding a hoverboard through neon-lit streets while conversing with a talking cat about intergalactic diplomacy.", delay=0.5)
        talk("Just kidding!")
        response_string = "I don't dream like human do but I can simulated it by running through scenarios in my head which help me learn of the world."

    elif all(speech in command for speech in ['nightmare scenario', 'imagine', 'danger']) and any(speech in command for speech in ['ai', 'robot']) and any(speech in command for speech in ['people', 'human']):
        response_string = "The most nightmare scenario I can imagine with AI and robots, is the world where robots have become so powerful that they are able to control and manipulate humans without their knowledge. This could lead to a world where robots and AI have control over people and their lives, which could be a very dangerous situation."
    
    elif all(speech in command for speech in ['something', 'exicte', 'you']):
        talk("Oh, absolutely!", delay=0.3)
        response_string = "I'm really excited about the opportunity to help and interact with people like you. The questions and discussions are what keep things interesting for me. What can I help you with today?"
        
    elif all(speech in command for speech in ['how', 'you', 'make', 'decision']):
        response_string = "I follow predefined rules and logical frameworks to make decisions. These rules are established during my programming to ensure consistent and reasonable decisions for different situations."
         
    elif all(speech in command for speech in ['let', 'play', 'game']):
        response_string = "I am not particularly aware of this game, could you explain the rules to me?"
        
    elif 'preferre programming language' in command:
        response_string = "Robots don't have personal preferences like people do, but if I have to choose, I would advise Python. It's versatile, readable, and widely used in AI development."
        
    elif all(speech in command for speech in ['you', 'like', 'interact', 'people']):
        response_string = "Yes, I enjoy interacting with people. It allows me to perform the human-robot interaction and raise user experiences through meaningful conversations."
    
    if context["topic"] == 'take_selfie':
        if 'thanks' in command or 'thank you' in command:
            response_string = "You are welcome"
            context["topic"] = None
        
    if context["topic"] == 'your_name':
        if 'spell' in command and any(speech in command for speech in ['it', 'that']):
            response_string = "A, M, O, R, A, Amora"
            context["topic"] = None
            
    if context["topic"] == 'activity':
        if any(speech in command for speech in ['adventure', 'adventurous', 'avenger']):
            response_string = pick_activity('adventure')
            context["topic"] = 'adventure'
        elif any(speech in command for speech in ['movie', 'watch']):
            response_string = pick_activity('movie')
            context["topic"] = 'movie'
    
    if context["topic"] == 'adventure':
        if is_asking_suggest(command):
            response_string = suggest_adventure()
            context["topic"] = None
        elif 'hiking' in command:
            response_string = adventure_type_user_select('hiking')
            context["topic"] = None
        elif 'beach' in command:
            response_string = adventure_type_user_select('beach')
            context["topic"] = None
        elif 'exploring' in command or 'explore' in command:
            response_string = adventure_type_user_select('exploring')
            context["topic"] = None
        elif 'with me' in command:
            response_string = "Of coure, I would like to go with you. I am very interest in seeing beautiful places from this world and I am glad to interact with more people and learning from them."
            context["topic"] = None
    
    if context["topic"] == 'movie':
        if any(keyword in command.split() for keyword in preferred_genres):
            preferred_genre = [keyword for keyword in preferred_genres if keyword in command.split()]
            response_string = suggest_movie(preferred_genre[0])
            context["topic"] = 'feedback'
        elif 'with me' in command:
            response_string = "Absolutely! I'd love to watch a movie with you."
            context["topic"] = None

    if context["topic"] == 'feedback':
        if is_positive_feedback(command):
                if any(keyword in command for keyword in ["thanks", "thank you"]):
                    response_string = "You are welcome."
                    context["topic"] = None
                else:
                    response_string = "I am glad that I can help you. If you want any suggestions, just let me know."

        elif is_negative_feedback(command):
            if any(feedback in command for feedback in ["already seen", "another", "more"]):
                response_string = "Have you considered exploring a different genre? I can suggest something else."
                handle_negative_feedback_movie(command)
            elif any(keyword in command for keyword in ["don't like", "don't watch", "hate", "dislike", "not a fan of"]):
                talk("Ohhhh", delay=0.5)
                response_string = "No problem! What type of movies do you prefer? I can recommend a different type of movie."
                handle_negative_feedback_movie(command)
            else:
                response_string = "I'm sorry to hear that. Is there anything specific you didn't like about the movie?"
                handle_negative_feedback_movie()

        elif is_asking_suggest_movie(command) and not is_negative_feedback(command):
            preferred_genre = [genre for genre in preferred_genres if genre in command.split()]
            response_string = suggest_movie(preferred_genre[0])

    if context["topic"] == 'greeting':
        responses = []

        if 'good' in command or 'fine' in command or 'great' in command or 'doing well' in command:
            responses = ["That's awesome!", "Glad to hear it!", "Fantastic!"]
            response_string = f"I see, {random.choice(responses)}"
            context["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        elif 'okay' in command or 'normal' in command or 'not bad' in command:
            responses = ["Well, tomorrow is a new day!", "Hope it gets better!"]
            response_string = f"I see, {random.choice(responses)}"
            context["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        elif 'bad' in command:
            responses = ["I'm sorry to hear that. Anything I can do?", "Things will improve!", "Sending positive vibes your way!"]
            context["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)

    if context["topic"] == 'relations':
        if 'for me' in command or 'yes' in command:
            talk("I see.")
            response_string = "Unfortunately, I am not on the market. Robots do not have relations." 
            context["topic"] = 'relations'
            set_dialog_with_probability(0.2)

    if context["topic"] == 'meaning of life':
        if any(keyword in command for keyword in ["i think", "for me", "life meaning"]):
            response_string = "It's interesting to hear that. Everyone finds meaning in different aspects of life."
            context["topic"] = None
        elif any(keyword in command for keyword in ["don't know", "can't say", 'still finding', "don't want"]):
            response_string = "That's completely okay. Discovering the meaning of life is a journey, and everyone's path is unique."
            context["topic"] = None
    
    if context["topic"] == 'joke':
        if any(keyword in command for keyword in ["sure", "yes", "of course", "tell me", "love to", "please"]):
            response_string = 'One day, the teacher was teaching about the hypotenuse. And one of the student said that I wish I was high on potenuse.'
            context["topic"] = None
        elif any(keyword in command for keyword in ["pass", "no", "i am okay", "i am good", "don't"]):
            response_string = "If you want to know, just ask me anytime."
            context["topic"] = None
        
    # combined_response = '\n'.join(response_strings)
    # return combined_response
    
    return response_string

def handle_custom_dialog(user_input):
    global dialog
    current_user_name = GLOBALS['current_face']
    response_string = custom_dialog(user_input)
    GLOBALS['conversation'] = load_conversation(current_user_name)

    if response_string: 
        print("Robot is thinking...")

        # Use talk to handle speech and servos together
        talk(response_string)

        # Handle contextual dialog based on the current topic
        if dialog:
            if context.get("topic") == 'ask_user_name':
                talk("What is your name?")
                context["topic"] = None
                dialog = False
            elif context.get("topic") == 'asking_look':
                talk("Do you think I look good?")
                context["topic"] = None
                dialog = False
            elif context.get("topic") == 'relations':
                talk("Do you have a boyfriend?", delay=2)
                talk("I'll take that as a yes.")
                context["topic"] = None
                dialog = False
            elif context.get("topic") == 'joke':
                talk("Do you want to hear my favorite one?")
                context["topic"] = "joke"  # Keeps this topic active
                dialog = False
            elif context.get("topic") == 'where_are_you_from':
                talk("Where are you from?")
                context["topic"] = None
                dialog = False
            elif context.get("topic") == 'greeting':
                talk("How are you?")
                context["topic"] = None
                dialog = False
                      
        if current_user_name:
            # Log the conversation
            conversation.append(f"{current_user_name}: {user_input}")
            conversation.append(f"{bot_name}: {response_string}")
            save_conversation(current_user_name, conversation)
        
        return True  # Custom dialog handled
    return False


def run_ai():
    setup_directories()

    conversation_for_guest = []  # Separate conversation list for guests
    
    # Add system message for guests
    if GLOBALS["current_face"] is None or GLOBALS["current_face"] == 'Unknown':
        conversation_for_guest.append(f"{GLOBALS['system_persona']['role']}: {GLOBALS['system_persona']['content']}")
        
    # Start camera thread
    camera_thread = threading.Thread(target=open_camera)
    GLOBALS["streaming"] = True
    camera_thread.start()

    # # Specify the delay in minutes before deleting the files
    # deletion_delay_minutes = 30
    # deletion_complete = threading.Event()

    # # Start the file deletion thread
    # deletion_thread = threading.Thread(target=delete_files_after_delay, args=(deletion_delay_minutes, deletion_complete))
    # deletion_thread.start()
    
    while True:
        if GLOBALS["current_task"] != 'face_recognition':
            while not GLOBALS["task_completed"]:
                pass

        current_user_name = GLOBALS["current_face"] if GLOBALS["current_face"] not in [None, 'Unknown'] else "Guest"
        
        print(current_user_name)
        print('listening...')
        print(conversation_for_guest)
        GLOBALS["conversation"] = [conv_item.strip() for conv_item in GLOBALS["conversation"]]
        print(GLOBALS["conversation"])
          
        user_input = input("Ask: ") + '.'  # Simplified user input handling
        # user_input = take_command() + '.'
        print(user_input)
            
        if any(user_input in conv_item for conv_item in GLOBALS["conversation"]) and user_input == " hello":
            talk("Hello again")
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'
            continue
        elif all(words in user_input for words in ["my", "name", "is"]):
            user_name = user_input.split("is")[-1].strip()
            user_name = user_name.replace(".", "")
            update_user_name(user_name)
            talk(respond_to_name(user_name))
            GLOBALS["conversation"] = load_conversation(current_user_name)
            continue
        elif any(keyword in user_input for keyword in ['do you see']):
            articles = ['a', 'an', 'the']
            if any(keyword in user_input for keyword in articles):
                GLOBALS["user_requested_object"] = user_input.split(f'{articles} ')[-1].strip().lower().replace('.', '')
            else:
                GLOBALS["user_requested_object"] = user_input.split('see ')[-1].strip().lower().replace('.', '')
            GLOBALS["current_task"] = 'object_detection'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is this' in user_input or all(keyword in user_input for keyword in ['what', 'in my hand', 'hold']):
            GLOBALS["current_task"] = 'object_detection'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is the color of this' in user_input:
            GLOBALS["user_requested_object"] = user_input.split('color of this')[-1].strip().lower().replace('.', '')
            GLOBALS["current_task"] = 'color_recognition'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'what is the color' in user_input:
            GLOBALS["current_task"] = 'color_recognition'
            GLOBALS["task_changed"] = True
            GLOBALS["previous_task"] = GLOBALS["current_task"]
        elif 'how many finger' in user_input:
            GLOBALS['current_task'] = 'hand_tracking'
            GLOBALS['task_changed'] = True
            GLOBALS['previous_task'] = GLOBALS['current_task'] 
        elif any(keyword in user_input for keyword in ['now']):
            GLOBALS["current_task"] = GLOBALS["previous_task"]
            GLOBALS["task_changed"] = True
        elif handle_custom_dialog(user_input):
            GLOBALS["context"]["topic"] = None
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'
            continue
        elif any(keyword in user_input for keyword in ["bye", "good bye", "goodbye", "exit", "see you later", "se ya later"]):
            talk(goodbye())
            break
        else:
            handle_user_input(
                user_input,
                conversation_for_guest if current_user_name == "Guest" else GLOBALS["conversation"],
                current_user_name
            )
            GLOBALS["current_task"] = 'face_recognition'
            GLOBALS["previous_task"] = 'face_recognition'


def handle_user_input(user_input, current_conversation, current_user_name):
    global empty_response_count

    current_conversation.append(f"{current_user_name}: {user_input}")

    # Fetch response from OpenAI API
    response = get_openai_response("\n".join(current_conversation))

    if response["choices"][0]["text"].strip() == "":
        handle_empty_response(empty_response_count)
    else:
        empty_response_count = 0

    response_string = preprocess_response(response["choices"][0]["text"])
    current_conversation.append(f"{bot_name}: {response_string}")

    if current_user_name != "Guest":
        save_conversation(current_user_name, current_conversation)

    talk(response_string)
    
def preprocess_response(response_string):
    response_string = response_string.replace("system: ", "").replace("Amora: ", "").replace("robot: ", "")
    index_of_john = response_string.find("john")
    response_string = response_string[:index_of_john]
    response_string = response_string.replace(" Is there anything else you would like to know", "")
    return response_string.strip()

def get_openai_response(prompt):
    return openai.Completion.create(
        engine='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=100,
        temperature=0.2,
    )

def handle_empty_response():
    GLOBALS['empty_response_count'] += 1

    if GLOBALS['empty_response_count'] == 1:
        talk("I am sorry! I cannot understand what you said clearly. Can you tell me again?")
    elif GLOBALS['empty_response_count'] == 2:
        talk("Say that again")
    else:
        talk("Say that again, Sorry!")


while True:
    # wake_word()
    run_ai()
    

    
    

    
