import syllapy
import string
import re
import spacy
# import numpy as np

nlp = spacy.load('en_core_web_sm')

lorem = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"

# sentence = "The quick brown fox jumped over the lazy dog"

# count = syllables.estimate(sentence)

# print(count)


# text = u'This is a smiley face \U0001f602'
# print(text) # with emoji

def remove_emojis(text):
    """ 
    https://stackoverflow.com/a/49146722/330558
    """
    pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return pattern.sub(r'',text)


tokens = nlp(remove_emojis(lorem))
syllables = [syllapy.count(token.text) for token in tokens]



# print([token.text for token in tokens])

# ontrack = True

# for t, s in zip(tokens[:10], syllables[:10]):
#     print(t, s)

# for t, s in zip(tokens[:10], syllables[:10]):
#     print(t, s)
# first_line = []
# for i in range(len(t)):
# while (len(first_line) < 6):

# print("voluptatem", syllapy.count("voluptatem"))

def check_count(first_line, second_line, third_line):
    return sum(first_line) == 5 and sum(second_line) == 7 and sum(third_line) == 5


length = 10

# ts = tokens[:10]

# print(tokens[:10])

def adjacent_good(start, limit):
    temp, count = [], 0
    for i in range(start, length):
        temp.append(tokens[i].text)
        count = sum([syllapy.count(t) for t in temp])
        if (count >= limit): break
    return count == limit

def first_layer(start, current, items):
    count = sum([syllapy.count(t) for t in items])
    if (count < 5 and current == length - 1):
        return []
    if (count > 5):
        return first_layer(start + 1, start + 1, [])
    if (count == 5):
        if (adjacent_good(current, 7)):
            # if (adjacent_good(current + 7, 5)):
            second = next_layer(current, current, [], 7)
            # third = next_layer(current + 7, current + 7, 5)
            print(items, second)
            return items
        return first_layer(start + 1, start + 1, [])
    items.append(ts[current].text)
    return first_layer(start, current + 1, items)

def next_layer(start, current, items, limit):
    count = sum([syllapy.count(t) for t in items])
    if (count > limit):
        return next_layer(start + 1, start + 1, [], limit)
    if (count == limit):
        return items
    if (current < length):
        items.append(ts[current].text)
        return next_layer(start, current + 1, items, limit)
    return []

def third_layer(start, current, items):
    count = sum([syllapy.count(t) for t in items])
    if (count > 5):
        return third_layer(start + 1, start + 1, [])
    if (count == 5):
        return items
    if (current < length):
        items.append(ts[current].text)
        return third_layer(start, current + 1, items)
    return items

# items = first_layer(0, 0, [])

# print(items)


def loop_condition(first_count, second_count, third_count):
    return first_count <= 5 and second_count <= 7 and third_count < 5


test = """the first cold shower even the monkey seems to want a little coat of straw"""
test = """the first cold shower even the """

test = """An old silent pond... A frog jumps into the pond, splash! Silence again."""

""" Naive approach """

def is_haiku(text):
    cond, first, second, third = False, [], [], []
    items = [t for t in nlp(remove_emojis(text))]
    items = [t for t in items if t.text not in string.punctuation]
    sylls = [syllapy.count(t.text) for t in items]
    if (sum(sylls) < 17):
        return cond, first, second, third
    while(not cond and len(items) > 0):
        cond, first, second, third = check_sequence(items)
        items.pop(0)
    return cond, first, second, third

def check_sequence(items):
    first, second, third = [], [], []
    first_count, second_count, third_count = 0, 0, 0
    clone = items.copy()
    while(loop_condition(first_count, second_count, third_count) and len(clone) > 0):
        if (first_count < 5):
            first.append(clone.pop(0))
            first_count = sum([syllapy.count(t.text) for t in first])
        if (first_count == 5 and second_count < 7):
            # print(first, first_count, second, second_count)
            second.append(clone.pop(0))
            second_count = sum([syllapy.count(t.text) for t in second])
            print(first, first_count, second, second_count)
        if (first_count == 5 and second_count == 7 and third_count < 5):
            print(first, first_count, second, second_count, third, third_count)
            third.append(clone.pop(0))
            third_count = sum([syllapy.count(t.text) for t in third])
        # print(first, first_count, second, second_count, third, third_count)
    if (first_count == 5 and second_count == 7 and third_count == 5):
        return True, first, second, third
    return False, [], [], []


text = nlp(test)
print(text)

# def serialize_string():


# for t in text:
#     print(t.text)
#     print(t.text in '\u2026')
#     print(t.text == '\u2026')
#     print(t.text == '...')
#     print()


# for t in nlp()

# c, f, s, t = is_haiku(test)
# print(c, f, s, t)