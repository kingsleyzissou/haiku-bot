def post_process(text):
    """
    Remove white space and capitalize text.
    This method is a little bit hacky, but
    it works
    """
    text = ' '.join(text)  # remove whitespace
    text = text.split()  # split again
    text = ' '.join(text)  # and repeat
    text = text.rstrip()  # remove trailing whitespace
    return text  # return capitalized phrase
