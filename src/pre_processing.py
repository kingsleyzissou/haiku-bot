import re
import string
import spacy
import syllapy

nlp = spacy.load('en_core_web_sm')

def remove_emojis(text):
    """ 
    Remove all emojis from text

    https://stackoverflow.com/a/49146722/330558
    """
    pattern = re.compile(
        pattern = "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
        "]+", flags = re.UNICODE
    )
    return pattern.sub(r'', text)

def remove_punctiation(text):
    """
    Remove punctiation from piece of text
    """
    text = [t for t in text if t not in string.punctuation]
    text = [t for t in text if t not in ['...']]
    return text

def remove_other(text):
    """
    Remove hyperlinks and hashtags (useful for tweets)

    https://stackoverflow.com/q/62788640 
    """
    text = re.sub(r'https?:\/\/.*\/\w*', '', text)
    text = re.sub(r'#\w*', '', text)
    return text

def tokenize(text):
    """
    Get the nlp tokens
    """
    return [t.text for t in nlp(text)]

def pre_process(text):
    """
    Pre-processing pipeline to return
    a clean, tokenized piece of text
    and the associated syllables
    """
    text = remove_emojis(text)
    text = remove_other(text)
    text = tokenize(text)
    text = remove_punctiation(text)
    syllables = [syllapy.count(t) for t in text]
    return text, syllables