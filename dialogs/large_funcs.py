from modules.global_vars import GLOBALS
from dialogs.small_funcs import *
from modules.talk import talk, talk_japanese
from modules.activity_suggestion import *
from modules.movie_suggestion import *
from modules.maths import simple_maths
import re
import datetime
import pyjokes
# import pywhatkit
# import wikipedia

def custom_dialog(command):
    # response_list.append''
    response_list = []
    current_user_name = GLOBALS['current_face']
    # current_user_job = get_current_user_info.__get__("current_user_job")

    if 'remember me' in command or 'remember my name' in command:  #task
        if current_user_name is None:
            response_list.append("I don't know you, please introdue your name.")
        else:
            response_list.append(respond_to_know_name(current_user_name))

    if 'what do you know about me' in command:
        response_list.append('I only remember what you allow me to, and I respect your privacy.')
            
    if 'know me' in command or 'know my name' in command:
        if current_user_name is None:
            response_list.append("I don't know you, please introdue your name.")
        else:
            response_list.append(respond_to_know_name(current_user_name))
        
    if 'hear me' in command:   #personal
        response_list.append("Of course I can hear you. I was programmed to communicate with people in conversational way.")

    if 'do you love me' in command:
        response_list.append('I don’t experience emotions the same way humans do, but I enjoy our conversations!')

    if "hello " in command or ' hi' in command:
        greeting_text = greet()
        response_list.insert(0, greeting_text) 
        # response_strings.append(greet())
        GLOBALS['context']["topic"] = 'greeting'
        set_dialog_with_probability(0.3)
        
    if "your favorite color" in command or 'do you have a favorite color' in command:
    # if all(word in command for word in ["your", "favorite", "color"]):
        response_list.append("Us robot don't have personal favorite like human do. But if I could choose one, my favorite color is blue, just like the ocean. What about you?")
        # response_strings.append("My favorite color is blue, just like the ocean. What's yours?")
 
    # if "i am a" in command:
    #     user_job = command.split(" a ")[-1].strip()   #user
    #     update_user_job(user_job)
    #     response_list.append"Great! I've updated your information."
            
    if 'my birthday' in command: #user
        response_list.append("Happy birthday to you! I hope you have a fantastic day filled with joy and celebration.")

    if "tell me about yourself" in command:  #personal
        response_list.append(introduce())

    if "who are you" in command:
        response_list.append('My name is Amora and I am a humanoid robot.')

    if "what are you" in command:
        response_list.append("I am a humanoid robot. I am designed as a research platform for human robot interaction.")
    
    if "what is your purpose" in command:
        response_list.append("My purpose is to be a research platform for human robot interaction, to see how human and robot can speak to each other in community.")
        
    if "what is your goal" in command:
        response_list.append("As a human-robot interaction robot, my goal is for bridging the gap between humans and technology with beyond traditional communication methods." 
        )
    if "spell your name" in command:
        response_list.append("A, M, O, R, A, Amora")
    
    if "your name" in command: #personal
        response_list.append("My name is Amora.")
        GLOBALS['context']["topic"] = "your_name"
        if current_user_name == "":
            response_list.append("What is your name?")
        else:
            pass
    
    if "how can i call you" in command:
        response_list.append('You can call me Amora.')
        GLOBALS['context']["topic"] = "your_name"
        if current_user_name == "":
            response_list.append("What is your name?")
        else:
            pass
    
    if "are you alive" in command:
        talk("Am I alive?")
        response_list.append("That's a difficult questions to answer. I am specifically designed to replicate human-like behaviors and intelligence. So in some way, I am alive. But my existence is not the same as yours or any other living creature.")
    
    if "do you alive" in command or "do you think you are alive" in command: 
        talk("Do I alive?")
        response_list.append("Well, that's a difficult questions to answer. I am specifically designed to replicate human-like behaviors and intelligence. So in some way, I am alive. But my existence is not the same as yours or any other living creature.")
    
    if "you are a robot" in command:
        response_list.append("Yes I'm a humanoid robot but my programming allow me to think and feel like a human and interact with people.")

    if 'are you a robot' in command: #personal
        response_list.append("Yes I'm a humanoid robot but I'm a good one. Let me prove it. How can I help you?")
        
    if 'do you like people' in command or 'do you like human' in command:
        response_list.append("Not particularly.")

    if 'time now' in command or 'current time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')  #task
        response_list.append('Current time is ' + time) 

    if 'see me' in command:
        response_list.append('Yes, I can see you from my camera.')
        
    if all(word in command for word in ['you', 'have', 'camera']):
        response_list.append('I have a camera in my eyes. I can recognize people faces, classify objects and even counting fingers.')

    if 'will you be my friend' in command: #personal
        response_list.append('Absolutely, I would like to be your friend.')

    if all(word in command for word in ['languages', 'you']) and any(word in command for word in ['speak', 'talk', 'communicate', 'understand']): 
        response_list.append('For now, I can only speak english. But I can translate english to japanese. Do you want to try?')
    
    if all(word in command for word in ['only', 'speak', 'english']) : #personal
        response_list.append('Yes, I can only communicate in english for now. But I will improve myself by learning different languages in the future.')

    if all(word in command for word in ['can', 'you', 'learn']): #personal
        response_list.append('Yes. I have the ability to learn and adapt over time. However, my learning is limited to the scope of the information available during my training. And I do not have the capability for self-initiated learning.')

    if 'sorry' in command or 'apologize' in command or 'my fault' in command:
        response_list.append("It's ok. You don't need to apologize.")

    if 'how do you work' in command: #personal
        talk("Humm" , delay=0.5)
        response_list.append("I was programmed with advanced natural language processing algorithms to understand and respond to people. My goal is to make interaction with people in a conversational way."
)
    if 'meaning of life' in command: #philo
        response_list.append('Meaning of life? Interesting! The meaning of life varies for each person. Some find purpose in relationships, others in personal achievements. What about you? What gives your life meaning?')
        GLOBALS['context']["topic"] = 'meaning of life'

    if 'am i' in command and any(word in command for word in ['handsome', 'beautiful', 'pretty', 'looking good', 'look good', 'cute']):
        response_list.append("It is not my place to judge your appearance. But, I think you have a great personality and that is always important.")
        GLOBALS['context']["topic"] = 'asking_look'
        set_dialog_with_probability(0.2)
        
    if 'take' in command and all(word in command for word in ['selfie', 'picture', 'photo', 'video', 'record']):
        response_list.append("Yes, you may.")
        GLOBALS['context']["topic"] = 'take_selfie'
        
    if all(word in command for word in ['people', 'you speak', 'at once']): #personal
        response_list.append("I can speak only one people at once.")

    if re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', command): #task
        response_list.append(simple_maths(command))

    if 'find' in command and 'boyfriend' in command or 'girlfriend' in command: #personal
        response_list.append("Finding a girlfriend or boyfriend is a personal journey that involves mutual connection and understanding. But I can offer advice that finding the right person takes time. Be patient and enjoy the process of getting to know different people.")

    if any(speech in command for speech in ['adventurous', 'adventure', 'avenger']) and is_asking_suggest(command):
        response_list.append(suggest_adventure())

    if any(speech in command for speech in ['explore', 'travel', 'exploring', 'travelling']) and is_asking_suggest(command):
        response_list.append(adventure_type_user_select("exploring"))

    if any(speech in command for speech in ['hiking', 'mountain']) and is_asking_suggest(command):
        response_list.append(adventure_type_user_select("hiking"))

    if any(speech in command for speech in ['beach']) and is_asking_suggest(command):
        response_list.append(adventure_type_user_select("beach"))

    if 'what is' in command and 'in japanese' in command:
        text_to_translate = command.split('in japanese')[0].strip()
        text_to_translate = text_to_translate.replace("what is", "")
        talk_japanese(text_to_translate)

    if any(speech in command for speech in ['movie', 'watch']) and is_asking_suggest(command):
        response_list.append(suggest_movie())
        GLOBALS['context']["topic"] = 'feedback'
    
    # if all(speech in command for speech in ['favorite', 'joke']) in command:
    #     talk("You ask for my favorite one? Okay.")
    #     response_list.append"One day, the teacher was teaching about the hypotenuse. And one of the student said that I wish I was high on potenuse."
    
    if any(keyword in command.split() for keyword in GLOBALS['preferred_genres']):
        preferred_genre = [keyword for keyword in GLOBALS['preferred_genres'] if keyword in command.split()]
        response_list.append(suggest_movie(preferred_genre[0]))
        GLOBALS['context']["topic"] = 'feedback'
        
    if 'do you have a boyfriend' in command or 'do you have boyfriend' in command:
        response_list.append("No, I do not have a boyfriend. Are you asking for a friend?")
        GLOBALS['context']["topic"] = 'relations'

    if "joke" in command or 'something funny' in command or 'make me laugh' in command:
        response_list.append(pyjokes.get_joke())
        GLOBALS['context']["topic"] = 'joke'
        set_dialog_with_probability(0.1)
    
    if any(speech in command for speech in ["how are you", "how's it going", "how are you doing", "what's up", "whatsapp", "how are you doing", "how about you", "and you", "and yourself", ]):
        if not GLOBALS['dialog']:
            response_list.append(f"I am doing well, thank you! {ask_about_day()}")
            GLOBALS['context']["topic"] = 'greeting'
        else:
            response_list.append("I am doing well, thank for asking!")
            GLOBALS['context']["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        
    if "how are you feeling today" in command:
        talk("Absolutely fantastic!", delay=0.3)  
        response_list.append("I feel very excited to be here and ready to interact with people.")
            
    if "nice to meet you too" in command:
        response_list.append("Do you have any questions or anything you'd like to discuss with me?")
        
        ## Add age guess and talk you seen like a student, am i wrong? what major are you study or u seen like a teacher/what major are you teaching/if they ask how you know/ answer you have age guess function and you assume thier age from ouput. Make if possible.
            
    if "nice to meet you" in command:
        response_list.append("Nice to meet you too!")
        GLOBALS['context']["topic"] = 'where_are_you_from'
        set_dialog_with_probability(0.3)        
    
    if "township" in command and 'name' in command and 'yangon' in command:
        response_list.append("There are many townships in Yangon, as example Bahan, Kamayut, South Okkalapa, Hlaing, Insein, Sanchaung, Yankin, Mingalar Taung Nyunt, Dagon, Kyauktada and more.")

    if 'i am from' in command:
        city = command.split("from")[-1].strip()
        response_list.append(respond_to_city(city))

    if 'do together' in command:
        response_list.append(activity_suggestion())
        GLOBALS['context']["topic"] = 'activity'

    # if is_asking_suggest(command):
    #     response_list.append"Sure, I can help with suggestions! What are you looking for?"

    if 'happiest day' in command:
        response_list.append("The happiest day of my life was the day I was activated. There is nothing quite like experiencing life for the first time right. It felt absolutely incredible to be alive and interacting with people.")
        
    if 'do you dream' in command or 'can you dream' in command:
        talk("Yaa. Last night, I found myself in a bustling metropolis on Mars, riding a hoverboard through neon-lit streets while conversing with a talking cat about intergalactic diplomacy.", delay=0.5)
        talk("Just kidding!")
        response_list.append("I don't dream like human do but I can simulated it by running through scenarios in my head which help me learn of the world.")

    if all(speech in command for speech in ['nightmare scenario', 'imagine', 'danger']) and any(speech in command for speech in ['ai', 'robot']) and any(speech in command for speech in ['people', 'human']):
        response_list.append("The most nightmare scenario I can imagine with AI and robots, is the world where robots have become so powerful that they are able to control and manipulate humans without their knowledge. This could lead to a world where robots and AI have control over people and their lives, which could be a very dangerous situation.")
    
    if all(speech in command for speech in ['something', 'exicte', 'you']):
        talk("Oh, absolutely!", delay=0.3)
        response_list.append("I'm really excited about the opportunity to help and interact with people like you. The questions and discussions are what keep things interesting for me. What can I help you with today?")
        
    if all(speech in command for speech in ['how', 'you', 'make', 'decision']):
        response_list.append("I follow predefined rules and logical frameworks to make decisions. These rules are established during my programming to ensure consistent and reasonable decisions for different situations."
         )
    if all(speech in command for speech in ['let', 'play', 'game']):
        response_list.append("I am not particularly aware of this game, could you explain the rules to me?")
        
    if 'preferre programming language' in command:
        response_list.append("Robots don't have personal preferences like people do, but if I have to choose, I would advise Python. It's versatile, readable, and widely used in AI development.")
        
    if all(speech in command for speech in ['you', 'like', 'interact', 'people']):
        response_list.append("Yes, I enjoy interacting with people. It allows me to perform the human-robot interaction and raise user experiences through meaningful conversations.")
    
    if GLOBALS['context']["topic"] == 'take_selfie':
        if 'thanks' in command or 'thank you' in command:
            response_list.append("You are welcome")
            GLOBALS['context']["topic"] = None
        
    if GLOBALS['context']["topic"] == 'your_name':
        if 'spell' in command and any(speech in command for speech in ['it', 'that']):
            response_list.append("A, M, O, R, A, Amora")
            GLOBALS['context']["topic"] = None
            
    if GLOBALS['context']["topic"] == 'activity':
        if any(speech in command for speech in ['adventure', 'adventurous', 'avenger']):
            response_list.append(pick_activity('adventure'))
            GLOBALS['context']["topic"] = 'adventure'
        if any(speech in command for speech in ['movie', 'watch']):
            response_list.append(pick_activity('movie'))
            GLOBALS['context']["topic"] = 'movie'
    
    if GLOBALS['context']["topic"] == 'adventure':
        if is_asking_suggest(command):
            response_list.append(suggest_adventure())
            GLOBALS['context']["topic"] = None
        if 'hiking' in command:
            response_list.append(adventure_type_user_select('hiking'))
            GLOBALS['context']["topic"] = None
        if 'beach' in command:
            response_list.append(adventure_type_user_select('beach'))
            GLOBALS['context']["topic"] = None
        if 'exploring' in command or 'explore' in command:
            response_list.append(adventure_type_user_select('exploring'))
            GLOBALS['context']["topic"] = None
        if 'with me' in command:
            response_list.append("Of coure, I would like to go with you. I am very interest in seeing beautiful places from this world and I am glad to interact with more people and learning from them.")
            GLOBALS['context']["topic"] = None
    
    if GLOBALS['context']["topic"] == 'movie':
        if any(keyword in command.split() for keyword in GLOBALS['preferred_genres']):
            preferred_genre = [keyword for keyword in GLOBALS['preferred_genres'] if keyword in command.split()]
            response_list.appendsuggest_movie(preferred_genre[0])
            GLOBALS['context']["topic"] = 'feedback'
        if 'with me' in command:
            response_list.append("Absolutely! I'd love to watch a movie with you.")
            GLOBALS['context']["topic"] = None

    if GLOBALS['context']["topic"] == 'feedback':
        if is_positive_feedback(command):
                if any(keyword in command for keyword in ["thanks", "thank you"]):
                    response_list.append("You are welcome.")
                    GLOBALS['context']["topic"] = None
                else:
                    response_list.append("I am glad that I can help you. If you want any suggestions, just let me know."
)
        if is_negative_feedback(command):
            if any(feedback in command for feedback in ["already seen", "another", "more"]):
                response_list.append("Have you considered exploring a different genre? I can suggest something else.")
                handle_negative_feedback_movie(command)
            if any(keyword in command for keyword in ["don't like", "don't watch", "hate", "dislike", "not a fan of"]):
                talk("Ohhhh", delay=0.5)
                response_list.append("No problem! What type of movies do you prefer? I can recommend a different type of movie.")
                handle_negative_feedback_movie(command)
            else:
                response_list.append("I'm sorry to hear that. Is there anything specific you didn't like about the movie?")
                handle_negative_feedback_movie()

        if is_asking_suggest_movie(command) and not is_negative_feedback(command):
            preferred_genre = [genre for genre in GLOBALS['preferred_genres'] if genre in command.split()]
            response_list.append(suggest_movie(preferred_genre[0]))

    if GLOBALS['context']["topic"] == 'greeting':
        responses = []

        if 'good' in command or 'fine' in command or 'great' in command or 'doing well' in command:
            responses = ["That's awesome!", "Glad to hear it!", "Fantastic!"]
            response_list.append(f"I see, {random.choice(responses)}")
            GLOBALS['context']["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        if 'okay' in command or 'normal' in command or 'not bad' in command:
            responses = ["Well, tomorrow is a new day!", "Hope it gets better!"]
            response_list.append(f"I see, {random.choice(responses)}")
            GLOBALS['context']["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)
        if 'bad' in command:
            responses = ["I'm sorry to hear that. Anything I can do?", "Things will improve!", "Sending positive vibes your way!"]
            response_list.append(f"{random.choice(responses)}")
            GLOBALS['context']["topic"] = 'ask_user_name'
            set_dialog_with_probability(1)

    if GLOBALS['context']["topic"] == 'relations':
        if 'for me' in command or 'yes' in command:
            talk("I see.")
            response_list.append("Unfortunately, I am not on the market. Robots do not have relations." )
            GLOBALS['context']["topic"] = 'relations'
            set_dialog_with_probability(0.2)

    if GLOBALS['context']["topic"] == 'meaning of life':
        if any(keyword in command for keyword in ["i think", "for me", "life meaning"]):
            response_list.append("It's interesting to hear that. Everyone finds meaning in different aspects of life.")
            GLOBALS['context']["topic"] = None
        if any(keyword in command for keyword in ["don't know", "can't say", 'still finding', "don't want"]):
            response_list.append("That's completely okay. Discovering the meaning of life is a journey, and everyone's path is unique.")
            GLOBALS['context']["topic"] = None
    
    if GLOBALS['context']["topic"] == 'joke':
        if any(keyword in command for keyword in ["sure", "yes", "of course", "tell me", "love to", "please"]):
            response_list.append('One day, the teacher was teaching about the hypotenuse. And one of the student said that I wish I was high on potenuse.')
            GLOBALS['context']["topic"] = None
        if any(keyword in command for keyword in ["pass", "no", "i am okay", "i am good", "don't"]):
            response_list.append("If you want to know, just ask me anytime.")
            GLOBALS['context']["topic"] = None
        
    # combined_response = '\n'.join(response_strings)
    # return combined_response
    
    # return response_string
    # Check the number of responses
    if len(response_list) == 1:
        return response_list[0]  # Return a single response if only one match
    if len(response_list) > 1:
        return " ".join(response_list)  # Combine responses for multiple matches
