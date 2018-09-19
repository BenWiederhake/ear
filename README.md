# ear

> Listen to the words and reliably detect the human language in which they are written.

Assume you have some text.  Any text.  And you want to determine the language.

`ear` listens to what you give it.  Well, it reads it,
but the metaphor works better with "listening" than "looking".

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [State of the ear](#state-of-the-ear)
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

### Usage as a library

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
lang, confidence = ear.fold_rating(rating)
print('Language seems to be ' + lang)  # Output
```

Just use it!
The complexity lies in collecting the data and applying it properly.
Usage is just a function call.

### Usage as a stand-alone executable

Due to the long load time (seconds), this may be a bad idea.

But you can use it like this:

```
$ ./ear.py README.md
README.md: probably "eng" (0.4759299781181619).
```

And to show off the other features:

```
$ ./ear.py --reason - < README.md
-: probably "eng" (0.4759299781181619).  Reason: __total__ (914), or eng (435), or tgl (380), or knn-in (377), or ceb (350), or lus (335), or cym (331), or pap (327), or jav-id (322), or ltz (321), or lim-nl (316), or ast (313), or som (309), or arg (308), or dan (308), or mri-nz (304), or ron (297), or sqi (290), or xho (289), or swa (287), or gle (286), or msa (276), or als-sqi (274), or por (264), or fry (264), or tur (260), or slv (259), or ita (258), or mlt (249), or isl (249), or tam (235), or war (233), or amh (227), or est (223), or nor (219), or uzb (218), or afr (211), or rus (210), or epo (210), or hin (209), or gsw-ch (207), or bul (202), or mon (197), or aze (192), or guj (192), or fra (184), or hrv (180), or ind (180), or gom (168), or swe (164), or bos (162), or cat (161), or vie (160), or spa (155), or slk (147), or pol (145), or sna-zw (143), or hat-ht (142), or ces (141), or glg (139), or cmn (137), or azj-az (136), or fao (136), or zul (134), or hun (133), or tha (132), or fin (121), or lit (118), or hye (114), or jpn (113), or yid (112), or lav (112), or lug (111), or pus (110), or srp-rs (109), or eus (108), or kal (106), or zho (105), or ell (105), or kor (97), or nld (87), or fas (87), or tgk (87), or heb (83), or bak (79), or kan (78), or pes-ir (77), or ara (73), or kir (72), or pan-in (69), or urd (69), or deu (68), or kat (66), or san (66), or mkd (58), or kaz (50), or bel (49), or ukr (46), or mal (34), or tat (33), or tuk-tm (31), or div (31), or ben (27), or tel (11), or mar (3)
```

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
