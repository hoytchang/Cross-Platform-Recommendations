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
top_subreddit = subreddit.top(limit=3)
for submission in top_subreddit:
	print('\n   title = ' + submission.title) #some times gives error UnicodeEncodeError: 'charmap' codec can't encode character
	raw_text += " " + submission.title
	print('    body = ' + submission.selftext)
	raw_text += " " + submission.selftext
	comments = submission.comments.list()
	max_comments = 1000
	n_comments = min(max_comments, len(comments))
	for i in range(n_comments):
		try:
			print('      comment ' + str(i) + ' = ' + comments[i].body)
			raw_text += " " + comments[i].body
		except:
			pass

#Use nltk to convert string into tokens (words and puncuation)
tokens = word_tokenize(raw_text)

#Use nltk to find frequency distribution of words
fdist = FreqDist(tokens)

#Remove tokens with only 1 or 2 characters
short_words = []
for i in fdist:
	if len(i) < 3:
		print('to be removed: ' + i)
		short_words.append(i)
for s in short_words:
	print('removing: '+s)
	fdist.pop(s)

#Remove common but useless tokens 
stop = set(stopwords.words('english')) #get pre-defined stop words
additional_stop = ['https','n\'t', 'like', 'buy'] #add additional stop words
for a in additional_stop:
	stop.add(a) 
for s in stop:
	try:
		fdist.pop(s)
	except:
		pass
#needs some work here to stem the tokens

