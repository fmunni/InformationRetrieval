import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
import pprint
from datetime import datetime

def print_submission_info(submission):
    account_creation_date = datetime.fromtimestamp(submission.author.created_utc)
    account_link_karma = submission.author.link_karma
    upvote_ratio = submission.upvote_ratio  # The percentage of upvotes from all votes on the submission.

    print("%s\n\t%f, %s, %s, %s" % (
    submission.title, upvote_ratio, submission.author, account_creation_date, account_link_karma))


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def flatten_comment_forest(commentList, commentListContainer):
    for comment in commentList:
        commentListContainer.append(str(comment.score) + ":::" + comment.body)
        if comment.replies != None:
            flatten_comment_forest(comment.replies.list(), commentListContainer)


def write_submission_comments_to_file(subreddit, submission, sort=True):
    f = open("./"+subreddit+"/"+submission.title + ".txt", 'w')

    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()
    all_comments = []
    flatten_comment_forest(comments, all_comments)

    if sort:
        all_comments = sorted(comments, key=lambda x: x.score)

    for comment in all_comments:
        if type(comment) == 'str':
            print(comment)
            continue
        body = comment.body.replace("\r", " ")
        body = body.replace("\n", ' ')
        f.write(str(comment.score) + ":::" + body + "\n")
    f.close()




# May be useful
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




# START MAIN CODE

# Global Vars
overwrite_existing = True
reddit = praw.Reddit('bot1', user_agent='my user agent')
subreddits = [
    'Politics',
    'The_Donald'
]

for subreddit in subreddits:
    if not os.path.exists("./"+subreddit+"/"):
        os.makedirs("./"+subreddit+"/")

    hot_posts_generator = reddit.subreddit(subreddit).hot()
    num_posts_to_parse = 5

    while num_posts_to_parse > 0:
        submission = hot_posts_generator.next()
        if os.path.isfile("./" + subreddit + "/" + submission.title + ".txt"):
            if not overwrite_existing:
                continue
        print_submission_info(submission)
        write_submission_comments_to_file(subreddit, submission, overwrite_existing)
        num_posts_to_parse -= 1

