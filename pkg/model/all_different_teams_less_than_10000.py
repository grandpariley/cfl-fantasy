from pkg.model.abstract_model import Model

picked_teams = []


def score_and_sort(data):
    new_data = []
    for d in data:
        if d['team'] in picked_teams or int(d['price']) > 10000:
            d['score'] = 0
        else:
            d['score'] = float(d['projected_points'])
        new_data.append(d)
    return sorted(new_data, key=lambda d: d['score'])


class AllDifferentTeamsAndLessThan10000(Model):
    def sort(self, data):
        return score_and_sort(data)

    def re_sort(self, data, picks, last_picked, budget):
        if last_picked:
            picked_teams.append(last_picked['team'])
        return score_and_sort(data)

    def sort_pick_positions(self, positions):
        return sorted(positions)