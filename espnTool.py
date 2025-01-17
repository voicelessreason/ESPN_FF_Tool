from ff_espn_api import League
from prettytable import PrettyTable
from os import system, name
import datetime
from userData import (currentWeek, year, leagues)
from roundUpReport import (roundUp)

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


def initializeLeagues():
    global leagues_initialized
    if not leagues_initialized:
        for league in leagues:
            authed_leagues.append(League(league["leagueID"], year, league["espn_s2"], league["swid"]))
            leagues_initialized = True

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
           roundUp((selection - 1), currentWeek, authed_leagues)
           break
        else:
            print("Invalid selection! Try again.")

def displayMenu():
    menu = {}
    menu['1.'] = "Start Scoreboard"
    menu['2.'] = "Round Up Report"
    menu['3.'] = "Exit"
    while True:
        options = menu.keys()
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
