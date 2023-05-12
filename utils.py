import re

# Format Reddit comment for API request
def format_comment(character, comment):
    # remove the word michael-bot
    comment = comment.split()
    botName = character + "-bot"
    filtered_comment = [word for word in comment if botName not in word]
    comment = " ".join(filtered_comment)
    # remove nonalphanumeric chars
    comment = re.sub(r"[^a-zA-Z0-9\s]", "", comment)
    # remove extra whitespaces
    comment = " ".join(comment.split())
    comment = comment.replace(" ", "-")
    if comment[-1] == "-":
        comment = comment[:-1]
    return comment
