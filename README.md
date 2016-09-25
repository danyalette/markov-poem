# markov-poem

Markov-poem takes a source text and, using markov chains, generates a set of lines that have a specified number of syllables.

### Dependencies

markovify:  
`pip install markovify`  

nltk:   
`pip install nltk`  

cmudict:  
`python -m nltk.downloader cmudict`


### Usage

```
python markov_poem.py -f <source_text_filepath> -s <comma,separated,syllable,count>
```

### Examples

```
$ python markov_poem.py -s 4,4,4,4,4,4 -f ~/ulysses.txt
He brought it in
In the bright air
Please tell me so
— Don’t you forget
What will you pun
Or do you do
```

```
$ python markov_poem.py -s 5,7,5 -f ~/ulysses.txt
Couldn’t eat a beefsteak
He hoped she had ever seen
Sitting at his mouth
```

```
$ python markov_poem.py -s 6,6,6 -f ~/ulysses.txt
Across the page rustling
I was to be grownups
And still his eyes cast down
```

### Notes

- If the source text is too short, markovify will fail.
- The syllable count is quite accurate but don't expect it to be perfect.
- Lines with very many (~>30) or very few (~<3) syllables will also likely fail to generate.