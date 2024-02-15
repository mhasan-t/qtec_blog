import enchant


def autocorrect_string(string):
    checker = enchant.Dict("en_US")  # or any other language you prefer
    words = string.split()
    corrected_words = [checker.suggest(word)[0] if not checker.check(word) else word for word in words]

    return ' '.join(corrected_words)
