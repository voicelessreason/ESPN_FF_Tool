currentWeek = 5                         # Change this each week

year = 2019                             # Change this to reflect each season

                                        # If any leagues are private
espnUsername = "SampleUsername"         # input username here and
espnPassword = "SamplePassword"         # input password here then
                                        # modify variable names below

league1 = [
    "Sample League Name One",           # League Name
    11111111,                           # League ID
    "Sample Team Name One",             # Team Name (MUST BE CORRECT FOR YOUR TEAM)
    espnUsername,                       # either (espnUsername) or (None)
    espnPassword                        # either (espnPassword) or (None)
    ]

league2 = [
    "Sample League Name Two",           # League Name
    22222222,                           # League ID
    "Sample Team Name Two",             # Team Name (MUST BE CORRECT FOR YOUR TEAM)
    None,                               # either (espnUsername) or (None)
    None                                # either (espnPassword) or (None)
    ]

league3 = [
    "Sample League Name Three",         # League Name
    33333333,                           # League ID
    "Sample Team Name Three",           # Team Name (MUST BE CORRECT FOR YOUR TEAM)
    None,                               # either (espnUsername) or (None)
    None                                # either (espnPassword) or (None)
    ]

leagues = [league1, league2, league3]
