#!/usr/bin/python

import io, markovify, sys, getopt, os.path
from syllables import getSyllables
import json
import string
import random

def makeId(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getSourceCacheId(cacheIndex, source):
    cacheId = None
    for i in cacheIndex:
        if i[0] == source:
            cacheId = i[1]
    return cacheId

def removeDuplicateCachedModels(cacheIndex, source):
    for i in cacheIndex:
        if i[0] == source:
            cacheIndex.remove(i)

def main(argv):
    sourceText = ''
    syllableCounts = ''
    cache = False

    try:
        opts, args = getopt.getopt(argv,"hf:s:c",["file=","syllables=", "cache="])
    except getopt.GetoptError:
        throwUsageError()
    for opt, arg in opts:
        if opt == '-h':
            throwUsageError()
        elif opt in ("-f", "--file"):
            sourceText = arg
        elif opt in ("-s", "--syllables"):
            syllableCounts = arg
        elif opt in ("-c", "--cache"):
            cache = True

    print generatePoem(syllableCounts, sourceText, cache)


def generatePoem(syllableCounts, sourceText, cache):

    result = []
    syllableCounts = syllableCounts.split(',')

    if not os.path.isfile(sourceText):
        throwUsageError()
    if not syllableCounts or [s for s in syllableCounts if not s.isdigit()]:
        throwUsageError()

    # get list of cached sources
    with io.open('data/sources.json','r') as f:
        text = f.read()
        if text != '':
            sourceModelIndex = json.loads(text)
        else:
            sourceModelIndex = []

    # get id of current source's cachec
    sourceCacheId = getSourceCacheId(sourceModelIndex, sourceText)

    # if ww to use cache, and current source is cached:
    if cache and sourceCacheId:
        with io.open('data/' + sourceCacheId + '.json','r') as f:
            data = json.load(f)
            text_model = markovify.Text.from_json(data)
    else:
        with io.open(sourceText,'r') as f:
            text = f.read()
        text_model = markovify.Text(text)
        model_json = text_model.to_json()

        # save new markov model to cache
        sourceId = makeId()
        with io.open('data/sources.json','w',encoding="utf-8") as indexFile:
            removeDuplicateCachedModels(sourceModelIndex, sourceText)
            sourceModelIndex.append((sourceText,sourceId))
            indexFile.write(unicode(json.dumps(sourceModelIndex, ensure_ascii=False)))
        with open('data/' + sourceId + '.json', 'w') as outFile:
            json.dump(model_json, outFile)

    for s in syllableCounts:
        line = generateLine(int(s), text_model)
        if line:
            result.append(line)
        else:
            result.append('Error: could not generate a line where syllable count == ' + s)

    return '\n'.join(result)

def throwUsageError():
    print 'Usage: python markov_poem.py -f <source_text_filepath> -s <comma,separated,syllable,count> [-c (use cached markov model of source text)]'
    sys.exit()

def generateLine(syllables, text_model):
    for i in range(300):
        sentence = text_model.make_sentence()
        if (sentence):
            syls = getSyllables(sentence)
            if (syls == syllables):
                return sentence[:-1]

if __name__ == "__main__":
   main(sys.argv[1:])
