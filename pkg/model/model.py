from abc import ABC, abstractmethod

INITIAL_BUDGET = 40000


def pick_position(budget, players):
    while int(players[0]['price']) > budget:
        players.pop()
    player = players.pop()
    return player['firstName'] + ' ' + player['lastName'], budget - int(player['price'])


class Model(ABC):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.picks = {
            'qb': '',
            'rb1': '',
            'rb2': '',
            'wr1': '',
            'wr2': '',
            'flex': '',
            'd': '' # not yet implemented
        }

    @abstractmethod
    def sort(self):
        pass

    def pick(self):
        self.sort()
        qbs = list(filter(lambda d: d['position'] in ['quarterback'], self.data))
        rbs = list(filter(lambda d: d['position'] in ['running_back'], self.data))
        wrs = list(filter(lambda d: d['position'] in ['wide_receiver'], self.data))
        budget = INITIAL_BUDGET
        self.picks['qb'], budget = pick_position(budget, qbs)
        self.picks['rb1'], budget = pick_position(budget, rbs)
        self.picks['rb2'], budget = pick_position(budget, rbs)
        self.picks['wr1'], budget = pick_position(budget, wrs)
        self.picks['wr2'], budget = pick_position(budget, wrs)
        flex = wrs + rbs
        self.picks['flex'], budget = pick_position(budget, flex)

    def present(self):
        print(self.name + ' suggests you pick:\n' + '\n'.join([k + ': ' + self.picks[k] for k in self.picks]))
