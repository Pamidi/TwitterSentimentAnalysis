import string

class ClusteringEngine:
    def __init__(self, match):
        self.match = match
        self.match_event_tree = match.get_event_hierarchy_tree()

    def train_data(self):
        """
        TO-DO : train the engine with random tweets
                to improve the accuracy of the system
                Implementing a simple rule based engine for now
        """
        pass

    def cleanup_data(self, text):
        """
        TO-DO: Use re to remove punctuations ,white spaces,
        edit distance enhancement etc.
        """
        return text

    def process(self, tweet):
        """
        #process the tweet with text and tm
        """

        #identify the applicable event keywords for this text
        text = self.cleanup_data(tweet.text)
        tokens = [str(t.lower()).translate(None, string.punctuation) for t in tweet.text.split()]
        import ipdb; ipdb.set_trace()
        applicable_tokens = []
        for phrase in self.match_event_tree.root.keywords:
            if phrase in " ".join(tokens):
                applicable_tokens.append(phrase)

        self.match_event_tree.propogate_tweet(applicable_tokens, tweet)
