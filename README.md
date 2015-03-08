# twobirds-solver
A brute force solver for twobirds puzzles (and regular games) 

This is a simple solver for the word game twobirds. It works with the same dictionaries as the [wordbase-solver](https://github.com/relet/wordbase-solver).
It is not completed, as I find the game not actually that interesting to analyze.

## Game files 

As with the wordbase solver, the game supports arbitrary size game boards. They consist of lines of lower case letters. 
The following special characters are supported:

 * A dot `.` represents a blank tile.
 * An uppercase letter represents a bonus (golden) tile.

## Puzzles

Currently, there are two types of python scripts:

    ./puzzle.py game
    
This will solve a daily puzzle based on a game file in the game files directory. It will use brute force on the game board to find the longest N words. It will simulate playing each of these words, shrink the board accordingly and repeat the process until there are no possible moves left.
Each of the results is scored according to how many letters have been used, the length of the words used, and including a bonus when using all letters. The best scoring game is then displayed.

E.g.:

    ./puzzle.py 7
    49           
    ['-', u'SPAKE', u'TET', u'HOURLY', u'MUMMERY', u'SCULPED']  
    
Plays the daily puzzle for March 7, 2015 - English. The game is solved completely when playing the words SCULPED, MUMMERY, etc. in this order. Ambiguous moves may occur, but since the game allows trial and error, you may just want to play these out.
This is a perfect game, yielding 151 points when including the letter scores and 10 point bonus tiles. 

The scripts nopuz.py and depuz.py play a game using the Norwegian and German dictionaries respectively. For the puzzle games, that is the only change.

## Regular games

The other script just displays the highest scoring words for a given game.

E.g.:

    ./regular.py tut
    GROWLINESS 31
    CHLORINES 28
    CHLORINES 28
    LOWLINESS 27
    UNMELLOW 27                            

This script takes into account bonus tiles (capital letters in the game file) and the actual point value of a letter. 

The corresponding scripts for Norwegian and German are noreg.py and dereg.py. These have unicode support for the respective special characters and adjusted (but currently not correct) letter values.
