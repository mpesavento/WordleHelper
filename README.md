# WordleHelper

A dude named Wardle wrote a word puzzle for his long distance partner, and now we 
have [Wordle](https://www.powerlanguage.co.uk/wordle/), the addictive 5 
letter guessing game.

But what about those of us that can't remember all of the 5 letter words? 
The guy that is pretty horrible at Scrabble? (definitely not me, nope, not at all).

Given a set of dictionaries, find all of the 5 letter words and given exact positions
or correct letters but wrong position, find all possible words.

TODO: Bonus, rank them by commonness.


## Word lists

The one used is from here:
https://github.com/dwyl/english-words
as `word_alpha.txt`, and then reduced to only the 5 letter words.

Other unused word lists can be found here:
https://hashcat.net/forum/thread-1236.html


## Developer notes
Ann attempt was made to minimize requirements to make this as light as possible.
That means not using `numpy` or `pandas` tooling, which makes some of the algorithms easier.

