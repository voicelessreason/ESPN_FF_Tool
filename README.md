# ESPN_FF_Tool
<<<<<<< HEAD
 Small scripts to improve your QoL when using ESPN's fantasy football platform.

Dependencies:

[ff-espn-api](https://github.com/cwendt94/ff-espn-api) by cwendt94

[prettytable](https://github.com/jazzband/prettytable) by jazzband

```
pip install ff-espn-api
pip install prettytable
```  
=======
 Small scripts to improve your QoL when using ESPN's fantasy football platform. Must be running Python 3 or higher.
>>>>>>> merge1

The first script in the tool provides a constantly updating scoreboard as seen in the image below.
![image of first script](https://i.imgur.com/WBPZ9Zu.png)

The second script shows players that are starting on your team in 1+ league but against you in 1+ leagues as well.
<<<<<<< HEAD
![image of second script](https://i.imgur.com/8Czq7aU.png)

A userData.py file has been added to the script to act as a simple way to import/change league and team info. Simply adjust the variables in that file to fit according to your league, rename the file, and it will be automatically loaded.

NOTE: Please ensure your team names are spelled properly, this is the method used to determine which team belongs to you

NOTE: You MUST rename your default_userData.py file to userData.py otherwise this will not work
=======
![image of second script](https://i.imgur.com/zV0Enpo.png)

### Dependencies
- [ff-espn-api](https://github.com/cwendt94/ff-espn-api) from cwendt94
- [prettyTable](https://github.com/jazzband/prettytable) from jazzband

### Run Instructions
1. Copy default_userData.py into userData.py
2. In userData.py, enter the current week.
3. For each league you are in:

    a. Replace the value in league_names with your league name. If you are in multiple leagues, add them all to the array. Ex: [league1, league2, league3]

    b. Replace the sample information with your own. Copy the entire block and repeat for multiple leagues.

        i. Public Leagues: Leave the final two values as None for each league
        ii. Private Leagues: Visit your league's page and copy over the necessary fields from your cookies.  
4. Install the two necessary modules:

    a. `pip install ff_espn_api`

    b. `pip install prettyTable`
5. Run `python3 espnTool.py`
>>>>>>> merge1
