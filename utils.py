#!/usr/bin/python

import string, re

def vowelCount(word):
    count = 0
    for c in word:
        if c in 'aeiouy':
            count += 1
    return count

def isVowel(c):
    if c:
        return c.lower() in 'aeiouy'

def stripPunctuation(str):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in str if ch not in exclude)

def sentenceToWords(sentence):
    return re.split(ur'[ +-]', sentence)
