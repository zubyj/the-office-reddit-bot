# the-office-reddit-bot

## Overview
* Reddit bot that gets triggered by certain keywords and responds to comments with character lines from NBC's, "The Office"

* The response is generated from [The Reddit Script API](https://theofficescript.com). You can use it [here](https://github.com/zubyj/the-office-api) or check out the [github](https://github.com/zubyj/the-office-api)

* <b>Technologies</b>: Python, SQLite3,  [The Office Script API](https://theofficescript.com), PRAW (Python-Reddit API Wrapper)

<hr>

## Getting Started

1. Create a Reddit account for the bot

2. Create a Reddit app to obtain the API key and secret

3. Download PRAW (Python-Reddit API Wrapper)

4. Use the API key and secret to authenticate the bot & use the Reddit API

5. Browse certain subreddits with comments that include keywords such as 'michael-bot' 'dwight-bot', etc

6. Make an API request to [The Office API](https://www.theofficescript.com/#ask_question_character) given the character and reddit comment

7. Use the API response to reply to the comment and store the comment id using SQLite (avoids spamming same comment)

<hr>

## Example 

The bot browses the DunderMifflin subreddit and reads the following comment

>"hey dwight-bot do bears eat beets"

The bot makes an API request to [theofficescript.com](https://theofficescript.com)

>[theofficescript.com/characters/dwight/ask/bears-eat-beets](https://theofficescript.com/characters/dwight/ask/hey-do-bears-eat-beets)

The API responds with 

>{
season : 3
episode : 20
line : Bears do not--- What is going on--- What are you doing?!
}

The bot replies to the Reddit comment using the response









