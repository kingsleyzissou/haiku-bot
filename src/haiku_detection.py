import syllapy

DEFAULT_RESPONSE = False, [], [], [], None

def get_count(items):
    """
    Count the number of syllables in a list
    of words

    :items: list of strings
    """
    return sum([syllapy.count(t) for t in items])

def loop_condition(first_count, second_count, third_count):
    """
    Custom function used to break out of while loop

    :first_count: number of syllables in first line
    :second_count: number of syllables in second line
    :third_count: number of syllables in third line
    """
    return first_count <= 5 and second_count <= 7 and third_count < 5

def extract_haiku(text, strict = False):
    """
    Custom function to extract a haiku from a body of a text

    :text: body of text to be checked
    :strict: when strict mode is disabled the entire text is checked if it contains a haiku, 
             otherwise the whole body of text has to be a match
    """
    cond, first, second, third, handle = DEFAULT_RESPONSE
    sylls = get_count(text)
    items = text.copy()
    if sylls == 0:
        return DEFAULT_RESPONSE
    if items[0] == 'RT':
        items.pop(0)
        handle = items.pop(0)
    if sylls < 17:
        return DEFAULT_RESPONSE
    if strict and sylls != 17:
        return DEFAULT_RESPONSE
    while(not cond and len(items) > 0):
        cond, first, second, third = check_sequence(items)
        items.pop(0)
    return cond, first, second, third, handle

def check_sequence(items):
    """
    This function iterates through a body of text one
    word at a time. And builds up each line of the haiku
    one line at a time
    """
    first, second, third = [], [], []
    first_count, second_count, third_count = 0, 0, 0
    ## since we are removing items from the array, we want to make
    ## a clone so we don't modify the original array
    clone = items.copy()
    ## make sure that we aren't getting syllable counts
    ## greater than what we need
    while(loop_condition(first_count, second_count, third_count) and len(clone) > 0):
        if (first_count < 5):
            first.append(clone.pop(0))
            first_count = get_count(first)
        if (first_count == 5 and second_count < 7 and len(clone) > 0):
            second.append(clone.pop(0))
            second_count = get_count(second)
        if (first_count == 5 and second_count == 7 and third_count < 5 and len(clone) > 0):
            third.append(clone.pop(0))
            third_count = get_count(third)
    ## this condition checks if each line of the haiku is a match
    if (first_count == 5 and second_count == 7 and third_count == 5):
        ## rule-based exclusion
        exclude = [
            'the', 'my', 'in', 'to', 'for', 'what', 
            'when', 'where', 'whenever', 'it', 'by',
            'and', 'we', 'he', 'they', 'I', 'of'
        ]
        if third[-1:][0].lower() in exclude:
            return DEFAULT_RESPONSE[:4]
        return True, first, second, third
    return DEFAULT_RESPONSE[:4]