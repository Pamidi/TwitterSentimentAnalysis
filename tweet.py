class Tweet:
    """
    Model a tweet for our system
    """
    def __init__(self, text, ts):
        self.text = text
        self.ts = ts

    def __cmp__(self,other):
        if self.ts < other.ts:
            return -1
        elif self.ts > other.ts:
            return 1
        else:return 0
