import sys
import os
import praw
from myRedditKeys import myRedditKeys
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords

#Set encoding to UTF-8 to avoid Unicode Encode Error
if sys.platform == "win32":
	os.system('chcp 65001')

#Get reddit API keys.  You need to create a reddit account and go to "preferences" and apps" and click "create an app" to get the keys.
[client_id, client_secret, user_agent, username, password] = myRedditKeys()

#Set up reddit API
reddit = praw.Reddit(client_id = client_id,
	client_secret = client_secret,
	user_agent = user_agent,
	username = username,
	password = password)

#Specify subreddit you want to get recommendations on. For example, put in 'bitcoin' for https://www.reddit.com/r/Bitcoin/
sr = 'bitcoin'

#For each submission get the title, body, and comment.  For each comment, get the body.  Store everything in raw_text.
raw_text = ""
subreddit = reddit.subreddit(sr)
print("Getting data from "+subreddit._path)
top_subreddit = subreddit.top(limit=3) #use low limit for debugging, high limit for more data
count_submission = 0
count_comment = 0
for submission in top_subreddit:
	raw_text += " " + submission.title #add title
	raw_text += " " + submission.selftext #add body
	count_submission += 1
	comments = submission.comments.list()
	max_comments = 1000 #put a cap on how many comments per submission
	n_comments = min(max_comments, len(comments))
	for i in range(n_comments):
		if not isinstance(comments[i], praw.models.reddit.more.MoreComments): #avoid MoreComments
			raw_text += " " + comments[i].body #add comment
			count_comment += 1
print("Collected data from " + str(count_submission) + " submissions and " + str(count_comment) + " comments.")

#Use nltk to convert string into tokens (words and puncuation)
tokens = word_tokenize(raw_text)

#Use nltk to find frequency distribution of words
fdist = FreqDist(tokens)

#Remove tokens with only 1 or 2 characters
short_words = []
for i in fdist:
	if len(i) < 3:
		short_words.append(i)
for s in short_words:
	fdist.pop(s)

#Remove common but useless tokens 
stop = set(stopwords.words('english')) #get pre-defined stop words
additional_stop = ['https','http','n\'t','The','This','That','...'] #add additional stop words
for a in additional_stop:
	stop.add(a) 
for s in stop:
	try:
		fdist.pop(s)
	except:
		pass

#needs some work here to stem the tokens


#print results of nltk
print("The 50 most commonly used words in this subreddit: ")
for f in fdist.most_common(50):
	print(f)

#search youtube