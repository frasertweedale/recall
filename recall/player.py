class Player(object):
    """Recall game player.

    A player takes a game (as a constructor argument).  When
    ``play`` is called (no arguments) the game is played to
    completion and the result of the game is returned.

    """
    def __init__(self, game):
        self.game = game
        self.cards = {(x, y) for x in range(game.x) for y in range(game.y)}
        self.memory = {}
        self.matches = set()

    def play(self):
        while not self.in_end_state():
            guess = self.choose_cards()
            a, b = self.game.guess(guess)
            if a != b:
                self.match_or_remember(a, guess[0])
                self.match_or_remember(b, guess[1])
            print self.cards
            print self.matches
            print self.memory
            print
        return self.game.end(self.choose_cards())

    def match_or_remember(self, value, card):
        if value in self.memory:
            self.matches.add((self.memory.pop(value), card))
        else:
            self.memory[value] = card

    def choose_cards(self):
        if self.matches:
            return self.matches.pop()
        else:
            return self.cards.pop(), self.cards.pop()

    def in_end_state(self):
        """Return True iff in an end state."""
        return not self.memory and (
            (len(self.cards) == 2 and len(self.matches) == 0)
            or (len(self.matches) == 1 and len(self.cards) == 0)
        )
