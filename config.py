import os

# Telegram
BOT_TOKEN = os.environ["BOT_TOKEN"]

# The Odds API
ODDS_API_KEY = os.environ["ODDS_API_KEY"]

# Football
SPORT = "soccer"
REGIONS = "eu"
BOOKMAKERS = "pinnacle"
MARKETS = "h2h"
ODDS_FORMAT = "decimal"

# Monitoring
CHECK_INTERVAL = 10800      # 3 часа
ALERT_DROP = 0.10           # спад 0.10

# Database
DATABASE = "matches.db"

# Logging
LOG_LEVEL = "INFO"