from ff_espn_api import League
from prettytable import PrettyTable
from collections import Counter
from os import system, name
from time import sleep
import datetime
from userData import (currentWeek, year, leagues)

beginTime = datetime.datetime.now()
beginTime = beginTime.replace(microsecond = 0)
authed_leagues = []
leagues_initialized = False

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def getProjTeamPoints(team):
    projectedScore = 0
    for player in team:
        if (player.slot_position != "BE") and (player.slot_position != "IR"):
            projectedScore += player.projected_points
    return round(projectedScore, 1)

def formatForHome(homeName, homeScore, homeProj, awayName, awayScore, awayProj):
    formatted = []
    formatted.append("\033[1;32;40m " + homeName + " \033[0;37;40m")
    formatted.append("\033[1;32;40m " + str(homeScore) + " \033[0;37;40m")
    formatted.append("\033[40m " + str(homeProj) + " \033[0;37;40m")
    formatted.append("\033[40m " + str(awayProj) + " \033[0;37;40m")
    formatted.append("\033[1;31;40m " + str(awayScore) + " \033[0;37;40m")
    formatted.append("\033[1;31;40m " + awayName + " \033[0;37;40m")
    return formatted

def formatForAway(homeName, homeScore, homeProj, awayName, awayScore, awayProj):
    formatted = []
    formatted.append("\033[1;31;40m " + homeName + " \033[0;37;40m")
    formatted.append("\033[1;31;40m " + str(homeScore) + " \033[0;37;40m")
    formatted.append("\033[40m " + str(homeProj) + " \033[0;37;40m")
    formatted.append("\033[40m " + str(awayProj) + " \033[0;37;40m")
    formatted.append("\033[1;32;40m " + str(awayScore) + " \033[0;37;40m")
    formatted.append("\033[1;32;40m " + awayName + " \033[0;37;40m")
    return formatted

def getScores():
    timesLooped = 0
    print("Note: Use Ctrl-C to Stop")
    while True:
        startTime = datetime.datetime.now()
        startTime = startTime.replace(microsecond = 0)
        print("\033[0;37;40mStarted at:", startTime)
        boxScore = PrettyTable()
        boxScore.field_names = [
        "\033[0;30;47m League \033[0;37;40m",
        "\033[0;30;47m Home Team \033[0;37;40m",
        "\033[0;30;47m H \033[0;37;40m",
        "\033[0;30;47m Orig. Proj. \033[0;37;40m",
        "\033[0;30;47m vs \033[0;37;40m",
        "\033[0;30;47m Orig. Proj \033[0;37;40m",
        "\033[0;30;47m A \033[0;37;40m",
        "\033[0;30;47m Away Team \033[0;37;40m"]
        for x in range(len(leagues)):
            leagueName = leagues[x]["leagueName"]
            teamName = leagues[x]["teamName"]
            box_score = authed_leagues[x].box_scores(currentWeek)
            for i in range(len(box_score)):
                scoreRow = []
                home_team = box_score[i].home_team
                away_team = box_score[i].away_team
                home_name = home_team.team_name
                away_name = away_team.team_name
                home_score = box_score[i].home_score
                away_score = box_score[i].away_score
                proj_away_score = getProjTeamPoints(box_score[i].away_lineup)
                proj_home_score = getProjTeamPoints(box_score[i].home_lineup)
                if teamName == home_name:
                    scoreRow = formatForHome(home_name, home_score, proj_home_score, away_name, away_score, proj_away_score)
                    boxScore.add_row([leagueName, scoreRow[0], scoreRow[1], scoreRow[2], "vs", scoreRow[3], scoreRow[4], scoreRow[5]])
                elif teamName == away_name:
                    scoreRow = formatForAway(home_name, home_score, proj_home_score, away_name, away_score, proj_away_score)
                    boxScore.add_row([leagueName, scoreRow[0], scoreRow[1], scoreRow[2], "vs", scoreRow[3], scoreRow[4], scoreRow[5]])
        finishTime = datetime.datetime.now()
        finishTime = finishTime.replace(microsecond = 0)
        runtime = finishTime - startTime
        timesLooped += 1
        print(boxScore)
        print("[", timesLooped, "] ", "Updated:", finishTime, "( runtime:", runtime, ")\n")

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

def roundUpMenu():
    i = 0
    menu = {}
    for i in range(len(leagues)):
        menu[str(i+1) + '.'] = leagues[i]["leagueName"]
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        selection = int(input("Select a league: "))
        if selection > 0 and selection <= len(leagues):
           roundUp((selection - 1), currentWeek)
           break
        else:
            print("Invalid selection! Try again.")

def roundUp(league_index, week):
    roundUpString = "*~* *Week " + str(week) + " Round Up* *~*\n\n"
    roundUpString += getScoreSummary(league_index) + '\n' + getMinMaxScores(league_index) + getVictoryMargins(league_index) + getBenchScore(league_index) + '\n' + getTopScore(league_index) + '\n'
    print(roundUpString)

def initializeLeagues():
    global leagues_initialized
    if not leagues_initialized:
        for league in leagues:
            authed_leagues.append(League(league["leagueID"], year, league["espn_s2"], league["swid"]))
            leagues_initialized = True

def displayMenu():
    menu = {}
    menu['1.'] = "Start Scoreboard"
    menu['2.'] = "Round Up Report"
    menu['3.'] = "Exit"
    while True:
        options = menu.keys()
        #options.sort()
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please Select: ")
        if selection =='1':
            clear()
            try:
                getScores()
            except KeyboardInterrupt:
                clear()
                print("Please choose another option:\n")
                pass
        elif selection == '2':
            clear()
            roundUpMenu()
            input("Press 'Enter' to continue...")
        elif selection == '3':
            break
        else:
            print("Unknown option selected!")



clear()
initializeLeagues()
displayMenu()
