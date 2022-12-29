import unittest
from utils import format_comment
import requests


class TestBotMethods(unittest.TestCase):

    def test_format_dwight_comment_1(self):
        comment = 'hey /u/dwight-bot do bears eat beets'
        self.assertEqual('hey-do-bears-eat-beets', format_comment('dwight', comment))


    def test_format_dwight_comment_2(self):
        comment = 'i hate you so much dwight-bot'
        self.assertEqual('i-hate-you-so-much', format_comment('dwight', comment))


    def test_format_dwight_comment_3(self):
        comment = 'u/dwight-bot what are you doing'
        self.assertEqual('what-are-you-doing', format_comment('dwight', comment))


    def test_format_dwight_comment_4(self):
        comment = 'u/dwight-bot what are you doing?'
        self.assertEqual('what-are-you-doing', format_comment('dwight', comment))


    def test_format_andy_comment_1(self):
        comment = 'andy-bot is so annoying..'
        self.assertEquals('is-so-annoying', format_comment('andy', comment))

    def test_format_michael_comment_1(self):
        comment = ' what is wrong with michael-bot. stop'
        self.assertEqual('what-is-wrong-with-stop', format_comment('michael', comment))


    def test_api_response(self):
        # test api response
        # Make API request with given character and Reddit comment
        comment = 'what-are-you-doing'
        response = requests.get("https://theofficescript.com/characters/dwight/ask/" + comment).json()['response']
        self.assertEqual("We search for the organs. Where's the heart? The precious heart.", response)


# run them unit tests
if __name__ == '__main__':
    unittest.main()