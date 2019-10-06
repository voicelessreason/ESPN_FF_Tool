from ff_espn_api import League
from prettytable import PrettyTable
from collections import Counter
from os import system, name
from time import sleep
import datetime
import signal
import yaml

beginTime = datetime.datetime.now()
beginTime = beginTime.replace(microsecond = 0)
timesLooped = 0
myPlayers = []
oppPlayers = []
allPlayers = []
fullPlayers= []

def keyboardInterruptHandler(signal, frame):
    print("  KeyboardInterrupt (ID: {}) has been caught. Stopping...".format(signal))
    exit(0)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def readConfig(config):
    with open(config) as f:
        configData = yaml.load(f, Loader=yaml.FullLoader)
        return configData

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
    global timesLooped
    global finishTime
    configData = readConfig('config.yml')

    if timesLooped == 0:
        startTime = beginTime
    else:
        startTime = finishTime
    startTime = startTime.replace(microsecond = 0)
    print("Started at: ", startTime)
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

    for name in configData['league_names']:
        year = configData['year']
        week = configData['currentWeek']
        teamName = name
        id = configData[name]['id']
        swid = configData[name]['swid']
        espn_s2 = configData[name]['espn_s2']
        league = League(id, year, swid, espn_s2)
        box_score = league.box_scores(week)
        i = 0
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
                boxScore.add_row([teamName, scoreRow[0], scoreRow[1], scoreRow[2], "vs", scoreRow[3], scoreRow[4], scoreRow[5]])
            elif teamName == away_name:
                scoreRow = formatForAway(home_name, home_score, proj_home_score, away_name, away_score, proj_away_score)
                boxScore.add_row([teamName, scoreRow[0], scoreRow[1], scoreRow[2], "vs", scoreRow[3], scoreRow[4], scoreRow[5]])
    finishTime = datetime.datetime.now()
    finishTime = finishTime.replace(microsecond = 0)
    runtime = finishTime - startTime
    #runtime = runtime.replace(microsecond = 0)
    timesLooped = timesLooped + 1
    print(boxScore)
    print("[", timesLooped, "] ", "Updated: ", finishTime, " (runtime: ", runtime, ")\n")
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

def findTraitors():
    global timesLooped
    global finishTime
    global myPlayers
    global oppPlayers
    global allPlayers
    configData = readConfig('config.yml')
    print("Started at: ", beginTime)
    if timesLooped == 0:
        startTime = beginTime
    else:
        startTime = finishTime
    boxScore = PrettyTable()
    boxScore.field_names = [
        "\033[0;30;47m Player \033[0;37;40m",
        "\033[0;30;47m Position \033[0;37;40m",
        "\033[0;30;47m For \033[0;37;40m",
        "\033[0;30;47m Against \033[0;37;40m"]
    for name in configData['league_names']:
        year = configData['year']
        week = configData['currentWeek']
        teamName = name
        id = configData[name]['id']
        swid = configData[name]['swid']
        espn_s2 = configData[name]['espn_s2']
        league = League(id, year, swid, espn_s2)
        box_score = league.box_scores(week)
        i = 0
        for i in range(len(box_score)):
            home_team = box_score[i].home_team
            away_team = box_score[i].away_team
            home_name = home_team.team_name
            away_name = away_team.team_name
            if home_name == teamName:
                home_score = box_score[i].home_score
                away_score = box_score[i].away_score
                home_lineup = box_score[i].home_lineup
                away_lineup = box_score[i].away_lineup
                for player in range(len(home_lineup)):
                    player_name = home_lineup[player].name
                    player_pos = home_lineup[player].slot_position
                    myPlayers.append((player_name, player_pos))
                    allPlayers.append((player_name, player_pos))
                for player in range(len(away_lineup)):
                    player_name = away_lineup[player].name
                    player_pos = away_lineup[player].slot_position
                    oppPlayers.append((player_name, player_pos))
                    allPlayers.append((player_name, player_pos))
            if away_name == teamName:
                home_score = box_score[i].home_score
                away_score = box_score[i].away_score
                home_lineup = box_score[i].home_lineup
                away_lineup = box_score[i].away_lineup
                for player in range(len(home_lineup)):
                    player_name = home_lineup[player].name
                    player_pos = home_lineup[player].slot_position
                    oppPlayers.append((player_name, player_pos))
                    allPlayers.append((player_name, player_pos))
                for player in range(len(away_lineup)):
                    player_name = away_lineup[player].name
                    player_pos = away_lineup[player].slot_position
                    myPlayers.append((player_name, player_pos))
                    allPlayers.append((player_name, player_pos))
    for z in range(len(allPlayers)):
        name = allPlayers[z]
        if (name[1] != "BE") and (name[1] != "IR"):
            forCount = Counter(myPlayers)[name]
            againstCount = Counter(oppPlayers)[name]
            fullPlayers.append((name, forCount, againstCount))
    finishTime = datetime.datetime.now()
    runtime = finishTime - startTime
    playerList = list(dict.fromkeys(fullPlayers))
    for i in range(len(playerList)):
        if (playerList[i][1] > 0) and ((playerList[i][2] > 0)):
            displayName = playerList[i][0][0]
            displayPos = playerList[i][0][1]
            plays = playerList[i][1] + playerList[i][2]
            boxScore.add_row([displayName, displayPos, playerList[i][1], playerList[i][2]])
    boxScore.sortby = "\033[0;30;47m Position \033[0;37;40m"
    print(boxScore)
    print("Processed at: ", finishTime, "\nRuntime: ", runtime, "")

def benchScore():
    global game
    global apiTeam
    global teams
    global benchPlayers
    global benchScore
    global benchScores
    global lineups
    benchScore = 0
    benchScores = []
    teams = []
    lineups = []
    benchPlayers = []

    configData = readConfig('config.yml')
    name = configData['league_names'][0]
    year = configData['year']
    week = configData['currentWeek']
    teamName = name
    id = configData[name]['id']
    swid = configData[name]['swid']
    espn_s2 = configData[name]['espn_s2']
    league = League(id, year, swid, espn_s2)
    box_score = league.box_scores(week)

    i = 0
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
    benchWarmer = max(benchScores)
    returnTeam = teams[benchScores.index(benchWarmer)]
    print(returnTeam + ': ' + str(benchWarmer))

def topScore():
    global game
    global apiTeam
    global teams
    global players
    global score
    global scores
    global lineups
    score = 0
    scores = []
    teams = []
    lineups = []
    players = []

    configData = readConfig('config.yml')
    name = configData['league_names'][0]
    year = configData['year']
    week = configData['currentWeek']
    teamName = name
    id = configData[name]['id']
    swid = configData[name]['swid']
    espn_s2 = configData[name]['espn_s2']
    league = League(id, year, swid, espn_s2)
    box_score = league.box_scores(week)

    i = 0
    for i in range(len(box_score)):
        teams.append(box_score[i].away_team.team_name)
        teams.append(box_score[i].home_team.team_name)
        lineups.append(box_score[i].away_lineup)
        lineups.append(box_score[i].home_lineup)
    for j in range(len(lineups)):
        score = 0
        for player in lineups[j]:
            player_pos = player.slot_position
            players = []
            if player_pos != 'BE' and player_pos != "IR":
                players.append(player.points)
            for p in players:
                score += p
        scores.append(round(score))
    topScore = max(scores)
    returnTeam = teams[scores.index(topScore)]
    print(returnTeam + ': ' + str(topScore))

def minMaxScores():
    scores = []
    configData = readConfig('config.yml')
    name = configData['league_names'][0]
    year = configData['year']
    week = configData['currentWeek']
    teamName = name
    id = configData[name]['id']
    swid = configData[name]['swid']
    espn_s2 = configData[name]['espn_s2']
    league = League(id, year, swid, espn_s2)
    box_scores = league.box_scores(week)
    for game in box_scores:
        scores.append(game.home_score + game.away_score)
    snoozeFest = min(scores)
    barnBurner = max(scores)
    print("Snoozefest of the Week: " + str(snoozeFest))
    print("Barnburner of the Week: " + str(barnBurner))


def displayMenu():
    menu = {}
    menu['1.'] = "Start Scoreboard"
    menu['2.'] = "View Traitors"
    menu['3.'] = "MinMax"
    menu['4.'] = "Top Score"
    menu['5.'] = "Exit"
    while True:
        options = menu.keys()
        #options.sort()
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please Select: ")
        if selection =='1':
            clear()
            while True:
                getScores()
        elif selection == '2':
            findTraitors()
        elif selection == '3':
            minMaxScores()
        elif selection == '4':
            topScore()
        elif selection == '5':
            break
        else:
            print("Unknown Option Selected!")

clear()
displayMenu()
