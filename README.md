# ESPN_FF_Tool
 Small scripts to improve your QoL when using ESPN's fantasy football platform.

Dependencies:

[ff-espn-api](https://github.com/cwendt94/ff-espn-api) by cwendt94

[prettytable](https://github.com/jazzband/prettytable) by jazzband

```
pip install ff-espn-api
pip install prettytable
```  

The first script in the tool provides a constantly updating scoreboard as seen in the image below.
![image of first script](https://i.imgur.com/WBPZ9Zu.png)

The second script shows players that are starting on your team in 1+ league but against you in 1+ leagues as well.
![image of second script](https://i.imgur.com/8Czq7aU.png)

A userData.py file has been added to the script to act as a simple way to import/change league and team info. Simply adjust the variables in that file to fit according to your league, rename the file, and it will be automatically loaded.

NOTE: Please ensure your team names are spelled properly, this is the method used to determine which team belongs to you

NOTE: You MUST rename your default_userData.py file to userData.py otherwise this will not work
