def make_freq_dict(k, word_sequence):
    """
    Makes a "frequency dictionary" from a sequence of words.
    For each k-gram that appears in `word_sequence`, freq_dict[k_gram] is
    another dictionary that maps words to how often they occur after k_gram.

    :param      k:              Size of k-gram
    :type       k:              int
    :param      word_sequence:  A book, broken up into a list of strings
    :type       word_sequence:  List of strings

    :returns:   Frequency dictionary
    :rtype:     dict of dicts (str -> dict of str -> int)
    """

    # Make an empty dictionary to count frequencies using defaultdict with Counter
    freq_dict = defaultdict(Counter)

    # Iterate through the word_sequence to generate k-grams and their next words
    for i in range(len(word_sequence) - k):
        # Create the k-gram as a tuple of the previous k words
        k_gram = tuple(word_sequence[i:i+k])

        # The next word after the k-gram
        next_word = word_sequence[i + k]

        # Update the frequency count for the next word following the k-gram
        freq_dict[k_gram][next_word] += 1

    return freq_dict

def predict_next_word(this_kgram, freq_dict):
    """
    Randomly picks the next word given the previous k-gram, using the frequency
    of possible next words according to `freq_dict`. If `freq_dict` does not
    contain the k-gram, return None.

    :param      this_kgram:  The current k-gram (tuple of words)
    :type       this_kgram:  tuple of strings
    :param      freq_dict:   A frequency dictionary
    :type       freq_dict:   dict of dicts (tuple -> dict of string -> int)

    :returns:   The next word, or None
    :rtype:     string or None
    """

    # Check if the k-gram exists in the frequency dictionary
    if this_kgram not in freq_dict:
        return None

    # Get the possible next words and their counts
    next_word_counts = freq_dict[this_kgram]

    # Use random.choices to select the next word based on the frequency
    next_words = list(next_word_counts.keys())
    probabilities = list(next_word_counts.values())

    return random.choices(next_words, probabilities)[0]


def predict_paragraph(start_kgram, k, freq_dict, gen_length=300):
    """
    Given a starting k-gram, this randomly generates `gen_length` many new
    words to form a paragraph of text consistent with `freq_dict`. If the last
    word in the book is generated (i.e. if `predict_next_word` returns None),
    then this will short-circuit and stop generating words early.

    :param      start_kgram:  The k-gram to start from.
    :type       start_kgram:  tuple of strings
    :param      k:            k-gram size
    :type       k:            int
    :param      freq_dict:    A frequency dictionary
    :type       freq_dict:    dict of dicts (tuple -> dict of string -> int)
    :param      gen_length:   The number of words to generate.
    :type       gen_length:   int

    :returns:   A generated paragraph as a list of words.
    :rtype:     List of string
    """

    # Initialize the generated paragraph with the starting k-gram
    gen_para = list(start_kgram)

    # Generate words until the desired length is reached
    current_kgram = start_kgram
    for _ in range(gen_length - k):
        # Predict the next word
        next_word = predict_next_word(current_kgram, freq_dict)

        # If no next word is found, stop generation
        if next_word is None:
            break

        # Append the next word to the paragraph
        gen_para.append(next_word)

        # Update the k-gram to include the new word
        current_kgram = tuple(gen_para[-k:])

    return gen_para

# Pick k and make a frequency dictionary from Metamorphosis.
k_test = 3
freq_dict_test = make_freq_dict(k_test, metamorphosis)

# Pick a random starting k-gram from the freq_dict.
start_test = random.choice(list(freq_dict_test.keys()))

# Alternatively, pick the start of the book as the first k-gram.
# start_test = tuple(metamorphosis[0:k_test])

# Generate a paragraph, and print it.
gen_paragraph = predict_paragraph(start_test, k_test, freq_dict_test)

# Join the generated words into a readable paragraph.
print("Generated Paragraph:")
print(" ".join(gen_paragraph))
