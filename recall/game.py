import random

import requests


class OnlineGame(object):
    def __init__(self, url, name, email):
        """Initialise game with base URL."""
        self.url = url
        r = requests.post(
            '{}/games/'.format(url),
            data={'name': name, 'email': email}
        )
        data = r.json()
        self.id, self.x, self.y = data['id'], data['width'], data['height']

    def guess(self, cards):
        if cards[0] == cards[1]:
            raise ValueError('cannot guess same card')
        a = requests.get(
            '{}/games/{}/cards/{},{}'
            .format(self.url, self.id, cards[0][0], cards[0][1])
        )
        b = requests.get(
            '{}/games/{}/cards/{},{}'
            .format(self.url, self.id, cards[1][0], cards[1][1])
        )
        return a.text, b.text

    def end(self, cards):
        r = requests.post(
            '{}/games/{}/end'.format(self.url, self.id),
            data={
                'x1': cards[0][0], 'y1': cards[0][1],
                'x2': cards[1][0], 'y2': cards[1][1],
            }
        )
        data = r.json()
        return data['success'], data['message']


def value_generator():
    value = ord('a')
    while True:
        yield chr(value)
        yield chr(value)
        value += 1


class OfflineGame(object):
    def __init__(self):
        self.x = 4
        self.y = 4
        cards = [(x, y) for x in range(self.x) for y in range(self.y)]
        random.shuffle(cards)
        values = value_generator()
        self.cards = set(cards)
        self.values_by_card = {card: next(values) for card in cards}

    def guess(self, cards):
        a, b = map(self.values_by_card.get, cards)
        if a == b:
            self.cards -= set(cards)
        return a, b

    def end(self, cards):
        remaining = len(self.cards)
        if remaining == 2 and self.cards == set(cards):
            return True, "for the win"
        else:
            return False, "epic fail; {} cards remaining".format(remaining)
