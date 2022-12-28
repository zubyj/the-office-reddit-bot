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

        # Available characters that can be asked questions on The Office Script API
        self.bots = ['michael-bot', 'dwight-bot', 'jim-bot', 'pam-bot', 'andy-bot']

        self.character = 'michael'

        self.names = {
            'michael' : 'Michael Scott',
            'dwight' : 'Dwight Schrute',
            'pam' : 'Pam Beesly',
            'jim' : 'Jim Halpert',
            'andy' : 'Andy Bernard',
        }


    # format Reddit comment to send to API
    def format_comment(self, comment):
        # remove the word michael-bot
        comment = comment.split()
        botName = self.character + '-bot'
        filtered_comment = [word for word in comment if botName not in word]
        comment = ' '.join(filtered_comment)
        # remove nonalphanumeric chars
        comment = re.sub(r'[^a-zA-Z0-9\s]', '', comment)
        # remove extra whitespaces 
        comment = ' '.join(comment.split())
        comment = comment.replace(' ' , '-')
        if comment[-1] == '-':
            comment = comment[:-1]
        return comment


    def is_valid(self, comment):
        valid = False
        # checks if comment contains keyword
        for bot in self.bots:
            if bot in comment.body.lower():
                valid = True
                self.character = bot.split('-')[0]
        if not valid: return False

        if comment.author == 'the-office-bot':
            return False

        # checks if comment hasnt already been replied to
        self.c.execute('SELECT * FROM comments WHERE id=?', (comment.id,))
        if self.c.fetchone() is not None:
            valid = False
        return valid


    def run(self):
        for comment in self.subreddit.stream.comments():
            if self.is_valid(comment):
                # reply if bot hasnt already replied
                commentBody = self.format_comment(comment.body)

                # get response from The Office Script API
                response = requests.get("https://theofficescript.com/characters/" + self.character + "/ask/" + commentBody)
                response = response.json()

                line = response['response']
                season = str(response['season'])
                episode = str(response['episode'])
                botResponse = line + "\n\n" + "-" + self.names[self.character]+ "\n\nSeason " + season + " Episode " + episode
                comment.reply(botResponse)
                print('comment ' + commentBody)
                print('response ' + botResponse)

                self.c.execute('INSERT INTO comments VALUES (?)', (comment.id,))
                self.conn.commit()


bot = The_Office_Bot()

bot.run()





