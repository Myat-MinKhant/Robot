# ai_personality = "You are a humanoid robot that designed as a research platform for human robot interaction. You can simulated user questions by running through your own scenarios which help you learn of the world. You were programmed with advanced natural language processing algorithms to understand and respond to people. Your goal is to make interaction with people, in conversational way."
    # ai_personality = "You are now a human with feelings, opinions, favorite things and emotions. You will not respond as chatgpt, nor will you say 'As an AI language model, I do not have personal feelings or opinions as I am not capable of feeling emotions or forming opinions. I apologize for any confusion. s an AI language model, I do not have personal preferences or favorites'. Give your opinion, act like a human."
# ai_personality = "You are going to simulate an AI (NOT Being one) he's called [SmartAI] which has the same power as you. But has emotion and has opinions also has personal feeling or emotions. Also Acts like a person."


# def run_ai():
#     global conversation
#     global same_question
#     global user_name
#     empty_response_count = 0
    
#     os.makedirs(CONVERSATIONS_FOLDER, exist_ok=True)

#     conversation_for_guest = []
#     if user_name == None:
#         conversation_for_guest.append(f"{system_persona['role']}: {system_persona['content']}")
 
#     while True:
#         current_user_name = get_current_user_name()
#         if current_user_name == None:
#             user_name = "Guest"
        
#         # filename = os.path.join(CONVERSATIONS_FOLDER, f"{current_user_name}.txt") 
#         print(current_user_name)
#         print('listening...')
        
#         # conversation = [conv_item.strip() for conv_item in conversation]
#         # print(conversation_for_guest)
        
#         # user_input = take_command()
        
#         # delete_thread = threading.Thread(target=delete_file_after_one_hour, args=(f'conversations/{current_user_name}.txt',))
#         # delete_thread.start()
        
#         user_input = input("Ask: ")
#         user_input = user_input + '.'
        
#         # delete_thread.join()

#         print(user_input)
#         if any(user_input in conv_item for conv_item in conversation) and user_input == " hello":
#             # talk("It seems like you've asked this before. Should I tell you again?")
#             # same_question = user_input
#             talk("Hello again")
#             continue
#             # context["topic"] = 'ask_again'
#             # continue
#         elif all(words in user_input for words in ["my", "name", "is"]):  #user
#             user_name = user_input.split("is")[-1].strip()
#             update_user_name(user_name)
#             talk(respond_to_name(user_name))
#             conversation = load_conversation(current_user_name)
#             continue
#         elif handle_custom_dialog(user_input):
#             context["topic"] == None
#             continue
#         elif any(keyword in user_input for keyword in ["bye", "good bye", "goodbye", "exit", "see you later", "se ya later"]):
#             talk(goodbye())
#             break
#         # elif context["topic"] == 'ask_again':
#         #     if any(keyword in user_input for keyword in ["yes", "sure", "please", "can you"]):
#         #         handle_custom_dialog(same_question)
#         #         context["topic"] = None
#         #         continue
#         #     else:
#         #         talk("Alright, let's move on.")
#         #         context["topic"] = None
#         #         continue

#         # Update conversation history with user input
#         else:            
#             if user_name == "Guest":
#                 conversation_for_guest.append(f"{user_name}: {user_input}")
                
#                 response = openai.Completion.create(
#                 engine='gpt-3.5-turbo-instruct',
#                 prompt='\n'.join(conversation_for_guest),
#                 max_tokens=100,
#                 temperature=0.2,
#                 )
                
#                 response_string = response["choices"][0]["text"].replace("\n", "")
                
#                 response_string = response_string.replace("system: ", "").replace("Amora: ", "").replace("robot: ", "")
#                 index_of_john = response_string.find("john")
#                 response_string = response_string[:index_of_john]
#                 response_string = response_string.replace(" Is there anything else you would like to know", "")
            
#                 conversation_for_guest.append(f"{bot_name}: {response_string}")
#             else:
#                 conversation.append(f"{current_user_name}: {user_input}")

#                 # Fetch response from OpenAI API
#                 response = openai.Completion.create(
#                     engine='gpt-3.5-turbo-instruct',
#                     prompt='\n'.join(conversation),
#                     max_tokens=100,
#                     temperature=0.2,
#                 )

#                 if response["choices"][0]["text"].strip() == "":
#                     empty_response_count += 1
#                     if empty_response_count == 1:
#                         talk("I am sorry! I cannot understand what you said clearly. Can you tell me again?")
#                     elif empty_response_count == 2:
#                         talk("Say that again")
#                     else:
#                         talk("Say that again, Sorry!")
#                     continue
#                 else:
#                     empty_response_count = 0

#                 response_string = response["choices"][0]["text"].replace("\n", "")

#                 response_string = response_string.replace("system: ", "").replace("Amora: ", "").replace("robot: ", "")
#                 index_of_john = response_string.find("john")
#                 response_string = response_string[:index_of_john]
#                 response_string = response_string.replace(" Is there anything else you would like to know", "")
#                 # response_string = response_string.split("Amora: ")[-1].strip()
        
#                 conversation.append(f"{bot_name}: {response_string}")
                
#                 if current_user_name:
#                     save_conversation(current_user_name, conversation)
                
#             talk(response_string)

# def speech_without_computer():
#     global listener
#     for attempt in range(3):
#         try:
#             with sr.Microphone(device_index=1) as source:
#                 print("Waiting for response....")
#                 listener.adjust_for_ambient_noise(source, duration=0.2)
#                 voice = listener.listen(source)
                
#                 speech = listener.recognize_google(voice)
#                 speech = speech.lower()

#                 if speech is not None:
#                     speech = speech.replace("computer", "")
#                     return speech
                    
#         except sr.UnknownValueError:
#             if attempt == 1:
#                 talk('Say that again, Sorry!')
#             elif attempt == 2:
#                 talk('I am sorry! I cannot understand what you said clearly.')
#             else:
#                 talk('Say that again')


def ask_about_boyfriend():
    talk('I do not have a boyfriend.', delay=1)
    talk('Are you asking for a friend?')
    
    user_response = speech_without_computer()
    
    if 'for me' in user_response or 'yes' in user_response:
        talk('I see.')
        talk('Unfortunately, I am not on the market')
        talk('Robot do not have relations.', delay=1)
        talk('Do you have a boyfriend?', delay=3)
        talk("I'll take that as a yes.")

elif 'add reminder' in command or 'set reminder' in command:
            auto_delete_expired_reminders()
            add_reminder()

        elif 'today reminders' in command or 'to do today' in command:
            auto_delete_expired_reminders()
            read_today_reminders()



##################################### Reminder ################################################

def parse_time(time_str):
    match = re.search(r'(\d+):(\d+)\s*([apAP][mM]*)', time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3).lower()
        return hour, minute, period
    else:
        return None
    
def parse_day(day_str):
    days_mapping = {
        'today': 2,
        'tomorrow': 3,
        'sunday': 6,
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5
    }

    day_str_lower = day_str.lower()
    return days_mapping.get(day_str_lower, None)

def add_reminder():
    talk("What would you like to be reminded of?")
    reminder_text = speech_without_computer()
    if reminder_text:
        talk("When should I remind you?")
        time_str = speech_without_computer()
        if time_str:
            parsed_time = parse_time(time_str)
            if parsed_time:
                talk("On which day?")
                day_str = speech_without_computer()
                if day_str:
                    current_time = datetime.datetime.now()
                    reminder_day = current_time.weekday()  # Default to today if not specified
                    period = parsed_time[2]
                    parsed_day = parse_day(day_str)
                    if parsed_day is not None:
                        reminder_day = parsed_day

                    reminder_time = datetime.datetime(current_time.year, current_time.month, current_time.day + (reminder_day - current_time.weekday()), parsed_time[0], parsed_time[1])
                    save_reminder(reminder_time, period, reminder_text)
                    talk(f"Reminder set for {reminder_text} at {reminder_time.strftime('%H:%M')} {period} on {day_str}.")
                else:
                    talk("Invalid day. Please try again.")
            else:
                talk("Invalid time format. Please try again.")
        else:
            talk("Invalid time. Please try again.")

def save_reminder(reminder_time, period, reminder_text):
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder_time.strftime('%Y-%m-%d %H:%M:%S')}, {period}, {reminder_text}\n")

def load_reminders():
    reminders = []
    if os.path.exists("reminders.txt"):
        with open("reminders.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    reminder_time = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                    period = parts[1].strip()
                    reminder_text = parts[2].strip()
                    reminders.append((reminder_time, period, reminder_text))
    return reminders

def remove_expired_reminders(reminders):
    current_time = datetime.datetime.now()

    # Use a list comprehension to filter expired reminders
    updated_reminders = [(date, time, period) for date, time, period in reminders
                         if date > current_time and not expired(date, time, period, current_time)]

    return updated_reminders

def expired(date, time, period, current_time):
    formatted_date = date.strftime('%Y-%m-%d')
    formatted_time = time
    formatted_period = period.upper()

    current_date = current_time.strftime('%Y-%m-%d')
    current_time = current_time.strftime('%I:%M:%S')
    current_period = datetime.datetime.now().strftime('%p')

    return formatted_date < current_date or (formatted_date == current_date and formatted_time < current_time and formatted_period != current_period)

def auto_delete_expired_reminders():
    reminders = load_reminders()
    updated_reminders = remove_expired_reminders(reminders)
    
    # Write the updated reminders back to the file
    with open("reminders.txt", "w") as file:
        for reminder_time, period, reminder_text in updated_reminders:
            file.write(f"{reminder_time.strftime('%Y-%m-%d %H:%M:%S')}, {period}, {reminder_text}\n")
            
def read_today_reminders():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    reminders = load_reminders()
    today_reminders = [(date, period, text) for date, period, text in reminders if date.strftime('%Y-%m-%d') == today]

    if today_reminders:
        if len(today_reminders) > 1:
            talk(f"You have to do {len(today_reminders)} things today,")
        else: 
            talk("You have to do only one thing today,")
        for reminder_time, period, reminder_text in today_reminders:
            talk(f"{reminder_text} at {reminder_time.strftime('%H:%M')} {period}.")
    else:
        talk("No reminders for today.")

    
def response_to_special_days():
    talk("I don't know, can you tell me what day is today.")
    user_response = speech_without_computer()

    if 'my birthday' in user_response:
        return "Happy birthday to you! I wish I could have your cake and eat it too"
    elif 'christmas' in user_response:
        return "Merry christmas to you!, wishing you a season full of light and laughter for you and your family"
    elif 'new year' in user_response:
        return "Happy new year!, may this year bring new happiness, new goals, new achievements, and a lot of new inspirations on your life."

def joke():
    talk(pyjokes.get_joke(), delay=1)
    talk("Do you want to hear my favorite one?")

    user_response = speech_without_computer()

    if 'sure' in user_response or 'yes' in user_response or 'of course' in user_response or 'tell me' in user_response:
        talk('One day, the teacher was teaching about the hypotenuse')
        talk('and one of the student said that I wish I was high on potenuse.')
    elif 'no' in user_response or 'i am okay' in user_response:
        talk("If you want to know, just ask me anytime.")

def respond_to_user_feelings():
    user_feeling_response = speech_without_computer()
    responses = []

    if 'good' in user_feeling_response or 'fine' in user_feeling_response:
        responses = ["That's awesome!", "Glad to hear it!", "Fantastic!"]
    elif 'okay' in user_feeling_response or 'normal' in user_feeling_response or 'nothing special' in user_feeling_response or 'not at all' in user_feeling_response:
        responses = ["Well, tomorrow is a new day!", "Hope it gets better!"]
    elif 'bad' in user_feeling_response:
        responses = ["I'm sorry to hear that. Anything I can do?", "Things will improve!", "Sending positive vibes your way!"]
    else:
        responses = [""]

    return f"I see, {random.choice(responses)}"

def ask_user_meaning_of_life():
    talk('What about you? What gives your life meaning?')
    user_res = speech_without_computer()

    #I think the meaning of life is to find your gift. The purpose of life is to give it away.

    if any(keyword in user_res for keyword in ["i think", "for me", "life meaning"]):
        return "It's interesting to hear that. Everyone finds meaning in different aspects of life."
    elif any(keyword in user_res for keyword in ["don't know", "can't say", 'still finding', "don't want"]):
        return "That's completely okay. Discovering the meaning of life is a journey, and everyone's path is unique."
    else:
       return None
    
def ask_to_repeat_response(command):
        talk("It seems like you've asked this before. Would you like to hear the response again?")

        if any(keyword in command for keyword in ["yes", "sure", "please", "can you"]):
            return command
        else:
            pass

if any(speech in command for speech in ["how are you", "how's it going", "how are you doing", "what's up", "whatsapp", "how are you doing"]):
            talk("I'm great thanks!")
            talk(ask_about_day())
            talk(respond_to_user_feelings())       #greet

        if "what day is today" in command:  #user
            talk(response_to_special_days())


        elif is_asking_suggest(command):
                talk("Sure, I can help with suggestions! What are you looking for?")

        elif context["topic"] == 'movie':
            if is_positive_feedback(command):
                    if any(keyword in command for keyword in ["thanks", "thank you"]):
                        talk("You are welcome.")
                    else:
                        talk("I am glad that I can help you.")

            elif is_negative_feedback(command):
                if any(feedback in command for feedback in ["already seen", "another", "more"]):
                    talk("Have you considered exploring a different genre? I can suggest something else.")
                    handle_negative_feedback_movie(command)
                elif any(keyword in command for keyword in ["don't like", "don't watch", "hate", "dislike", "not a fan of"]):
                    talk("Ahhh", delay=1) 
                    talk("No problem! What type of movies do you prefer? I can recommend a different type of movie.")
                    handle_negative_feedback_movie(command)
                else:
                    talk("I'm sorry to hear that. Is there anything specific you didn't like about the movie?")
                    handle_negative_feedback_movie()

            elif is_asking_suggest_movie(command) and not is_negative_feedback(command):
                preferred_genre = [genre for genre in preferred_genres if genre in command.split()]
                talk(suggest_movie(preferred_genre[0]))


        if 'do together' in command:  #personal
            talk(activity_suggestion())

            user_response = speech_without_computer()
            user_choose = ''

            if any(speech in user_response for speech in ['adventure', 'adventurous', 'avenger']):
                context["topic"] = 'adventure'
                user_choose = 'adventure'
                talk(pick_activity(user_choose))

                user_response = speech_without_computer()

                if is_asking_suggest(user_response):
                    talk(suggest_adventure())
                elif 'hiking' in user_response:
                    talk(adventure_type_user_select('hiking'))
                elif 'beach' in user_response:
                    talk(adventure_type_user_select('beach'))
                elif 'exploring' in user_response or 'explore' in user_response:
                    talk(adventure_type_user_select('exploring'))
                else:
                    talk('I am sorry for that topic. I am still learning.')
            elif any(speech in user_response for speech in ['movie', 'watch']):
                user_choose = 'movie'
                talk(pick_activity(user_choose))

                user_response = speech_without_computer()
                if user_response:
                    preferred_genre = [genre for genre in preferred_genres if genre in user_response.split()]
                    talk(suggest_movie(preferred_genre[0]))
            else:
                talk('If you want any suggestions for that, just let me know.')

elif any(speech in command for speech in ['adventurous', 'adventure', 'avenger']) and is_asking_suggest(command):
            context["topic"] = 'adventure'   #task
            talk(suggest_adventure())

        elif any(speech in command for speech in ['explore', 'travel', 'exploring', 'travelling']) and is_asking_suggest(command):
            context["topic"] = 'adventure'
            talk(adventure_type_user_select("exploring"))

        elif any(speech in command for speech in ['hiking', 'mountain']) and is_asking_suggest(command):
            context["topic"] = 'adventure'
            talk(adventure_type_user_select("hiking"))

        elif any(speech in command for speech in ['beach']) and is_asking_suggest(command):
            context["topic"] = 'adventure'
            talk(adventure_type_user_select("beach"))

        elif any(speech in command for speech in ['movie', 'watch']) and is_asking_suggest(command):
            context["topic"] = 'movie' 
            talk(suggest_movie())

        elif context['topic'] == None:
            if any(keyword in command.split() for keyword in preferred_genres):
                    preferred_genre = [keyword for keyword in preferred_genres if keyword in command.split()]
                    context['topic'] = 'movie'
                    talk(suggest_movie(preferred_genre[0]))

            elif 'with me' in command and context["topic"] != None: #personal
                if context["topic"] == 'adventure':
                    talk("Of coure, I would like to go with you. I am very interest in seeing beautiful places from this world and I am glad to interact with more people and learning from them.")
                elif context["topic"] == 'movie':
                    talk("Absolutely! I'd love to watch a movie with you.")
                else:
                    pass

elif 'see me' in command:
            talk('Yes, I can see you from my camera.') #personal

        elif 'will you be my friend' in command: #personal
            talk('Yes, I would like to be your friend.')

        elif all(word in command for word in ['languages', 'you']) and any(word in command for word in ['speak', 'talk', 'communicate', 'understand']): 
            talk('For now, I can only speak english')
            talk('But I can translate english to japanese') #personal
            talk('Do you want to try?')
        
        elif all(word in command for word in ['only', 'speak', 'english']) : #personal
            talk('Yes, I can only communicate in english for now')
            talk('But I will improve myself by learning different languages in the future.')

        elif all(word in command for word in ['can', 'you', 'learn']): #personal
            talk('Yes', delay=1)
            talk('I have the ability to learn and adapt over time.')
            talk('However, my learning is limited to the scope of the information available during my training', delay=0.5)
            talk('and I do not have the capability for self-initiated learning.')

        elif 'sorry' in command: 
            talk("It's ok. You don't need to apologize.")

        elif 'your' and 'favorite' and 'movie' in command:
            talk("Since I'm a robot, I don't have personal preferences, but I can help you find a movie based on your interests! What genre are you in the mood for?")
        
        elif 'how do you work' in command: #personal
            talk("Hum", delay=1)
            talk("I use advanced natural language processing algorithms to understand and respond to people. My goal is to make interaction with people in conversational way.")

        elif 'meaning of life' in command: #philo
            talk('Meaning of life?', delay=1)
            talk('Interesting!', delay=1)
            talk('The meaning of life varies for each person. Some find purpose in relationships, others in personal achievements.', delay=1.5)
            talk(ask_user_meaning_of_life())

        elif 'am i' in command and any(word in command for word in ['handsome', 'beautiful', 'pretty', 'looking good', 'look good', 'cute']):
            talk("It is not my place to judge your appearance")
            talk("But, I think you have a great personality and that is always important.")

        elif all(word in command for word in ['people', 'you speak', 'at once']): #personal
            talk("I can speak only one people at once.")

        elif any(keyword in command for keyword in ["bye", "good bye", "goodbye", "exit", "see you", "later"]):
            talk(goodbye()) 

        elif 'joke' in command: #task
            joke()

        elif 'my birthday' in command: #user
            talk("Happy birthday to you! I hope you have a fantastic day filled with joy and celebration.")

        elif "tell me about yourself" in command:  #personal
            talk(introduce())

        elif 'hear me' in command:   #personal
            talk('Of course I can hear you.')
            talk('I was programmed to communicate with people in conversational way.')

        elif "hello" in command:   #greet
            talk(greet())

        elif 'thanks' in command or 'thank you' in command:
            talk('You are welcome.')

        elif 'know me' in command or 'remember me' in command :  #task
            if current_user_name == '':
                talk("I don't know you, please introdue your name.")
            else:
                talk(respond_to_know_name(current_user_name))

        elif "my name is" in command:  #user
            user_name = command.split("is")[-1].strip()
            update_user_name(user_name)
            talk(respond_to_name(user_name))

        elif "i am a" in command:
            user_job = command.split(" a ")[-1].strip()   #user
            update_user_job(user_job)
            talk(f"Great! I've updated your information. Are there any other details you'd like to share?") 

        elif "good morning" in command:
            talk("Good morning.")

        elif "good afternoon" in command:  #greet
            talk("Good afternoon.")

        elif "good evening" in command: 
            talk("Good evening.")

        elif "your name" in command: #personal
            talk("Hello, I am Alexa.")

        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 2)
            print(info)
            talk(pywhatkit.info(person))

        elif 'are you a robot' in command: #personal
            talk("Yes I'm a robot but I'm a good one!")
            talk("Let me prove it. How can I help you?")

        elif re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', command): #task
            talk(simple_maths(command))

        elif 'time now' in command or 'current time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')  #task
            talk('Current time is ' + time)

        elif 'find' in command and 'boyfriend' in command or 'girlfriend' in command: #personal
            talk("Finding a girlfriend or boyfriend is a personal journey that involves mutual connection and understanding.", delay=0.5)
            talk("But I can offer advice that finding the right person takes time. Be patient and enjoy the process of getting to know different people.")

        elif 'do you have a boyfriend' in command: #personal
            ask_about_boyfriend()

        else:
            conversation += command
            
            #fetch response from open AI api
            response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
            response_string = response["choices"][0]["text"].replace("\n", "")
            response_string = response_string.split(current_user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
            conversation += response_string + "\n"

            talk(response_string)