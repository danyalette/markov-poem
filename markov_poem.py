#!/usr/bin/python

import io, markovify, sys, getopt, os.path
from syllables import getSyllables

def main(argv):
    sourceText = ''
    syllableCounts = ''

    try:
        opts, args = getopt.getopt(argv,"hf:s:",["file=","syllables="])
    except getopt.GetoptError:
        throwUsageError()
    for opt, arg in opts:
        if opt == '-h':
            throwUsageError()
        elif opt in ("-f", "--file"):
            sourceText = arg
        elif opt in ("-s", "--syllables"):
            syllableCounts = arg.split(',')

    if not os.path.isfile(sourceText):
        throwUsageError()

    if not syllableCounts or [s for s in syllableCounts if not s.isdigit()]:
        throwUsageError()

    with io.open(sourceText,'r') as f:
        text = f.read()
    text_model = markovify.Text(text)

    for s in syllableCounts:
        line = generateLine(int(s), text_model)
        if line:
            print line
        else:
            print 'Error: could not generate a line where syllable count == ' + s

def throwUsageError():
    print 'Usage: python markov_poem.py -f <source_text_filepath> -s <comma,separated,syllable,count>'
    sys.exit()

def generateLine(syllables, text_model):
    for i in range(100):
        sentence = text_model.make_short_sentence(syllables*6)
        if (sentence):
            syls = getSyllables(sentence)
            if (syls == syllables):
                return sentence[:-1]

if __name__ == "__main__":
   main(sys.argv[1:])