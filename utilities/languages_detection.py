from langdetect import detect
import re

# Function to check if the text contains only English words
def is_all_english(text):
    return re.fullmatch(r"[A-Za-z0-9\s,.!?'-]+", text) is not None

# Function to check if Burmese characters exist in the text
def contains_burmese(text):
    burmese_pattern = re.compile(r"[\u1000-\u109F]")
    return bool(burmese_pattern.search(text))

# Function to detect the primary language
def detect_language(text):
    if is_all_english(text):
        return "eng_Latn"  # English-only input
    if contains_burmese(text):
        return "mya_Mymr"  # Burmese detected
    try:
        return detect(text)  # Detect other languages
    except:
        return "unknown"

