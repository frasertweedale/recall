recall
======

recall is a simple recall/concentration game client that plays the
game implemented by https://github.com/frasertweedale/recall-server
or by other services implementing the same API.  It also provides a
local game mode.

The client provides a curses interface for playing the game but if
you are lazy you can let a built-in automatic mode with a perfect
memory play the game for you.


Instructions
------------

recall requires Python 2.7.  There is no install script (yet), but
you can run the client in-place.  This guide assume you are using
virtualenv.

First download recall and install the dependencies:

    mkvirtualenv recall
    pip install requests
    git clone https://github.com/frasertweedale/recall.git
    cd recall

To run the client (interactive mode):

    python -m recall --url "http://base-url-for-the-game-server"

To run the automatic player, supply `--auto`.  If you want to play a
local game instead of playing on a recall server, supply `--local`.
