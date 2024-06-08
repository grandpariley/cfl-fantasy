import itertools
from abc import ABC, abstractmethod
from math import inf

INITIAL_BUDGET = 70000


def pick_position(budget, players):
    player = None
    for i in range(len(players)):
        if int(players[i]['price']) <= budget:
            player = players[i]
    if player is None:
        return None, budget
    return player, budget - int(player['price'])


def get_players_by_position(key, data):
    if 'qb' == key:
        return list(filter(lambda d: d['position'] == 'quarterback', data))
    elif 'rb' in key:
        return list(filter(lambda d: d['position'] == 'running_back', data))
    elif 'wr' in key:
        return list(filter(lambda d: d['position'] == 'wide_receiver', data))
    return list(filter(lambda d: d['position'] in ('wide_receiver', 'running_back'), data))


def get_pick_score(picks):
    return sum([d['score'] if d else 0 for d in picks.values()])


def filter_duplicates(positions):
    pos = []
    for p in positions:
        if any(pi in pos for pi in positional_inverses(p)):
            continue
        pos.append(p)
    return pos


def positional_inverses(p):
    p_copy = [list(p), list(p), list(p), list(p), list(p), list(p), list(p)]
    p_copy[1][p.index('wr1')], p_copy[1][p.index('wr2')] = p_copy[1][p.index('wr2')], p_copy[1][p.index('wr1')]
    p_copy[2][p.index('rb1')], p_copy[2][p.index('rb2')] = p_copy[2][p.index('rb2')], p_copy[2][p.index('rb1')]
    p_copy[3][p.index('rb1')], p_copy[3][p.index('flex')] = p_copy[3][p.index('flex')], p_copy[3][p.index('rb1')]
    p_copy[4][p.index('rb2')], p_copy[4][p.index('flex')] = p_copy[4][p.index('flex')], p_copy[4][p.index('rb2')]
    p_copy[5][p.index('wr1')], p_copy[5][p.index('flex')] = p_copy[5][p.index('flex')], p_copy[5][p.index('wr1')]
    p_copy[6][p.index('wr2')], p_copy[6][p.index('flex')] = p_copy[6][p.index('flex')], p_copy[6][p.index('wr2')]
    return map(lambda c: tuple(c), p_copy)


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
        self.current_pick_score = -inf

    def pick(self):
        positions = filter_duplicates(list(itertools.permutations(blank_picks().keys())))
        for p in positions:
            self.pick_by_position_order(p)

    def pick_by_position_order(self, positions):
        picks = self.get_picks(positions)
        pick_score = get_pick_score(picks)
        if self.current_pick_score < pick_score:
            self.picks = picks
            self.current_pick_score = pick_score

    def get_picks(self, positions):
        budget = INITIAL_BUDGET
        data = sorted(list(map(self.assign_score, self.data)), key=lambda d: d['score'])
        picks = blank_picks()
        for p in positions:
            picks[p], budget = pick_position(budget, get_players_by_position(p, data))
            data = sorted(list(map(lambda d: self.re_assign_score(d, self.picks, self.picks[p], budget),
                                   filter(lambda d: str(d) != str(picks[p]), data))), key=lambda d: d['score'])
        return picks

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
