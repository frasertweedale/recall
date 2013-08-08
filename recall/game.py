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
