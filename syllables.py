#!/usr/bin/python

from nltk.corpus import cmudict
from utils import *

d = cmudict.dict()

def cmuSyllables(word):
    w = word.lower()
    if w in d:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[w]][0]
    else:
        return 0

def estimateSyllables(word):
    count = 0
    last_was_vowel = False

    if word[-3:] in ['ded', 'ted']:
        word = word[:-3]
        count += 1
    if word[-2:] == 'ed':
        word = word[:-2]
    if word[-1:] == 's':
        word = word[:-1]
    if word[-1:] == 'e':
        if word[-3:] in ['ble', 'cle', 'dle', 'fle', 'gle', 'kle']:
            word = word[:-3]
            count += 1
        elif vowelCount(word) > 1:
            word = word[:-1]
    if word[-3:] == 'n\'t':
        word = word[:-3]
        count += 1
    for c in word:
        if isVowel(c):
            if not last_was_vowel:
                count += 1
            last_was_vowel = True
        else:
            last_was_vowel = False
    return count

def getSyllables(sentence):
    count = 0
    for word in sentenceToWords(sentence):
        cs = cmuSyllables(stripPunctuation(word))
        if cs:
            count += cs
        else:
            count += estimateSyllables(stripPunctuation(word))
    return count
