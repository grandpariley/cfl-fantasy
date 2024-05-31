import random
from abc import ABC, abstractmethod

INITIAL_BUDGET = 40000


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


def get_pick_score(picks):
    return sum([d['score'] if d else 0 for d in picks.values()])


def blank_picks():
    return {
        'qb': None,
        'rb1': None,
        'rb2': None,
        'wr1': None,
        'wr2': None,
        'flex': None,
    }


class Model(ABC):
    def __init__(self, fetcher):
        self.data = fetcher.get_data()
        self.picks = blank_picks()
        self.current_pick_score = 0

    def pick(self):
        for _ in range(3):
            positions = list(self.picks.keys())
            random.shuffle(positions)
            self.pick_by_position_order(positions)

    def pick_by_position_order(self, positions):
        budget = INITIAL_BUDGET
        data = sorted(list(map(self.assign_score, self.data)), key=lambda d: d['score'])
        picks = blank_picks()
        for p in positions:
            self._pick(budget, data, p, picks)
        pick_score = get_pick_score(picks)
        if self.current_pick_score < pick_score:
            self.picks = picks
            self.current_pick_score = pick_score

    def _pick(self, budget, data, p, picks):
        qbs = list(filter(lambda d: d['position'] == 'quarterback', data))
        rbs = list(filter(lambda d: d['position'] == 'running_back', data))
        wrs = list(filter(lambda d: d['position'] == 'wide_receiver', data))
        flex = list(filter(lambda d: d['position'] in ('wide_receiver', 'running_back'), data))
        picks[p], budget = pick_position(budget, get_players_by_position(p, qbs, rbs, wrs, flex))
        data = self._refresh_data(data, p, budget, picks)

    def _refresh_data(self, data, p, budget, picks):
        return sorted(list(map(lambda d: self.re_assign_score(d, self.picks, self.picks[p], budget),
                               filter(lambda d: str(d) != str(picks[p]), data))), key=lambda d: d['score'])

    def present(self):
        p = ''
        for k in self.picks.keys():
            p += k + ': '
            if self.picks[k] is not None:
                p += self.picks[k]['firstName'] + ' ' + self.picks[k]['lastName']
            p += '\n'
        print(p)

    def assign_score(self, d):
        d['score'] = self.score(d)
        return d

    def re_assign_score(self, d, picks, last_picked, budget):
        d['score'] = self.re_score(d, picks, last_picked, budget)
        return d

    @abstractmethod
    def score(self, d):
        pass

    def re_score(self, d, picks, last_picked, budget):
        return self.score(d)
