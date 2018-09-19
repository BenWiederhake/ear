#!/usr/bin/env python3

import ear
import os


TEST_RESOURCE_DIR = 'tests'


def run_tests():
    results = dict()
    for filename in os.listdir(TEST_RESOURCE_DIR):
        if not filename.endswith('.txt'):
            continue
        name_part = filename[:-len('.txt')]
        fullname = os.path.join(TEST_RESOURCE_DIR, filename)
        with open(fullname, 'r') as fp:
            text = fp.read()
        rating = ear.null_rating()
        ear.rate_text(text, rating)
        result = list(rating.items())
        result.sort(reverse=True, key=lambda e: e[1])  # decreasing confidence
        results[name_part] = (result, ear.fold_rating(rating))
    return results


def print_results(results):
    results = list(results.items())
    results.sort(key=lambda e: e[0])  # increasing name
    for (name, (rating, guess)) in results:
        print('=====\n{}: probably {}.\n\tReason: {}'.format(name, guess, ', or '.join('{} ({})'.format(rname, rconf) for (rname, rconf) in rating)))

# Correctly recognized:
# de
# en
# es
# fr
# it
# ja
# pl
# pt
# ru
# vi

# Incorrectly recognized:
# ceb - Not recognized at all!  Hausa is completely wrong, Filipino is close enough.
# nl - Not recognized at all!  Huh?  
# sv - Huh?  Hausa (340) vs Swedish (94).
# war - Missing from dataset; essentially Filipino
# zh - Not recognized at all!

# Recommendation: For collect.py, I should use a data source that also
# provides conjugated words.

if __name__ == '__main__':
    print_results(run_tests())
