#!/usr/bin/env python3

from collections import defaultdict
import json
import lzma
import sys


def load_data():
    with lzma.open('digested.json.xz', 'rt') as fp:
        return json.load(fp)


COLLECTED_DIGESTED = load_data()
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
    if rating['__total__'] == 0 or lang == '__total__':
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


def run(args):
    if args == ['--help']:
        print('USAGE: ear.py { --reason | --no-reason | FILE }*')
        return
    if args == []:
        args = ['-']
    print_reason = False
    for arg in args:
        if arg == '--reason':
            print_reason = True
            continue
        if arg == '--no-reason':
            print_reason = False
            continue
        if arg == '-':
            text = sys.stdin.read()
        else:
            with open(arg, 'r') as fp:
                text = fp.read()
        if print_reason:
            rating = null_rating()
            rate_text(text, rating)
            lang, confidence = fold_rating(rating)
            result = list(rating.items())
            result.sort(reverse=True, key=lambda e: e[1])
            reason = ', or '.join('{} ({})'.format(rname, rconf)
                                  for (rname, rconf) in result)
            print('{}: probably "{}" ({}).  Reason: {}'.format(
                arg, lang, confidence, reason))
        else:
            lang, confidence = get_language(text)
            print('{}: probably "{}" ({}).'.format(arg, lang, confidence))


if __name__ == '__main__':
    run(sys.argv[1:])
