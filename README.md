# ESPN_FF_Tool
 Small scripts to improve your QoL when using ESPN's fantasy football platform. Must be running Python 3 or higher.

The first script provides a constantly updating scoreboard highlighting whether you are winning, losing, or tied.

![image of first script](https://i.imgur.com/WBPZ9Zu.png)

The second script shows players that you are both starting AND playing against in at least one league.

![image of second script](https://i.imgur.com/zV0Enpo.png)

### Dependencies
- [ff-espn-api](https://github.com/cwendt94/ff-espn-api) from cwendt94
- [prettyTable](https://github.com/jazzband/prettytable) from jazzband

### Run Instructions
1. Copy default_userData.py into userData.py
2. In userData.py, enter the current week. Update this each week to keep the tool up to date.
3. For each league you are in:

    a. Replace the value in "leagues" with the league variable. If you are in multiple leagues, add them all to the array. Ex: [league1, league2, league3]

    b. Replace the sample information with your own. Copy the entire block and repeat for multiple leagues.
        i. Public Leagues: Leave the final two values as None for each league
        ii. Private Leagues: Visit your league's page and copy over the necessary fields from your cookies
4. Install the two necessary modules:

    a. `pip install ff_espn_api`

    b. `pip install prettyTable`
5. Run `python3 espnTool.py`

### Credits
1. Obvious thanks to [cwendt94](https://github.com/cwendt94) and [jazzband](https://github.com/jazzband), without whom the project couldn't have gotten started
2. Big shoutout to [VoicelessReason](https://github.com/voicelessreason) for showing interest, making their own changes, and getting those changes implemented
