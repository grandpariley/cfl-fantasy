from types import NoneType
from datetime import date
from os.path import exists
import requests
import csv

columns = [
    'lastName',
    'firstName',
    'team',
    'position',
    'price',
    'projected_points',
    'average_points',
    'pass_tds',
    'interceptions',
    'pass_yds',
    'average_pass_yards',
    'targets',
    'receptions',
    'receiving_yds',
    'average_receiving_yds',
    'receiving_tds',
    'rushes',
    'rush_tds',
    'average_rush_yds'
]

players_url = 'https://gamezone.cfl.ca/json/fantasy/players.json'


def stats_file_name():
    return 'stats-' + str(date.today()) + '.csv'


def parse_row(row):
    return {
        'lastName': row[0],
        'firstName': row[1],
        'team': row[2],
        'position': row[3],
        'price': row[4],
        'projected_points': row[5],
        'average_points': row[6],
        'pass_tds': row[7],
        'interceptions': row[8],
        'pass_yds': row[9],
        'average_pass_yards': row[10],
        'targets': row[11],
        'receptions': row[12],
        'receiving_yds': row[13],
        'average_receiving_yds': row[14],
        'receiving_tds': row[15],
        'rushes': row[16],
        'rush_tds': row[17],
        'average_rush_yds': row[18],
    }


def get_row(datum):
    stats = datum.get('stats').get('stats')
    return [
        datum.get('lastName'),
        datum.get('firstName'),
        datum.get('squad').get('abbr'),
        datum.get('position'),
        datum.get('cost'),
        datum.get('stats').get('projectedScores', 0),
        datum.get('stats').get('avgPoints', 0),
        stats.get('pass_tds', 0),
        stats.get('pass_int', 0),
        stats.get('pass_yds', 0),
        stats.get('avg_pass_yds', 0),
        stats.get('tar', 0),
        stats.get('rec', 0),
        stats.get('rec_yds', 0),
        stats.get('avg_rec_yds', 0),
        stats.get('rec_tds', 0),
        stats.get('rush', 0),
        stats.get('rush_tds', 0),
        stats.get('avg_rush_yds', 0),
    ]


def load():
    if exists(stats_file_name()):
        return
    with open(stats_file_name(), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        r = requests.get(players_url)
        if r.status_code != 200:
            raise Exception(r)
        data = r.json()
        for datum in data:
            if type(datum.get('stats').get('stats')) in [list, NoneType]:
                continue
            writer.writerow(get_row(datum))


class Fetcher:
    def __init__(self):
        self.data = []
        load()

    def get_data(self):
        if self.data:
            return self.data
        self.data = []
        with open(stats_file_name(), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.data.append(parse_row(row))
            return self.data
