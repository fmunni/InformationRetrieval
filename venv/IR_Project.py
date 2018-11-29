import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit('bot1',user_agent='my user agent')


#nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']

def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']

def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']

def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def main():
    from praw.models import MoreComments
    URL ='https://www.reddit.com/r/Conservative/comments/9sy2s7/barbra_streisand_may_move_to_canada_if/?fbclid=IwAR27kKy3HOF218rYnmA7IeRgheNvG4njb19jRaKitRDNgC711ygVIVlcqxY'
    submission = reddit.submission(url=URL)
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        print(top_level_comment.score, top_level_comment.body)

main()
