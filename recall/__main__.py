import argparse

from . import game
from . import player


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true',
        help='automatically play the game')
    parser.add_argument('--local', action='store_true',
        help='play a local game (default: remote)')
    parser.add_argument('--url',
        help='base URL of the game server')
    parser.add_argument('--name', default='Fraser Tweedale')
    parser.add_argument('--email', default='frase@frase.id.au')

    args = parser.parse_args()

    if args.local:
        game_obj = game.OfflineGame()
    else:
        if not args.url:
            raise UserWarning('URL must be provided')
        game_obj = game.OnlineGame(url=args.url, name=args.name, email=args.email)

    if args.auto:
        player_obj = player.AutoPlayer(game_obj)
    else:
        player_obj = player.ManualPlayer(game_obj)

    result = player_obj.play()
    print result


main()
