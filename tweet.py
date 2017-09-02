class Tweet:
    """
    Model a tweet for our system
    """
    def __init__(self, text, tm):
        self.text = text
        self.tm = tm

    def __cmp__(self,other):
        if self.tm < other.tm:
            return -1
        elif self.tm > other.tm:
            return 1
        else:return 0
