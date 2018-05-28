import sys
import os
import praw
from myRedditKeys import myRedditKeys
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup as bs

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

#Needs some work here to stem the tokens


#Print results of nltk
print("The 50 most commonly used words in this subreddit: ")
for f in fdist.most_common(50):
	print(f)

#Search youtube.  
#For now, just search the subreddit name.  
#Later, we can search all the tokens from the subreddit, and also search the youtube comments to find better matches.
base = "https://www.youtube.com/results?search_query="
qstring = sr
r = requests.get(base+qstring)
page = r.text

#parse using beautiful soup
soup = bs(page,'html.parser')

#Find all <a> tags because they define hyper-links.  The parameter href is the link.
#Only find <a> tags that are classified as YouTube User Interface XML Tile Links: yt-uix-tile-link
vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})

#Extract weblink for each tile using the href property.  Append to list.
videolist = []
videoname = []
for v in vids:
	tmp = 'https://www.youtube.com' + v['href']
	videolist.append(tmp)
	videoname.append(v['title'])

#Print search results
print('Recommended videos: ')
for i in range(len(videolist)):
	if 'googleads' not in videolist[i]: #avoid google ads
		print('\n' + videoname[i][0:60]) #title of video, truncated
		print(videolist[i]) #url of video
