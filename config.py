import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
ODDS_API_KEY = os.environ["ODDS_API_KEY"]

SPORT = "soccer"
REGION = "eu"
BOOKMAKER = "pinnacle"

CHECK_INTERVAL = 300  # 5 минути

ALERT_DROP = 0.10

DATABASE = "matches.db"
LOG_LEVEL = "INFO"