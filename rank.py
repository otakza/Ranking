#!/usr/bin/python
import re
import sys
import fileinput

def rank_games(games):
    """ generator to parse games and yield ranking of each team """
    points = {}     # points associated with each team
    def game_points(scoreA, scoreB):
        """ compare scores, and allocate points: win=3, draw=1, lose=0 """
        return {1:3, 0:1, -1:0}[cmp(scoreA, scoreB)]

    # parse games and update points
    game_regex = re.compile(r'\s*(?P<teamA>\D+)\s+(?P<scoreA>\d+)\s*\,\s*(?P<teamB>\D+)\s+(?P<scoreB>\d+)', re.MULTILINE)
    for game in game_regex.finditer(games):
        game = game.groupdict()
        points[game['teamA']] = points.get(game['teamA'], 0) + game_points(game['scoreA'], game['scoreB'])
        points[game['teamB']] = points.get(game['teamB'], 0) + game_points(game['scoreB'], game['scoreA'])

    # display team ranking
    ranking = 1     # current ranking
    rankpts = None  # points associated with last rank
    rankmax = 0     # maximum ranking to be used in the event of a tie
    for team in sorted(sorted(points.keys(), key=lambda team: team.lower()), key=lambda team: points[team], reverse=True):
        # teams are sorted alphabetically, then based on maximum points
        rankmax += 1
        if points[team] != rankpts:
            ranking = rankmax
            rankpts = points[team]
        yield {'ranking':ranking, 'team':team, 'points':points[team], 'label':(points[team] == 1 and 'pt' or 'pts')}

def test_games():
    """ run a series of unit tests against standard input """
    testcase = """
        Lions 3, Snakes 3
        Tarantulas 1, FC Awesome 0
        Lions 1, FC Awesome 1
        Tarantulas 3, Snakes 1
        Lions 4, Grouches 0 """
    for rank in rank_games(testcase):
        if rank['points'] == 1:
            assert rank['label'] == 'pt', 'Label should indicate 1 pt'
        if rank['points'] != 1:
            assert rank['label'] == 'pts', 'Label should indicate pts'
        if rank['team'] == 'Tarantulas':
            assert rank['ranking'] == 1, 'Tarantulas have won all their matches'
        if rank['team'] in ('FC Awesome', 'Snakes'):
            assert rank['ranking'] == 3, 'FC Awesome & Snakes are tied at 1 point each'
        if rank['team'] == 'Grouches':
            assert rank['ranking'] == 5, 'Grouches have lost all their matches'
        if rank['team'] in ('FC', 'Awesome'):
            assert False, 'FC Awesome should have been parsed as a single team'
    print 'Unit tests have passed'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for ranking in rank_games('\n'.join(fileinput.input())):
            print '{ranking}. {team}, {points} {label}'.format(**ranking)
    else:
        test_games()
