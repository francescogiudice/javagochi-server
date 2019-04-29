MAX_USER_LEVEL = 50
MAX_JAVAGOCHI_LEVEL = 50

# Prevents superusers' Javagochis to take damage. Set to False to disabilitate
KILL_ALL = True

# At what percentage of the health the warning email is sent
JC_HEALTH_PERC_THRESHOLD = 10
# Cointains the amount of hot and cold increase in the various seasons
HOT_N_COLD_PER_SEASON = {
    "spring": {
        "hot": 10,
        "cold": -10
    },
    "autumn": {
        "hot": -10,
        "cold": 10
    },
    "summer": {
        "hot": 25,
        "cold": -30
    },
    "winter": {
        "hot": -30,
        "cold": 25
    }
}

# Fight details
STRONG_VS_MULTIPLIER = 2
LEVELS_LOST_ON_BATTLE = 5
USER_EXP_GAINED_ON_BATTLE = 500
JC_EXP_GAINED_ON_BATTLE = 1000

# Email details
EMAIL_SUBJECT = 'Your Javagochi is suffering!'
EMAIL_CONTENT = 'Help! Your Javagochi {} is suffering and is about to die!'
