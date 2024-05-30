import random
from abc import ABC, abstractmethod

INITIAL_BUDGET = 40000


def pick_position(budget, players):
    while len(players) > 0 and int(players[0]['price']) > budget:
        players.pop()
    if len(players) == 0:
        return '', budget
    player = players.pop()
    return player['firstName'] + ' ' + player['lastName'], budget - int(player['price'])


def get_players_by_position(key, qbs, rbs, wrs):
    if 'qb' == key:
        return qbs
    elif 'rb' in key:
        return rbs
    elif 'wr' in key:
        return wrs
    return []


class Model(ABC):
    def __init__(self, fetcher):
        self.data = fetcher.get_data()
        self.picks = {
            'qb': '',
            'rb1': '',
            'rb2': '',
            'wr1': '',
            'wr2': '',
            'flex': '',
        }

    def pick(self):
        data = self.sort(self.data)
        qbs = list(filter(lambda d: d['position'] in ['quarterback'], data))
        rbs = list(filter(lambda d: d['position'] in ['running_back'], data))
        wrs = list(filter(lambda d: d['position'] in ['wide_receiver'], data))
        budget = INITIAL_BUDGET
        keys = list(filter(lambda k: k != 'flex', self.picks.keys()))
        random.shuffle(keys)
        for k in keys:
            self.picks[k], budget = pick_position(budget, get_players_by_position(k, qbs, rbs, wrs))
        flex = wrs + rbs
        self.picks['flex'], budget = pick_position(budget, flex)

    def present(self):
        print('\n'.join([k + ': ' + self.picks[k] for k in self.picks]))

    @abstractmethod
    def sort(self, data):
        pass


class SimpleModel(Model, ABC):
    def sort(self, data):
        return sorted(data, key=self.key)

    @abstractmethod
    def key(self, d):
        pass
