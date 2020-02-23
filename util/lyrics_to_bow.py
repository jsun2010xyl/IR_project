# https://github.com/tbertinmahieux/MSongsDB/blob/master/Tasks_Demos/Lyrics/lyrics_to_bow.py
import os
import sys
try:
    from stemming.porter2 import stem
except ImportError:
    print('You need to install the following stemming package:')
    print('http://pypi.python.org/pypi/stemming/1.0')
    sys.exit(0)


def lyrics_to_bow(lyrics):
    """
    Main function to stem and create bag of words.
    It is what we used for the musiXmatch dataset.
    It is heavily oriented towards English lyrics, we apologize for that.
    INPUT
        lyrics as a string
    RETURN
        dictionary word -> count
        or None if something was wrong (e.g. not enough words)
    """
    # remove end of lines
    lyrics_flat = lyrics.replace('\r', '\n').replace('\n', ' ').lower()
    lyrics_flat = ' ' + lyrics_flat + ' '
    # special cases (English...)
    lyrics_flat = lyrics_flat.replace("'m ", " am ")
    lyrics_flat = lyrics_flat.replace("'re ", " are ")
    lyrics_flat = lyrics_flat.replace("'ve ", " have ")
    lyrics_flat = lyrics_flat.replace("'d ", " would ")
    lyrics_flat = lyrics_flat.replace("'ll ", " will ")
    lyrics_flat = lyrics_flat.replace(" he's ", " he is ")
    lyrics_flat = lyrics_flat.replace(" she's ", " she is ")
    lyrics_flat = lyrics_flat.replace(" it's ", " it is ")
    lyrics_flat = lyrics_flat.replace(" ain't ", " is not ")
    lyrics_flat = lyrics_flat.replace("n't ", " not ")
    lyrics_flat = lyrics_flat.replace("'s ", " ")
    # remove boring punctuation and weird signs
    punctuation = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
                   '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*')
    for p in punctuation:
        lyrics_flat = lyrics_flat.replace(p, '')
    words = filter(lambda x: x.strip() != '', lyrics_flat.split(' '))
    # stem words
    words = map(lambda x: stem(x), words)
    bow = {}
    for w in words:
        if not w in bow.keys():
            bow[w] = 1
        else:
            bow[w] += 1
    # remove special words that are wrong
    fake_words = ('>', '<', 'outro~')
    bowwords = bow.keys()
    for bw in bowwords:
        if bw in fake_words:
            bow.pop(bw)
        elif bw.find(']') >= 0:
            bow.pop(bw)
        elif bw.find('[') >= 0:
            bow.pop(bw)
    # not big enough? remove instrumental ones among others
    # if len(bow) <= 3:
    #     return None
    # done
    return bow
