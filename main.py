from dotenv import load_dotenv
import praw
import os, requests, re
import sqlite3

class The_Office_Bot:

    def __init__(self):
        load_dotenv()
        print('testing the office bot')

        # Authenticate account with Reddit API
        self.reddit = praw.Reddit(
            client_id=os.getenv('ID'),
            client_secret=os.getenv('SECRET'),
            password=os.getenv('PASSWORD'),
            user_agent=os.getenv('USER_AGENT'),
            username=os.getenv('USERNAME'),
        )
        self.subreddit = self.reddit.subreddit("BotsPlayHere")

        # Connect to the database
        self.conn = sqlite3.connect('replied_comments.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS comments (id text)''')


    # format Reddit comment to send to API
    def format_comment(self, comment):

        # remove the word michael-bot
        comment = comment.split()
        filtered_comment = [word for word in comment if 'michael-bot' not in word]
        comment = ' '.join(filtered_comment)
        # remove nonalphanumeric chars
        comment = re.sub(r'[^a-zA-Z0-9\s]', '', comment)
        # remove extra whitespaces 
        comment = ' '.join(comment.split())
        comment = comment.replace(' ' , '-')
        if comment[-1] == '-':
            comment = comment[:-1]
        return comment


    def run(self):
        for comment in self.subreddit.stream.comments():
            if not comment.saved and "michael-bot" in comment.body:
                commentBody = self.format_comment(comment.body)

                response = requests.get("https://theofficescript.com/characters/michael/ask/" + commentBody)
                response = response.json()

                line = response['response']
                season = str(response['season'])
                episode = str(response['episode'])

                botResponse = line + "\n\nseason " + season + " episode: " + episode

#               comment.reply(botResponse)
#               comment.save()

                self.c.execute('SELECT * FROM comments WHERE id=?', (comment.id,))

                # check if bot already replied to comment
                if self.c.fetchone() is None:
                    print('already replied to comment')
                    print(commentBody)
                    self.c.execute('INSERT INTO comments VALUES (?)', (comment.id,))
                    self.conn.commit()



bot = The_Office_Bot()

bot.run()





