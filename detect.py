#!/usr/bin/env python3

from collections import defaultdict
import json


# == BEGIN REPLACE ==
# Do not touch the previous line.
# This part will be replaced by a constant.  Essentially collected.json.

def digest_data():
    """
    Load collected.json and parse it.
    Only used when not auto-generated yet.
    """
    with open('collected.json', 'r') as fp:
        collected_raw = json.load(fp)
    digested = defaultdict(list)
    for (lang, wordlist) in collected_raw.items():
        for word in wordlist:
            digested[word].append(lang)
    # When replacing, I would like to substitude a plain dict,
    # and avoid constructing a defaultdict
    return dict(digested)


COLLECTED_DIGESTED = digest_data()

# Do not touch the next line.
# == END REPLACE ==

MIN_REQUIRED_CONFIDENCE = 0.01


def null_rating():
    """
    Returns a default, "no text" rating.
    Note that these will be modified by other functions.
    """
    # From lang to number of words seen.
    # Also, from key '__total__' to the total number of words.
    return defaultdict(int)


def rate_text(chunk, rating):
    """
    Update the given rating with what is found in the given text.
    Returns None.
    """
    for word in chunk.split():
        word = ''.join(filter((lambda c: c.isalnum()), word))
        rating['__total__'] += 1
        for lang in COLLECTED_DIGESTED.get(word, []):
            rating[lang] += 1


def fold_rating(rating, min_confidence=None):
    """
    Returns the most likely language and the confidence as a tuple.
    Or (None, 0.0), if the confidence was too low.
    The confidence is between 0.0 and 1.0,
    and represents the number of recognized words in that language.
    """

    def get_normal_matches(kv):
        # The multiplication only affects the '__total__' entry,
        # and resets the score (in the eyes of 'max()' to 0.
        # This never fails because there is at least one entry: '__total__'.
        return kv[1] * (kv[0] != '__total__')
    lang, matches = max(rating.items(), key=get_normal_matches)

    # Ignore any very low confidence result.
    if rating['__total__'] == 0:
        return (None, 0.0)
    confidence = matches / rating['__total__']
    if min_confidence is None:
        min_confidence = MIN_REQUIRED_CONFIDENCE
    if confidence < min_confidence:
        return (None, 0.0)

    # Yay!
    return lang, confidence


def get_language(text):
    """
    Convenience function: Analyze text, return language and confidence.
    """
    rating = null_rating()
    rate_text(text, rating)
    return fold_rating(rating)
