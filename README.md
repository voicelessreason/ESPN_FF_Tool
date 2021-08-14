# ESPN_FF_Tool
This is a tool for accessing the ESPN Fantasy Football API which provides two main functions:

1. A real-time display of all your matchups across all your leagues.

2. A report on the results of a given week's matchups in the league of your choice. This is primarily for commissioners who would like to add something to their league experience.

### Dependencies
- [ff-espn-api](https://github.com/cwendt94/ff-espn-api) from cwendt94
- [prettyTable](https://github.com/jazzband/prettytable) from jazzband

### Run Instructions

1. Retrieve three pieces of information, your `leagueId` (for each league), your `espn_s2` and your `swid`. After logging into the espn desktop website, you can find the `espn_s2` and  `swid` in the cookies. For each league, your `leagueId` will be visibile in the URL as a query param. 
2. Copy [default_userData.py](default_userData.py) into userData.py
3. In userData.py, enter the current week and year. Update this each week to keep the tool up to date.
4. For each league:

    a. Replace the value in "leagues" with the league variable. If in multiple leagues, add them all to the array. Ex: [league1, league2, league3]

    b. Replace the sample information with your own. Copy the entire block and repeat for multiple leagues.

5. Install the two necessary modules:

    a. `pip install ff_espn_api`

    b. `pip install prettyTable`

5. Run `python3 espnTool.py`

### Credits
1. Huge credit is owed to [cwendt94](https://github.com/cwendt94) and [jazzband](https://github.com/jazzband)
2. Big thanks to [Drippyer](https://github.com/drippyer/) for starting the project and writing the score display functionality
