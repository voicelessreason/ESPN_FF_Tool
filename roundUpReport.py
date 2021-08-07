from ff_espn_api import League
from userData import (currentWeek, leagues)
authed_leagues = []


def getBenchScore(league_index):
    benchScore = 0
    benchScores = []
    teams = []
    lineups = []
    benchPlayers = []
    i = 0
    box_score = authed_leagues[league_index].box_scores(currentWeek)
    for i in range(len(box_score)):
        teams.append(box_score[i].away_team.team_name)
        teams.append(box_score[i].home_team.team_name)
        lineups.append(box_score[i].away_lineup)
        lineups.append(box_score[i].home_lineup)
    for j in range(len(lineups)):
        benchScore = 0
        for player in lineups[j]:
            player_pos = player.slot_position
            benchPlayers = []
            if player_pos == 'BE' or player_pos == "IR":
                benchPlayers.append(player.points)
            for benchPlayer in benchPlayers:
                benchScore += benchPlayer
        benchScores.append(round(benchScore))
    benchPoints = max(benchScores)
    returnTeam = teams[benchScores.index(benchPoints)]
    return "*'Put Me In Coach' Award*: " + returnTeam + ' - ' + str(round(benchPoints, 1)) + " points left on the bench"

def getTopScore(league_index):
    score = 0
    scores = []
    scorers = []
    topScores = []
    topScorers = []
    i = 0
    for i in range(currentWeek):
        box_scores = authed_leagues[league_index].box_scores(i)
        for game in box_scores:
            scorers.append(game.home_team.team_name)
            scores.append(game.home_score)
            scorers.append(game.away_team.team_name)
            scores.append(game.away_score)
        topScores.append(max(scores))
        topScorers.append(scorers[scores.index(max(scores))])
    topScore = max(topScores)
    topScorer = topScorers[topScores.index(topScore)]
    return "*Highest Single Week Score*: " + topScorer + " - " + str(round(topScore, 1))

def getMinMaxScores(league_index):
    scores = []
    box_scores = authed_leagues[league_index].box_scores(currentWeek)
    for game in box_scores:
        scores.append(game.home_score + game.away_score)
    snoozeFest = round(min(scores), 1)
    barnBurner = round(max(scores), 1)
    snooze = "*Snoozefest of the Week*: " + str(snoozeFest) + " points scored"
    burner = "*Barnburner of the Week*: " + str(barnBurner) + " points scored"
    return burner + '\n' + snooze + '\n'

def getVictoryMargins(league_index):
    margins = []
    matchups = []
    box_scores = authed_leagues[league_index].box_scores(currentWeek)
    for game in box_scores:
        margins.append(abs(game.home_score - game.away_score))
        matchups.append(game.home_team.team_name + ' vs ' + game.away_team.team_name)
    maxMargin = max(margins)
    minMargin = min(margins)
    maxMatchup = matchups[margins.index(maxMargin)]
    minMatchup = matchups[margins.index(minMargin)]
    blowout = "*Blowout of the Week*: " + maxMatchup + " - " + str(round(maxMargin, 1)) + " point differential"
    nailbiter = "*Nailbiter of the Week*: " + minMatchup + " - " + str(round(minMargin, 1)) + " point differential"
    return blowout + '\n' + nailbiter + '\n'

def getScoreSummary(league_index):
    box_scores = authed_leagues[league_index].box_scores(currentWeek)
    returnString = ""
    for game in box_scores:
        winScore = max([game.away_score, game.home_score])

        if winScore == game.away_score:
            winnerRecord = "(" + str(game.away_team.wins) + "-" + str(game.away_team.losses) + ")"
            loserRecord = "(" + str(game.home_team.wins) + "-" + str(game.home_team.losses) + ")"
            returnString += "*" + game.away_team.team_name + "* " + winnerRecord + " defeats " + "*" + game.home_team.team_name + "* "  + loserRecord + ": " + str(round(game.away_score, 1)) + " - " + str(round(game.home_score, 1)) + '\n'
        else:
            winnerRecord = "(" + str(game.home_team.wins) + "-" + str(game.home_team.losses) + ")"
            loserRecord = "(" + str(game.away_team.wins) + "-" + str(game.away_team.losses) + ")"
            returnString += "*" + game.home_team.team_name + "* " + winnerRecord + " defeats " + "*" + game.away_team.team_name + "* "  + loserRecord + ": " + str(round(game.home_score, 1)) + " - " + str(round(game.away_score, 1)) + '\n'
    return returnString



def roundUp(league_index, week, authed, normal):
    global authed_leagues
    global leagues
    authed_leagues = authed
    leagues = normal

    roundUpString = "*~* *Week " + str(week) + " Round Up* *~*\n\n"
    roundUpString += getScoreSummary(league_index) + '\n' + getMinMaxScores(league_index) + getVictoryMargins(league_index) + getBenchScore(league_index) + '\n' + getTopScore(league_index) + '\n'
    print(roundUpString)
