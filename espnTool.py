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
            currentLeague = leagues[x]
            leagueName = currentLeague[0]
            leagueID = currentLeague[1]
            teamName = currentLeague[2]
            username = currentLeague[3]
            password = currentLeague[4]
            league = League(leagueID, year, username, password)
            box_score = league.box_scores(currentWeek)
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
        "\033[0;30;47m WEEK " + str(currentWeek) + " \033[0;37;40m",
        "\033[0;30;47m Pos. \033[0;37;40m",
        "\033[0;30;47m For \033[0;37;40m",
        "\033[0;30;47m Opp. \033[0;37;40m"]
    for x in range(len(leagues)):
        currentLeague = leagues[x]
        leagueName = currentLeague[0]
        leagueID = currentLeague[1]
        teamName = currentLeague[2]
        username = currentLeague[3]
        password = currentLeague[4]
        league = League(leagueID, year, username, password)
        box_score = league.box_scores(currentWeek)
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
    playerList = list(dict.fromkeys(fullPlayers))
    for i in range(len(playerList)):
        if (playerList[i][1] > 0) and ((playerList[i][2] > 0)):
            displayName = playerList[i][0][0]
            displayPos = playerList[i][0][1]
            plays = playerList[i][1] + playerList[i][2]
            traitorTable.add_row([displayName, displayPos, playerList[i][1], playerList[i][2]])
    traitorTable.sortby = "\033[0;30;47m Pos. \033[0;37;40m"
    print(traitorTable)
    finishTime = datetime.datetime.now()
    finishTime = finishTime.replace(microsecond = 0)
    runtime = finishTime - startTime
    print("Updated: ", finishTime, "\nRuntime: ", runtime, "")

def displayMenu():
    menu = {}
    menu['1.'] = "Start Scoreboard"
    menu['2.'] = "View Traitors"
    menu['3.'] = "TBD"
    menu['4.'] = "Exit"
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
            findTraitors()
            input("Press 'Enter' to continue...")
        elif selection == '3':
            print("Nothing here yet!")
        elif selection == '4':
            break
        else:
            print("Unknown option selected!")

clear()
displayMenu()
