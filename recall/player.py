import re


class EndGameException(Exception):
    pass


class Player(object):
    """Recall game player.

    A player takes a game (as a constructor argument).  When
    ``play`` is called (no arguments) the game is played to
    completion and the result of the game is returned.

    """
    def __init__(self, game):
        self.game = game

    def play(self):
        try:
            while True:
                guess = self.choose_cards()
                a, b = self.game.guess(guess)
                if a != b:
                    self.notify_nonmatch(a, guess[0])
                    self.notify_nonmatch(b, guess[1])
                else:
                    self.notify_match(a, guess)
        except EndGameException as e:
            return self.game.end(e.args[0])


class AutoPlayer(Player):
    def __init__(self, game):
        super(AutoPlayer, self).__init__(game)
        self.cards = {(x, y) for x in range(game.x) for y in range(game.y)}
        self.memory = {}
        self.matches = set()

    def choose_cards(self):
        if self.matches:
            return self.matches.pop()
        else:
            return self.cards.pop(), self.cards.pop()

    def notify_nonmatch(self, value, card):
        print 'saw {} at {}'.format(value, card)
        if value in self.memory:
            self.matches.add((self.memory.pop(value), card))
        else:
            self.memory[value] = card
        self.check_end_game()

    def notify_match(self, value, cards):
        print 'matched {} at {} and {}'.format(value, *cards)
        self.check_end_game()

    def check_end_game(self):
        """Return raise EndGameException iff in an end state."""
        if not self.memory and (
            (len(self.cards) == 2 and len(self.matches) == 0)
            or (len(self.matches) == 1 and len(self.cards) == 0)
        ):
            raise EndGameException(self.choose_cards())



class ManualPlayer(Player):
    def __init__(self, game):
        super(ManualPlayer, self).__init__(game)
        self.cards = {(x, y) for x in range(game.x) for y in range(game.y)}

    def choose_cards(self):
        print 'Remaining coordinates: {}'.format(sorted(self.cards))
        return (
            self.ask_card('Enter the first card: '),
            self.ask_card('Enter the second card: ')
        )

    def ask_card(self, prompt):
        s = raw_input(prompt).strip()
        if s == 'end':
            print 'Enter END GAME CARDS: '
            raise EndGameException(self.choose_cards())
        try:
            values = map(int, re.split('[,\s]+', s))
        except ValueError:
            return self.ask_card('Coordinates must be integer; try again: ')
        if len(values) != 2:
            return self.ask_card('Card must have two parts; "X, Y": ')
        return tuple(values)

    def notify_nonmatch(self, value, card):
        print 'saw {} at {}'.format(value, card)

    def notify_match(self, value, cards):
        print 'matched {} at {} and {}'.format(value, *cards)
        self.cards -= set(cards)
