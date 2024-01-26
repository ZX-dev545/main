import time

import praw
from pmaw import PushshiftAPI
import pandas as pd

from openai import OpenAI#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

reddit = praw.Reddit(client_id="Afl7Jlq5C3tpfp8jIJp7zA", client_secret="X5-bIpI6BK-6gfeuDEcZVAAQs2vEIQ", password="jigginaut",
    user_agent="Comment Extraction (by u/No-Assumption1527)",
    username="No-Assumption1527")
api = PushshiftAPI(praw=reddit)

# Creating keyword list
keyword_list = '"food, health"'

# Searching in all subreddits  
all = reddit.subreddit("all")
df = pd.DataFrame() # creating dataframe for displaying scraped data
stories = pd.DataFrame(columns=['CommentID', 'SubmissionID', 'Text', 'Upvotes'])

# creating lists for storing scraped data
titles=[]
scores=[]
ids=[]
raw = []

def slowly(func, *args):
    try:
        func(*args)
    except:
        time.sleep(10)
        slowly(func, *args)

# looping over posts and scraping it
for submission in all.search(keyword_list, limit=None):
    slowly(titles.append(submission.title))
    slowly(scores.append(submission.score)) #upvotes
    slowly(ids.append(submission.id))
    while True:
        try:
            comments = submission.comments
            break
        except:
            time.sleep(1)
    
    slowly(print(submission.id + ": " + str(len(comments))))
    #coms = [com for com in submission.comments]
    slowly(comments.replace_more(limit=None))
    for com in comments.list():
        #print(stories.shape[0])
        #print(submission.id)
        while True:
            try:
                line = str(com.body).replace('|', '')
                break
            except:
                time.sleep(1)

        line = line.replace(',', '|')
        line = line.replace('\n', '')
        #print(line)
        #print(com.ups)
        while True:
            try:
                stories.loc[stories.shape[0]] = [stories.shape[0], submission.id, line, com.ups]
                break
            except:
                time.sleep(1)

#cache_size = 1000
#comments = api.search_comments(q=keyword_list, subreddit="all", limit=cache_size, until=1629990795)
#for comment in comments:
#    raw.append(comment)
#    if len(raw) > cache_size:
#        break

#comment_list = ["www.reddit.com/" + com.permalink for com in raw]



df['Id'] = ids
df['Upvotes'] = scores #upvotes
df['Title'] = titles

print(df.shape)
df.to_csv("test.csv")
stories.to_csv("wishes.csv")

akhaten = OpenAI()

completion = akhaten.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a Food and Health administrator for a political party in charge of ascertaining peoples' problems and categorising them as efficiently as possible."},
    {"role": "user", "content": "These comments are lists of positive and normative statements. Convert these comments into python lists of strings. Each string should be either a positive or normative statement. Lists should be named in ascending order."}
  ]
)

lists = open("lists.txt")
lists.write(completion.choices[0].message)
lists.close()

completion = akhaten.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a Food and Health administrator for a political party in charge of ascertaining peoples' problems and categorising them as efficiently as possible."},
    {"role": "user", "content": "Write python code with pandas that saves a csv file with two columns: the ID of each repeated statement, and the number of times the statement is repeated."}
  ]
)