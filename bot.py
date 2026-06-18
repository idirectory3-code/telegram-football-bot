import requests
import datetime
API_KEY = "cfbacad76c4e4fa4b77ee318ffe139f9"
last_scores = {}


def get_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []

    matches = []

def get_matches():

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []

    for item in data.get("response", [])[:10]:

        league = item["league"]["name"]

        allowed_keywords = [
            "Tanzania", "Zanzibar", "England", "Spain",
            "Italy", "Germany", "France",
            "Cup", "Champions League", "Europa", "Conference"
        ]

        if any(x.lower() in league.lower() for x in allowed_keywords):

            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            score = item["goals"]

            minute = item["fixture"]["status"]["elapsed"]
            status = item["fixture"]["status"]["short"]
            
            matches.append(
                f"🔥 {league}\n"
                f"⚽ {home} vs {away}\n"
                f"📊 {score['home']} - {score['away']}\n"
                f"⏱️ {minute}'\n"
                f"🟢 {status}\n"
)

    return "\n".join(matches)
async def goal_check(context: ContextTypes.DEFAULT_TYPE):

    global last_scores

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    for item in data.get("response", []):

        home = item["teams"]["home"]["name"]
        away = item["teams"]["away"]["name"]

        home_goals = item["goals"]["home"]
        away_goals = item["goals"]["away"]

        fixture_id = item["fixture"]["id"]

        current_score = f"{home_goals}-{away_goals}"

        # check if score changed
        if fixture_id in last_scores:

            if last_scores[fixture_id] != current_score:

                await context.bot.send_message(
                    chat_id="@mohdalisportsupdates",
                    text=(
                        f"🚨 GOAL ALERT 🚨\n\n"
                        f"⚽ {home} vs {away}\n"
                        f"📊 {current_score}"
                    )
                )

        last_scores[fixture_id] = current_score
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# KEEP YOUR OWN TOKEN
TOKEN = "8697383175:AAEr6Ne_Xfpy-IHuQQLTETvXaZDao_1DLTU"

# KEEP YOUR OWN CHANNEL ID
CHANNEL_ID ="@mohdalisportsupdates"


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_matches()
async def fixtures(update: Update, context: ContextTypes.DEFAULT_TYPE):

    leagues = [
        39,   # Premier League
        140,  # La Liga
        135,  # Serie A
        78,   # Bundesliga
        61,   # Ligue 1
        2,    # UEFA Champions League
        103,  # Tanzania Premier League (if available in API)
    ]

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    all_matches = []

    for league_id in leagues:

        url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=5"

        response = requests.get(url, headers=headers)
        data = response.json()

        for item in data.get("response", []):

            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            league = item["league"]["name"]

            all_matches.append(
                f"🏆 {league}\n"
                f"⚽ {home} vs {away}\n"
            )

    if not all_matches:
        await update.message.reply_text("📅 No fixtures found right now.")
        return

    await update.message.reply_text("\n".join(all_matches))
    await update.message.reply_text("\n".join(matches))
# MANUAL POST COMMAND
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id="@mohdalisportsupdates",
        text="⚽ Manual football post working"
    )

    await update.message.reply_text("✅ Post sent")


# AUTO POST FUNCTION
async def auto_post(context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id="@mohdalisportsupdates",
        text="⚽ Auto football update working"
    )

    print("AUTO POST SENT")


async def auto_post(context: ContextTypes.DEFAULT_TYPE):

    matches = get_matches()

    if not matches:
        matches = "No live matches now ⚽"

    await context.bot.send_message(
        chat_id="@mohdalisportsupdates",
        text="🔥 LIVE FOOTBALL UPDATE\n\n" + matches
    )

    print("AUTO POST SENT")

# CREATE BOT
app = Application.builder().token(TOKEN).build()


# COMMANDS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
app.add_handler(CommandHandler("test", test))
app.add_handler(CommandHandler("fixtures", fixtures))

# AUTO POST EVERY 60 SECONDS
app.job_queue.run_repeating(
    auto_post,
    interval=600,
    first=10
)
app.job_queue.run_repeating(
    goal_check,
    interval=60,
    first=5
)

print("🚀 Bot running...")
app.run_polling()
