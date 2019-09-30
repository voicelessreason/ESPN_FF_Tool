from ff_espn_api import League
from prettytable import PrettyTable
from collections import Counter
from os import system, name
from time import sleep
import datetime

####################################################################
## Do not edit above this line if you don't know what you're doing

# this should be usable across seasons, just be sure to update year and other info below
year = 2019
# change this value each wweek to ensure you are comparing the right teams
currentWeek = 4
# input all league IDs separated by commas (required)
leagues = [11111111, 22222222, 33333333]
# optional
leagueNames = ["The boiz", "Throwback", "New Gang"]
# TEAM NAMES BELOW MUST MATCH YOUR TEAM NAME ON ESPN (required)
teamNames = ["Quarter Chubb", "Hyde and Zeke", "As Far As the Eye Kelce"]

## Do not edit below this line if you don't know what you're doing
####################################################################

beginTime = datetime.datetime.now()
beginTime = beginTime.replace(microsecond = 0)
timesLooped = 0
myPlayers = []
oppPlayers = []
allPlayers = []
fullPlayers= []

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def getScores():
    global timesLooped
    global finishTime
    if timesLooped == 0:
        startTime = beginTime
    else:
        startTime = finishTime
    startTime = startTime.replace(microsecond = 0)
    print("\033[0;37;40mStarted at: ", startTime)
    boxScore = PrettyTable()
    boxScore.field_names = [
        "\033[0;30;47m League \033[0;37;40m",
        "\033[0;30;47m Home Team \033[0;37;40m",
        "\033[0;30;47m H \033[0;37;40m",
        "\033[0;30;47m vs \033[0;37;40m",
        "\033[0;30;47m A \033[0;37;40m",
        "\033[0;30;47m Away Team \033[0;37;40m"]
    for x in range(len(leagues)):
        league_id = leagues[x]
        league = League(league_id, year)
        box_score = league.box_scores(currentWeek)
        i = 0
        for i in range(len(box_score)):
            home_team = box_score[i].home_team
            away_team = box_score[i].away_team
            home_name = home_team.team_name
            away_name = away_team.team_name
            if home_name == teamNames[x]:
                home_score = box_score[i].home_score
                away_score = box_score[i].away_score
                home_name = "\033[1;32;40m " + home_name + " \033[0;37;40m"
                if home_score > away_score:
                    home_score = "\033[1;32;40m " + str(home_score) + " \033[0;37;40m"
                else:
                    home_score = "\033[1;31;40m " + str(home_score) + " \033[0;37;40m"
                boxScore.add_row([leagueNames[x], home_name, home_score , "vs", away_score, away_name])
            if away_name == teamNames[x]:
                home_score = box_score[i].home_score
                away_score = box_score[i].away_score
                away_name = "\033[1;32;40m " + away_name + " \033[0;37;40m"
                if away_score > home_score:
                    away_score = "\033[1;32;40m " + str(away_score) + " \033[0;37;40m"
                else:
                    away_score = "\033[1;31;40m " + str(away_score) + " \033[0;37;40m"
                boxScore.add_row([leagueNames[x], home_name, home_score , "vs", away_score, away_name])
    finishTime = datetime.datetime.now()
    finishTime = finishTime.replace(microsecond = 0)
    runtime = finishTime - startTime
    timesLooped = timesLooped + 1
    print(boxScore)
    print("[", timesLooped, "] ", "Updated: ", finishTime, " (runtime: ", runtime, ")\n")

def findTraitors():
    global timesLooped
    global finishTime
    global myPlayers
    global oppPlayers
    global allPlayers
    print("\033[0;37;40mStarted at: ", beginTime)
    if timesLooped == 0:
        startTime = beginTime
    else:
        startTime = finishTime
    traitorTable = PrettyTable()
    traitorTable.clear()
    traitorTable.field_names = [
        "\033[0;30;47m WEEK " + str(currentWeek) + " \033[0;37;40m",
        "\033[0;30;47m Pos. \033[0;37;40m",
        "\033[0;30;47m For \033[0;37;40m",
        "\033[0;30;47m Opp. \033[0;37;40m"]
    for x in range(len(leagues)):
        league_id = leagues[x]
        league = League(league_id, year)
        box_score = league.box_scores(currentWeek)
        i = 0
        for i in range(len(box_score)):
            home_team = box_score[i].home_team
            away_team = box_score[i].away_team
            home_name = home_team.team_name
            away_name = away_team.team_name
            if home_name == teamNames[x]:
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
            if away_name == teamNames[x]:
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
                while True:
                    getScores()
            except KeyboardInterrupt:
                clear()
                print("Please choose another option:")
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
