# ear

> Listen to the words and reliably detect the human language in which they are written.

Assume you have some text.  Any text.  And you want to determine the language.

`ear` listens to what you give it.  Well, it reads it,
but the metaphor works better with "listening" instead of "looking at it".

This was mostly motivated because someone said "Oh I know!  I'm gonna use Markov chains!".
I think this is a much simpler, far more reliable way to do it.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [Contribute](#contribute)

## Background

Example: you have some kind of input, and for further processing (or proper display or whatever)
you would like to know the human language of it.

## Install

This is a drag-and-drop library.  Put it where you need it, and be happy.

More specifically:
In other words: Copy `ear-db.json`, or hard-code it in the appropriate place in `ear.py`.
Then, copy `ear.py` into your project and use it like it's your own code.

## Usage

For small passages of text, just call `ear.get_language(text)`.

For large passages (when memory starts to become an issue, or you need parallelism for some reason),
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

## TODOs

* Make the installation even easier.
For example, let `construct.py` merge `ear.py` and `ear-db.json` into `dist/ear-with-batteries.py` or something.

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/ear/issues/new) or submit PRs.
