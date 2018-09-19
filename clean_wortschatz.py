#!/usr/bin/env python3

from collections import defaultdict
import json
import os


WORTSCHATZ_DIR = 'wortschatz-uni-leipzig-de'


def read_words(filename):
    with open(filename, 'r') as fp:
        data = fp.read()
    words = []
    for (lineno, line) in enumerate(data.split('\n')):
        if line == '':
            continue
        parts = line.split('\t')
        assert len(parts) in {3, 4}, (filename, lineno, line)
        words.extend(parts[1].split(' '))
    return words


def clean_words(words):
    cleaned_words = set()
    for word in words:
        word = ''.join(c for c in word.lower() if c.isalpha())
        if 'http' in word or 'www' in word or word == '':
            # Sigh.
            continue
        cleaned_words.add(word)
    return list(cleaned_words)


def build_collected():
    collected = dict()
    for filename in os.listdir(WORTSCHATZ_DIR):
        print(filename)
        lang = filename.split('_')[0]
        assert lang not in collected, lang
        path = os.path.join(WORTSCHATZ_DIR, filename)
        dirty_words = read_words(path)
        cleaned_words = clean_words(dirty_words)
        collected[lang] = cleaned_words
    return collected


def digest_collected(collected):
    digested = defaultdict(list)
    for (lang, wordlist) in collected.items():
        for word in wordlist:
            digested[word].append(lang)
    # When replacing, I would like to substitute a plain dict,
    # and avoid constructing a defaultdict
    return dict(digested)


def run():
    collected = build_collected()
    digested = digest_collected(collected)
    with open('/tmp/digested.json', 'w') as fp:
        json.dump(digested, fp, separators=(',', ':'), sort_keys=True)


if __name__ == '__main__':
    run()
