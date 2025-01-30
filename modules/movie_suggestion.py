import random

def suggest_movie_from_genre(genre):
    movie_suggestions = {
        "drama": ["The Godfather", "Schindler's List"],
        "sci-fi": ["Blade Runner", "The Matrix"],
        "action": ["Die Hard", "Mad Max: Fury Road", "John Wick"],
        "horror": ["Get Out", "Hereditary"],
        "comedy": ["Anchorman", "Superbad"],
        # Add more movie suggestions for each genre
    }

    if genre in movie_suggestions:
        # context["topic"] = None
        # return f"How about {random.choice(movie_suggestions[genre])}, a {genre} movie? I hope you will like it."
        return random.choice(movie_suggestions[genre])
    else:
        pass

def suggest_movie(preferred_genre=None):
    if preferred_genre != None:
        movie_title = suggest_movie_from_genre(preferred_genre)

        return f"Let me think, for {preferred_genre} movie, I recommend {movie_title} for you."
    else:
        movie_suggestions = [
            {"title": "The Shawshank Redemption", "type": "drama", "about": "It's a classic film with a powerful storyline and exceptional performances."},
            {"title": "Inception", "type": "sci-fi", "about": "It's a mind-bending thriller directed by Christopher Nolan."},
            {"title": "Ocean's Eleven", "type": "action", "about": "It is a stylish heist film with an ensemble cast led by George Clooney. The elaborate heist and witty dialogue make it a great choice."},
            {"title": "The Conjuring", "type": "horror", "about": "It is known for its effective scares and suspenseful storytelling."},
            {"title": "Dumb and Dumber", "type": "comedy", "about": "It's a classic for its silly humor and memorable moments."},
            # Add more movie suggestions here
        ]

        suggested_movie = random.choice(movie_suggestions)
        return f"I suggest watching '{suggested_movie['title']}', a {suggested_movie['type']} movie. {suggested_movie['about']}."

def get_user_preferred_genre(user_response):
    preferred_genres = ["action", "comedy", "drama", "horror", "sci-fi"]
    if any(keyword in user_response.split() for keyword in preferred_genres):
        preferred_genre = [keyword for keyword in preferred_genres if keyword in user_response.split()]
        return suggest_movie(preferred_genre[0])

def is_asking_suggest_movie(user_input):
    preferred_genres = ["action", "comedy", "drama", "horror", "sci-fi"]
    return any(keyword in user_input for keyword in preferred_genres)

def handle_negative_feedback_movie(user_response):
    # command = speech_without_computer()
    # if any(expression in command for expression in ["don't want", "no", "i am good", 'skip']):
    #     # context["topic"] = None
    #     talk("Alright! If you ever want movie suggestions again, feel free to ask.")
    # else:
    if user_response:
        return get_user_preferred_genre(user_response)
    return None
