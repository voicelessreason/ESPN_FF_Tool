from ff_espn_api import League
from prettytable import PrettyTable
from collections import Counter
from os import system, name
from time import sleep
import datetime
from userData import (currentWeek, year, leagues)

beginTime = datetime.datetime.now()
beginTime = beginTime.replace(microsecond = 0)

def clear():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

def greenText(input):
    return "\033[1;32;40m" + str(input) + "\033[0;37;40m"

def yellowText(input):
    return "\033[1;33;40m" + str(input) + "\033[0;37;40m"

def redText(input):
    return "\033[1;31;40m" + str(input) + "\033[0;37;40m"

def negText(input):
    return "\033[0;30;47m " + str(input) + " \033[0;37;40m"

def getProjTeamPoints(team):
    projectedScore = 0

    for player in team:
        if (player.slot_position != "BE") and (player.slot_position != "IR"):
            projectedScore += player.projected_points

    return round(projectedScore, 2)

def getLeague(league_index):
    global leagueName
    global teamName

    currentLeague = leagues[league_index]

    leagueName = currentLeague[0]
    leagueID = currentLeague[1]
    teamName = currentLeague[2]
    username = currentLeague[3]
    password = currentLeague[4]

    league = League(leagueID, year, username, password)
    getLeague.league = league
    # to use this just be sure to replace "league.%%"" with "getLeague.league.%%"" (typically used when getting box_score)

def getScores():
    timesLooped = 0

    print("Note: Use Ctrl-C to Stop")

    while True:
        startTime = datetime.datetime.now()
        startTime = startTime.replace(microsecond = 0)
        print("\033[0;37;40mStarted at:", startTime)

        boxScore = PrettyTable()
        boxScore.field_names = [
            negText("League"),
            negText("Home Team"),
            negText("H (Proj)"),
            negText("vs"),
            negText("A (Proj)"),
            negText("Away Team")]

        for x in range(len(leagues)):
            getLeague(x)
            box_score = getLeague.league.box_scores(currentWeek)

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

                if home_name == teamName:
                    home_score = box_score[i].home_score
                    away_score = box_score[i].away_score

                    home_name = greenText(home_name)

                    if home_score > away_score:
                        home_score = greenText(home_score)
                    elif home_score == away_score:
                        home_score = yellowText(home_score)
                    else:
                        home_score = redText(home_score)

                    home_score_display = str(home_score) + " (" + str(proj_home_score) + ")"
                    away_score_display = str(away_score) + " (" + str(proj_away_score) + ")"

                    boxScore.add_row([leagueName, home_name, home_score_display, "vs", away_score_display, away_name])

                if away_name == teamName:
                    home_score = box_score[i].home_score
                    away_score = box_score[i].away_score

                    away_name = greenText(away_name)

                    if away_score > home_score:
                        away_score = greenText(away_score)
                    elif home_score == away_score:
                        away_score = yellowText(away_score)
                    else:
                        away_score = redText(away_score)

                    home_score_display = str(home_score) + " (" + str(proj_home_score) + ")"
                    away_score_display = str(away_score) + " (" + str(proj_away_score) + ")"

                    boxScore.add_row([leagueName, home_name, home_score_display, "vs", away_score_display, away_name])

        finishTime = datetime.datetime.now()
        finishTime = finishTime.replace(microsecond = 0)
        runtime = finishTime - startTime
        timesLooped += 1

        print(boxScore)
        print("[", timesLooped, "] ", "Updated:", finishTime, "( runtime:", runtime, ")\n")

def findTraitors():
    myPlayers = []
    oppPlayers = []
    allPlayers = []
    fullPlayers= []

    startTime = datetime.datetime.now()
    startTime = startTime.replace(microsecond = 0)
    print("\033[0;37;40mStarted at: ", startTime)

    traitorTable = PrettyTable()
    traitorTable.field_names = [
        negText("WEEK " + str(currentWeek)),
        negText("Pos."),
        negText("For"),
        negText("Opp.")]

    for x in range(len(leagues)):
        getLeague(x)
        box_score = getLeague.league.box_scores(currentWeek)

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
        position = name[1]

        if (position != "BE") and (position != "IR"):
            forCount = Counter(myPlayers)[name]
            againstCount = Counter(oppPlayers)[name]

            fullPlayers.append((name, forCount, againstCount))

    playerList = list(dict.fromkeys(fullPlayers))

    for i in range(len(playerList)):
        if (playerList[i][1] > 0) and ((playerList[i][2] > 0)):
            displayName = playerList[i][0][0]
            displayPos = playerList[i][0][1]
            plays = playerList[i][1] + playerList[i][2]

            traitorTable.add_row([displayName, displayPos, playerList[i][1], playerList[i][2]])

    traitorTable.sortby = negText("Pos.")
    print(traitorTable)

    finishTime = datetime.datetime.now()
    finishTime = finishTime.replace(microsecond = 0)
    runtime = finishTime - startTime
    print("Updated: ", finishTime, "\nRuntime: ", runtime, "")

def getBenchScore(league_index):
    roundUpAwards = roundUp.roundUpAwards
    benchScore = 0
    benchScores = []
    matchups = []
    lineups = []
    benchPlayers = []

    getLeague(league_index)
    box_score = getLeague.league.box_scores(currentWeek)

    i = 0
    for i in range(len(box_score)):
        matchups.append(box_score[i].away_team.team_name)
        matchups.append(box_score[i].home_team.team_name)

        lineups.append(box_score[i].away_lineup)
        lineups.append(box_score[i].home_lineup)

    for j in range(len(lineups)):
        benchScore = 0

        for player in lineups[j]:
            player_pos = player.slot_position
            benchPlayers = []

            if (player_pos == "BE") or (player_pos == "IR"):
                benchPlayers.append(player.points)

            for benchPlayer in benchPlayers:
                benchScore += benchPlayer
        benchScores.append(round(benchScore))

    benchPoints = max(benchScores)
    returnTeam = matchups[benchScores.index(benchPoints)]

    if returnTeam == teamName:
        returnTeam = greenText(returnTeam)

    roundUpAwards.add_row(["'Put Me In Coach!' Award", returnTeam, str(round(benchPoints, 2)) + " bench points"])

def getTopScore(league_index):
    roundUpAwards = roundUp.roundUpAwards
    score = 0
    scores = []
    scorers = []
    topScores = []
    topScorers = []
    week = []
    weeks = []
    topWeek = []
    topWeeks = []

    getLeague(league_index)

    for i in range(currentWeek):
        box_scores = getLeague.league.box_scores(i + 1)

        for game in box_scores:
            scorers.append(game.home_team.team_name)
            scores.append(game.home_score)
            weeks.append(i + 1)

            scorers.append(game.away_team.team_name)
            scores.append(game.away_score)
            weeks.append(i + 1)

        topScores.append(max(scores))
        topScorers.append(scorers[scores.index(max(scores))])
        topWeeks.append(weeks[scores.index(max(scores))])

    topScore = max(topScores)
    topScorer = topScorers[topScores.index(topScore)]
    topWeek = topWeeks[topScores.index(topScore)]

    if topScorer == teamName:
        topScorer = greenText(topScorer)

    roundUpAwards.add_row(["Highest Score This Season", topScorer, str(round(topScore, 2)) + " points in week " + str(topWeek)])

def getMinMaxScores(league_index):
    roundUpAwards = roundUp.roundUpAwards
    scores = []
    matchups = []

    getLeague(league_index)
    box_scores = getLeague.league.box_scores(currentWeek)

    for game in box_scores:
        scores.append(game.home_score + game.away_score)

        homeTeamName = game.home_team.team_name
        awayTeamName = game.away_team.team_name

        if homeTeamName == teamName:
            homeTeamName = greenText(homeTeamName)

        if awayTeamName == teamName:
            awayTeamName = greenText(awayTeamName)

        matchups.append(homeTeamName + " | " + awayTeamName)

    snoozeFest = round(min(scores), 2)
    barnBurner = round(max(scores), 2)

    snoozeTeams = matchups[scores.index(min(scores))]
    burnerTeams = matchups[scores.index(max(scores))]

    roundUpAwards.add_row(["Barnburner Matchup", burnerTeams, str(barnBurner) + " combined points"])
    roundUpAwards.add_row(["Total Snoozefest", snoozeTeams, str(snoozeFest) + " combined points"])

def getVictoryMargins(league_index):
    roundUpAwards = roundUp.roundUpAwards
    margins = []
    matchups = []

    getLeague(league_index)
    box_scores = getLeague.league.box_scores(currentWeek)

    for game in box_scores:
        margins.append(abs(game.home_score - game.away_score))

        homeTeamName = game.home_team.team_name
        awayTeamName = game.away_team.team_name

        if homeTeamName == teamName:
            homeTeamName = greenText(homeTeamName)

        if awayTeamName == teamName:
            awayTeamName = greenText(awayTeamName)

        matchups.append(homeTeamName + " | " + awayTeamName)

    maxMargin = max(margins)
    minMargin = min(margins)

    maxMatchup = matchups[margins.index(maxMargin)]
    minMatchup = matchups[margins.index(minMargin)]

    maxMargin = round(maxMargin, 2)
    minMargin = round(minMargin, 2)

    if minMargin <= 10:
        minMargin = yellowText(minMargin)

    roundUpAwards.add_row(["Blowout of the Week", maxMatchup, str(maxMargin) + " point differential"])
    roundUpAwards.add_row(["Nailbiter of the Week", minMatchup, str(minMargin) + " point differential"])

def getScoreSummary(league_index):
    roundUpScoreboard = roundUp.roundUpScoreboard

    getLeague(league_index)
    box_scores = getLeague.league.box_scores(currentWeek)

    for game in box_scores:
        winScore = max([game.away_score, game.home_score])

        if winScore == game.away_score:
            winnerTeam = game.away_team.team_name
            loserTeam = game.home_team.team_name

            if winnerTeam == teamName:
                winnerTeam = greenText(winnerTeam)

            if loserTeam == teamName:
                loserTeam = greenText(loserTeam)

            winnerRecord = "(" + str(game.away_team.wins) + "-" + str(game.away_team.losses) + ")"
            loserRecord = "(" + str(game.home_team.wins) + "-" + str(game.home_team.losses) + ")"

            winnerScore = str(round(game.away_score, 2))
            loserScore = str(round(game.home_score, 2))
        else:
            winnerTeam = game.home_team.team_name
            loserTeam = game.away_team.team_name

            if winnerTeam == teamName:
                winnerTeam = greenText(winnerTeam)

            if loserTeam == teamName:
                loserTeam = greenText(loserTeam)

            winnerRecord = "(" + str(game.home_team.wins) + "-" + str(game.home_team.losses) + ")"
            loserRecord = "(" + str(game.away_team.wins) + "-" + str(game.away_team.losses) + ")"

            winnerScore = str(round(game.home_score, 2))
            loserScore = str(round(game.away_score, 2))

        roundUpScoreboard.add_row([winnerTeam + " " + winnerRecord, winnerScore, loserScore, loserTeam + " " + loserRecord])

def roundUpMenu():
    i = 0
    menu = {}

    for i in range(len(leagues) + 1):
        try:
            menu[str(i+1) + "."] = leagues[i][0]
        except:
            menu[str(i+1) + "."] = "All"
            menu[str(i+2) + "."] = "Go Back"

    while True:
        options = menu.keys()

        for entry in options:
            print(entry, menu[entry])

        roundUpSelection = int(input("Select a league: "))
        roundUpMenu.roundUpSelection = roundUpSelection

        if (roundUpSelection > 0) and (roundUpSelection <= len(leagues)):
            clear()
            roundUp((roundUpSelection - 1), currentWeek)
            break
        elif (roundUpSelection == (len(leagues) + 1)):
            clear()
            for i in range(roundUpSelection - 1):
                roundUp(i, currentWeek)
            break
        elif (roundUpSelection == (len(leagues) + 2)):
            clear()
            break
        else:
            print("Invalid selection! Try again.")

def roundUp(league_index, week):
    startTime = datetime.datetime.now()
    startTime = startTime.replace(microsecond = 0)
    print("\033[0;37;40mStarted at:", startTime)

    roundUpSelection = roundUpMenu.roundUpSelection

    roundUpScoreboard = PrettyTable()
    roundUpScoreboard.field_names = [
    negText("Winner"),
    negText("W"),
    negText("L"),
    negText("Loser")]

    roundUpAwards = PrettyTable()
    roundUpAwards.field_names = [
    negText("Award"),
    negText("Team(s)"),
    negText("Values")]

    roundUp.roundUpScoreboard = roundUpScoreboard
    roundUp.roundUpAwards = roundUpAwards

    getScoreSummary(league_index)
    getMinMaxScores(league_index)
    getVictoryMargins(league_index)
    getBenchScore(league_index)
    getTopScore(league_index)

    print("    " + negText("*~* " + leagueName + ": Week " + str(week) + " Round Up *~*"))
    print(roundUpScoreboard)
    print(roundUpAwards)

    finishTime = datetime.datetime.now()
    finishTime = finishTime.replace(microsecond = 0)
    runtime = finishTime - startTime
    print("Completed at:", finishTime, " (runtime:", runtime, ")")

def displayMenu():
    menu = {}
    menu["1."] = "Start Scoreboard"
    menu["2."] = "View Traitors"
    menu["3."] = "Round Up Report"
    menu["4."] = "Exit"

    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        mainSelection = input("Please Select: ")

        if mainSelection == "1":
            clear()
            try:
                getScores()

            except KeyboardInterrupt:
                clear()
                print("Please choose another option:\n")
                pass
        elif mainSelection == "2":
            clear()
            findTraitors()
            input("Press 'Enter' to return to menu...")
            clear()
        elif mainSelection == "3":
            clear()
            roundUpMenu()
            input("Press 'Enter' to return to main menu...")
            clear()
        elif mainSelection == "4":
            break
        else:
            print("Unknown option selected!")

clear()
displayMenu()
