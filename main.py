from dotenv import load_dotenv
import praw
import os

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
        print(self.reddit.read_only)

run = The_Office_Bot()





