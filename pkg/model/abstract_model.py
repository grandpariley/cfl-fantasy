import random
from abc import ABC, abstractmethod

INITIAL_BUDGET = 40000


def firstfive(l):
    return list(map(lambda t: t['lastName'] + ' : ' + t['projected_points'] + ' : ' + t['price'], l))[-5:]


def pick_position(budget, players):
    player = None

    for i in range(len(players)):
        if int(players[i]['price']) <= budget:
            player = players[i]
    if player is None:
        return None, budget
    return player, budget - int(player['price'])


def get_players_by_position(key, qbs, rbs, wrs, flex):
    if 'qb' == key:
        return qbs
    elif 'rb' in key:
        return rbs
    elif 'wr' in key:
        return wrs
    return flex


class Model(ABC):
    def __init__(self, fetcher):
        self.data = fetcher.get_data()
        self.picks = {
            'qb': None,
            'rb1': None,
            'rb2': None,
            'wr1': None,
            'wr2': None,
            'flex': None,
        }

    def pick(self):
        budget = INITIAL_BUDGET
        data = self.sort(self.data)
        keys = list(self.picks.keys())
        random.shuffle(keys)
        for k in keys:
            qbs = list(filter(lambda d: d['position'] == 'quarterback', data))
            rbs = list(filter(lambda d: d['position'] == 'running_back', data))
            wrs = list(filter(lambda d: d['position'] == 'wide_receiver', data))
            flex = list(filter(lambda d: d['position'] in ('wide_receiver', 'running_back'), data))
            self.picks[k], budget = pick_position(budget, get_players_by_position(k, qbs, rbs, wrs, flex))
            data = list(filter(lambda d: str(d) != str(self.picks[k]), data))
            data = self.re_sort(data, self.picks, self.picks[k], budget)

    def present(self):
        p = ''
        for k in self.picks.keys():
            p += k + ': '
            if self.picks[k] is not None:
                p += self.picks[k]['firstName'] + ' ' + self.picks[k]['lastName']
            p += '\n'
        print(p)

    @abstractmethod
    def sort(self, data):
        pass

    @abstractmethod
    def re_sort(self, data, picks, last_picked, budget):
        pass


class SimpleModel(Model, ABC):
    def sort(self, data):
        return sorted(data, key=self.key)

    def re_sort(self, data, picks, last_picked, budget):
        return data

    @abstractmethod
    def key(self, d):
        pass
