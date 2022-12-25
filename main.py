from dotenv import load_dotenv
import praw
import os
import requests

class The_Office_Bot:

    def __init__(self):
        load_dotenv()
        print('testing the office bot')

        # Initialize Reddit object / Log into account
        self.reddit = praw.Reddit(
            client_id=os.getenv('ID'),
            client_secret=os.getenv('SECRET'),
            password=os.getenv('PASSWORD'),
            user_agent=os.getenv('USER_AGENT'),
            username=os.getenv('USERNAME'),
)
        self.subreddit = self.reddit.subreddit("BotsPlayHere")


    def run(self):
        for comment in self.subreddit.stream.comments():
            if not comment.saved and "michael-bot" in comment.body:
                print('replied to ' + comment.body)
                theComment = comment.body.replace('michael-bot', '')
                theComment = theComment.replace(" ", "-")
                theComment = theComment[:-1] if theComment[-1] == '-' else theComment
                print("the comment: " + theComment)
                response = requests.get("https://theofficescript.com/characters/michael/ask/" + theComment)
                response = response.json()

                line = response['response']
                season = str(response['season'])
                episode = str(response['episode'])

                botResponse = line + "\n\nseason " + season + " episode: " + episode
                print('response : ' + botResponse)
                comment.reply(botResponse)
                comment.save()

bot = The_Office_Bot()

bot.run()





