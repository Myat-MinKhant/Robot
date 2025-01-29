from nltk import CFG, ChartParser

# Define an extended context-free grammar for NLG
grammar = CFG.fromstring("""
    S -> NP VP | WhNP VP | WhNP VP T | WhNP VP Weather
    NP -> Det N
    VP -> V NP
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog'
    V -> 'chased' | 'bit'
    WhNP -> 'what' | 'who' | 'where' | 'is'
    T -> 'today'
    Weather -> 'weather'
""")

def generate_sentence(grammar, user_input):
    # Create a parser based on the grammar
    parser = ChartParser(grammar)

    # Tokenize the user input (you might want to use a more sophisticated tokenizer)
    user_tokens = user_input.lower().split()

    # Generate a sentence using the parser and user input
    sentence = list(parser.parse(user_tokens))

    # Flatten the generated sentence into a string
    return ' '.join(str(item) for item in sentence[0].leaves())

if __name__ == "__main__":
    # Get user input
    user_input = input("Ask a question: ")

    # Generate a sentence using the defined grammar and user input
    generated_sentence = generate_sentence(grammar, user_input)

    # Print the generated sentence
    print("Generated Sentence:", generated_sentence)
