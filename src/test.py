from pre_processing import pre_process
from haiku_detection import extract_haiku

if __name__ == "__main__":
    lorem = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
    test = """the first cold shower even the monkey seems to want a little coat of straw"""
    text = """An old silent pond... A frog jumps into the pond, splash! Silence again."""

    ## preprocess the text, remove punctuation
    ## and tokenize (using nlp)
    text, syllables = pre_process(lorem)

    res, first, second, third = extract_haiku(text, True)
    print(res, first, second, third)