class Tweet:
    """
    Model a tweet for our system
    """
    def __init__(self, text, ts, tweet_dict):
        self.text = text
        self.ts = ts
        self.tweet_dict = tweet_dict

    def __cmp__(self,other):
        if self.ts < other.ts:
            return -1
        elif self.ts > other.ts:
            return 1
        else:return 0
