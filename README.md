# ear

> Listen to the words and reliably detect the human language in which they are written.

Assume you have some text.  Any text.  And you want to determine the language.

`ear` listens to what you give it.  Well, it reads it,
but the metaphor works better with "listening" than "looking".

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [Contribute](#contribute)

## Background

This was mostly motivated because someone said "I'm gonna use Markov chains!".
I think this is a much simpler, far more reliable way to do it.

## Install

This is a drag-and-drop library.  Put it where you need it, and be happy.
Don't forget `digested.json.xz`.
If you dislike the load time, re-compress it to something else.

## Usage

For small passages of text, just call `ear.get_language(text)`.

The result will be an ISO 639-2 code, optionally followed by `-` and the country code.
See `wortschatz-uni-leipzig-de.ls` for the list of known languages.

For large bodies of text (when memory starts to become an issue, or you need parallelism for some reason),
you may want to process it by parts:

```py3
parts = ...  # Input
rating = ear.null_rating()
for chunk in parts:
    ear.rate_text(chunk, rating)
lang = ear.simplify_rating(rating)
print('Language seems to be ' + lang)  # Output
```

Just use it!
The complexity lies in collecting the data and applying it properly.
Usage is just a function call.

## State of the ear

All the major languages are properly recognized.

The folder `tests/` contains the frontpages of all wikipedias with at least 1 million articles.
This is my definition of "major language".

Given that I didn't special-case these languages, and that I tried to avoid Wikipedia when picking word-files,
I believe that `ear` should reasonably do well for many other languages.

### Detailed test results

- ceb: ceb (256), tgl (172) → Reasonable; similar language
- de: deu (207), gsw-ch (175) → Reasonable; similar language
- en: eng (567), tgl (497) → Meh, dirty word source (claims that words like "birthday" and "The" and "commission" are Tagalog.)
- es: spa (578), arg (494) → Reasonable; similar language
- fr: fra (498), ltz (307) → Reasonable; similar language
- it: ita (780), arg (405) → Reasonable; sufficiently large distance
- ja: jpn (16), zho (5) → Not great; need more samples of Japanese
- nl: nld (362), lim-nl (344), fry (299) → Reasonable; to some extent they are the same language anyway
- pl: pol (337), slk (113) → Reasonable; sufficiently large distance
- pt: por (596), glg (437), pus (422) → Huh.  No idea
- ru: rus (364), ukr (152) → Reasonable; sufficiently large distance
- sv: swe (489), nor (357), dan (268) → Reasonable; sufficiently large distance, but also similar language
- vi: vie (601), lus (30) → Reasonable; Reasonable; sufficiently large distance
- war: ceb (85), war (71), tgl (66) → Reasonable; similar language
- zh: zho (5) → Not great; need more samples of Chinese

## TODOs

* Make the installation even easier.
* Get better samples for Chinese, Japanese, Tagalog
* Understand why Portuguese, Gaelician, and Pashto seem to be so similar

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/ear/issues/new) or submit PRs.
