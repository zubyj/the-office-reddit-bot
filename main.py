#
"""

The Office Reddit Response Bots
Created by Zuby

"""


from dotenv import load_dotenv
import praw
import os, requests, sqlite3
from utils import format_comment


class The_Office_Bot:
    def __init__(self):
        load_dotenv()

        # Authenticate account with Reddit API
        self.reddit = praw.Reddit(
            client_id=os.getenv("ID"),
            client_secret=os.getenv("SECRET"),
            password=os.getenv("PASSWORD"),
            user_agent=os.getenv("USER_AGENT"),
            username=os.getenv("USERNAME"),
        )
        self.subreddit = self.reddit.subreddit("BotsPlayHere")

        # Connect to the database
        self.conn = sqlite3.connect("replied_comments.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS comments (id text)""")

        # Available characters that can be asked questions in the API
        # https://www.theofficescript.com/#ask_question_character
        self.bots = ["michael-bot", "dwight-bot", "jim-bot", "pam-bot", "andy-bot"]
        self.character = "michael"  # The character referenced by the reddit comment
        self.names = {
            "michael": "Michael Scott",
            "dwight": "Dwight Schrute",
            "pam": "Pam Beesly",
            "jim": "Jim Halpert",
            "andy": "Andy Bernard",
        }

    # Checks if our bots mentioned in reddit comment
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

        # Ensures we havent already responded to the comment
        self.c.execute("SELECT * FROM comments WHERE id=?", (comment.id,))
        if self.c.fetchone() is not None:
            valid = False
        return valid

    def run(self):
        for comment in self.subreddit.stream.comments():
            if self.is_valid(comment):
                commentBody = format_comment(self.character, comment.body)

                # Make API request with given character and Reddit comment
                response = requests.get(
                    "https://theofficescript.com/characters/"
                    + self.character
                    + "/ask/"
                    + commentBody
                )
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
                self.c.execute("INSERT INTO comments VALUES (?)", (comment.id,))
                self.conn.commit()


if __name__ == "__main__":
    bot = The_Office_Bot()
    bot.run()
