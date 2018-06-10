import praw
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords
# TODO: Use a logger for the status messages


class component(object):

    @classmethod
    def get_data(cls, config_keys, sr, *args, **kwargs):
        reddit = praw.Reddit(**config_keys)
        cls.sr = sr

        cls.raw_text = ""
        subreddit = reddit.subreddit(sr)

        print("Getting data from " + subreddit._path)
        # use low limit for debugging, high limit for more data
        top_subreddit = subreddit.top(limit=3)
        count_submission = 0
        count_comment = 0
        for submission in top_subreddit:
            cls.raw_text += " " + submission.title  # add title
            cls.raw_text += " " + submission.selftext  # add body
            count_submission += 1
            comments = submission.comments.list()
            max_comments = 1000  # put a cap on how many comments per submission
            n_comments = min(max_comments, len(comments))
            for i in range(n_comments):
                # avoid MoreComments
                if not isinstance(comments[i], praw.models.reddit.more.MoreComments):
                    cls.raw_text += " " + \
                        comments[i].body  # add comment
                    count_comment += 1
        print("Collected data from " + str(count_submission) +
              " submissions and " + str(count_comment) + " comments.")

        # Use nltk to convert string into tokens (words and
        # puncuation)
        tokens = word_tokenize(cls.raw_text)

        # Use nltk to find frequency distribution of words
        fdist = FreqDist(tokens)

        # Remove tokens with only 1 or 2 characters
        short_words = []
        for i in fdist:
            if len(i) < 3:
                short_words.append(i)
        for s in short_words:
            fdist.pop(s)

        # Remove common but useless tokens
        # get pre-defined stop words
        stop = set(stopwords.words('english'))
        additional_stop = ['https', 'http', 'n\'t', 'The',
                           'This', 'That', '...']  # add additional stop words
        for a in additional_stop:
            stop.add(a)
        for s in stop:
            try:
                fdist.pop(s)
            except:
                pass

        # Needs some work here to stem the tokens

        # Print results of nltk
        print("The 50 most commonly used words in this subreddit: ")
        return [f for f in fdist.most_common(50)]
