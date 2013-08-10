import abc
import curses
import re


class EndGameException(Exception):
    pass


class Player(object):
    """Recall game player.

    A player takes a game (as a constructor argument).  When
    ``play`` is called (no arguments) the game is played to
    completion and the result of the game is returned.

    """
    __metaclass__ = abc.ABCMeta

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
            outcome = self.game.end(e.args[0])
            self.notify_outcome(*outcome)

    @abc.abstractmethod
    def notify_match(self, value, cards):
        pass

    @abc.abstractmethod
    def notify_nonmatch(self, value, card):
        pass

    @abc.abstractmethod
    def notify_outcome(self, win, msg):
        pass


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

    def notify_outcome(self, win, msg):
        print msg


class ManualPlayer(Player):
    def __init__(self, game):
        super(ManualPlayer, self).__init__(game)
        self.cards = {(x, y) for x in range(game.x) for y in range(game.y)}
        self.matched_cards = set()

    def play(self):
        curses.wrapper(self._play)

    def _play(self, screen):
        self.screen = screen
        self.obscure_cards()
        self.screen.refresh()
        super(ManualPlayer, self).play()

    def obscure_cards(self):
        for x, y in self.cards:
            self.screen.addstr(y, x, '@')
        for x, y in self.matched_cards:
            self.screen.addstr(y, x, ' ')

    def choose_cards(self):
        return (
            self.ask_card('Enter the first card: '),
            self.ask_card('Enter the second card: ')
        )

    def ask_card(self, prompt):
        self.screen.move(self.game.y + 1, 0)
        self.screen.clrtoeol()
        self.screen.addstr(self.game.y + 1, 0, prompt)
        curses.echo()
        s = self.screen.getstr().strip()
        curses.noecho()
        if s == 'end':
            self.alert('Enter END GAME CARDS: ')
            raise EndGameException(self.choose_cards())
        try:
            values = tuple(map(int, re.split('[,\s]+', s)))
        except ValueError:
            self.alert('Coordinates must be integer; try again.')
            return self.ask_card(prompt)
        if len(values) != 2:
            self.alert('Card must have two parts; "X, Y".')
            return self.ask_card(prompt)
        if values not in self.cards:
            self.alert('Card is not on the table; try again.')
            return self.ask_card(prompt)
        # ready to rumble
        self.alert('')
        self.obscure_cards()
        return values

    def alert(self, msg):
        self.screen.move(self.game.y, 0)
        self.screen.clrtoeol()
        self.screen.addstr(self.game.y, 0, msg)

    def notify_nonmatch(self, value, card):
        self.screen.addstr(card[1], card[0], value[0])

    def notify_match(self, value, cards):
        self.alert('matched {} at {} and {}'.format(value, *cards))
        for x, y in cards:
            self.screen.addstr(y, x, ' ')
        self.cards -= set(cards)
        self.matched_cards |= set(cards)

    def notify_outcome(self, win, msg):
        self.alert(msg)
