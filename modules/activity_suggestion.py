import random

def activity_suggestion():
    reply = "We could hang out, talk, watching movies, go on adventures."
    return f"{reply}  Really, anything you can think of!"

def pick_activity(activity_user_choose):

    if activity_user_choose == 'movie':
        return "What kind of movie do you want to watch for?"
    elif activity_user_choose == 'game':
        return "What kind of game do you want to play for?"
    elif activity_user_choose == 'adventure':
        return "What kind of adventure are you in the mood for?"
    
# def adventure_type_suggestion():
    # adventures = ['hiking', 'beach', 'exploring']
    # adventure = random.choice(adventures)
    # # print(adventure)
    # # answer = suggest_adventure()
    # if adventure == 'hiking':
    #     answer = suggest_hiking_places(destination('hiking'))[0]
    # elif adventure == 'beach':
    #     answer = suggest_beach_places(destination('beach'))[0]
    # elif adventure == 'exploring':
    #     answer = suggest_explore_places(destination('exploring'))[0]
    
    # return (f"So many places we can go. May be we could go explore new city or hiking in a beautiful forest. {answer}")

def adventure_type_user_select(adventure_type):
    answer = ''

    if adventure_type == "hiking":
        places = destination('hiking')
        answer =  f"{suggest_hiking_places(places)}"
    elif adventure_type == "beach":
        places = destination('beach')
        answer = f"{suggest_beach_places(places)}"
    elif adventure_type == 'exploring':
        places = destination('exploring')
        answer = f"{suggest_explore_places(places)}"

    return answer

def destination(activity_type):
    hiking_places = {
        'Mountain Peak Trail': {'city': 'Denver', 'reason': 'You could enjoy offers stunning of panoramic views.'},
        'Mystic Forest Hike': {'city': 'Seattle', 'reason': 'You could immerse yourself in a lush, magical forest.'},
        'Coastal Cliff Expedition': {'city': 'San Francisco', 'reason': 'You could pleasure breathtaking views of the Pacific Ocean.'},
        'Wilderness Adventure Loop': {'city': 'Portland', 'reason': 'You would insterest to explore diverse ecosystems and wildlife.'},
        'Sunrise Summit Trek': {'city': 'Phoenix', 'reason': 'That would be a enjoyment to see witness a spectacular sunrise at the summit.'}
        }
    beach_places = {
        "Hawaii": {"city": "Honolulu", "reason": "There is many beautiful relaxing beaches with volcanic landscapes and outdoor activities."},
        "Miami": {"city": "USA", "reason": "It is famous for its beautiful beaches, vibrant nightlife, and art deco architecture."},
        "Phuket": {"city": "Thailand", "reason": "There is lively beach parties and so much diverse water activities experience there."},
        "Barcelona": {"city": "Spain", "reason": "There is beautiful beaches with rich cultural experiences."},
        "Cancún": {"city": "Mexico", "reason": "It is famous for its vibrant nightlife and water sports activities."},
    }
    cities_to_explore = {
        'Paris': {'landmark': 'Eiffel Tower', 'experience': 'romantic atmosphere'},
        'New York': {'landmark': 'Statue of Liberty', 'experience': 'breathtaking views'},
        'Tokyo': {'landmark': 'Tokyo Tower', 'experience': 'blend of tradition and modernity'}
    }

    if activity_type == 'hiking':
        return hiking_places
    elif activity_type == 'beach':
        return beach_places
    elif activity_type == 'exploring':
        return cities_to_explore

def suggest_hiking_places(places):
        suggested_place = random.choice(list(places.keys()))
        suggestions = []

        place = suggested_place
        city = places[place]['city']
        reason = places[place]['reason']
        suggestions.append(f"For hiking, I think {place} in {city} would be an amazing advanture. {reason}")

        return suggestions[0]

def suggest_beach_places(places):
        suggested_place = random.choice(list(places.keys()))
        suggestions = []

        place = suggested_place
        city = places[place]['city']
        reason = places[place]['reason']
        suggestions.append(f"For a fantastic beach experience, I recommend you should visiting {place} in {city}. {reason}")

        return suggestions[0]

def suggest_explore_places(places):
        suggested_place = random.choice(list(places.keys()))
        suggestions = []
        # print(places)

        place = suggested_place
        city = places[place]["landmark"]
        reason = places[place]["experience"]
        suggestions.append(f"I think visiting to {place} in {city} would be an amazing for a {reason}")

        return suggestions[0]

def suggest_adventure():
    adventure_suggestions = [
        "I think Bungee jumping off the Victoria Falls Bridge in Zambia would be hands down the most thrilling experience. It's not for the faint-hearted, but the sheer adrenaline rush might worth it!",
        "I highly recommend exploring the Amazon rainforest. The diverse wildlife, dense foliage, and the overall sense of being in the wild make it an incredible adventure.",
        "You should definitely trekking to Machu Picchu. The ancient ruins, stunning landscapes, and the sense of accomplishment at the end make it an unforgettable adventure.",
    ]
     
    return random.choice(adventure_suggestions)
