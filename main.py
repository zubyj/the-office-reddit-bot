from dotenv import load_dotenv
import praw
import os, requests, sqlite3
from utils import format_comment
import re, time


class The_Office_Bot:
    def __init__(self):
        load_dotenv()

        # Authenticate account with Reddit API
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            username=os.getenv("REDDIT_USERNAME"),
        )
        self.subreddit = self.reddit.subreddit("DunderMifflin")

        # Available characters that can be asked questions in the API
        self.bots = ["michael-bot", "dwight-bot", "jim-bot", "pam-bot", "andy-bot"]
        self.character = "michael"  # The character referenced by the reddit comment
        self.names = {
            "michael": "Michael Scott",
            "dwight": "Dwight Schrute",
            "pam": "Pam Beesly",
            "jim": "Jim Halpert",
            "andy": "Andy Bernard",
        }

    # Checks if we should respond to comment
    def is_valid(self, comment):
        if comment.author == "the-office-bot":
            return False

        valid = False
        for bot in self.bots:
            if bot in comment.body.lower():
                valid = True
                self.character = bot.split("-")[0]
        if not valid:
            return False

        # Checks if we haven't already responded to the comment
        with sqlite3.connect("replied_comments.db") as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS comments (id text)""")
            c.execute("SELECT * FROM comments WHERE id=?", (comment.id,))
            if c.fetchone() is not None:
                valid = False
        return valid

    def run(self):
        print("Bot is running on the subreddit " + self.subreddit.display_name)
        for comment in self.subreddit.stream.comments():
            try:
                if self.is_valid(comment):
                    commentBody = format_comment(self.character, comment.body)

                    # Make API request with given character and Reddit comment
                    response = requests.get(
                        "https://theofficescript.com/characters/"
                        + self.character
                        + "/ask/"
                        + commentBody
                    )
                    response.raise_for_status()
                    response = response.json()

                    # Format JSON response to respond to user
                    line = response["response"]
                    season = str(response["season"])
                    episode = str(response["episode"])
                    botResponse = (
                        line
                        + "\n\n"
                        + "-"
                        + self.names[self.character]
                        + "\n\nSeason "
                        + season
                        + " Episode "
                        + episode
                    )

                    comment.reply(botResponse)
                    print("comment : " + commentBody + ", response : " + botResponse)

                    # Store comment id in database (avoids replying more than once)
                    with sqlite3.connect("replied_comments.db") as conn:
                        c = conn.cursor()
                        c.execute("INSERT INTO comments VALUES (?)", (comment.id,))
                        conn.commit()

            except praw.exceptions.APIException as e:
                if e.attributes.get("error_type") == "RATELIMIT":
                    delay = re.search("(\d+) minutes?", e.message)
                    if delay:
                        delay_seconds = float(int(delay.group(1)) * 60)
                        print(f"Rate limit hit. Sleeping for {delay_seconds} seconds.")
                        time.sleep(delay_seconds)
                        continue
                    else:
                        delay = re.search("(\d+) seconds?", e.message)
                        delay_seconds = float(delay.group(1))
                        print(f"Rate limit hit. Sleeping for {delay_seconds} seconds.")
                        time.sleep(delay_seconds)
                        continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue


if __name__ == "__main__":
    bot = The_Office_Bot()
    bot.run()
