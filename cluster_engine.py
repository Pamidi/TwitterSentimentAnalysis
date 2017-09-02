class ClusteringEngine:
    def __init__(self, match):
        self.data_client = data_client
        self.match = match
        self.match_event_tree = match.get_event_hierarchy_tree()

    def process(self, text, tm):
        """
        #process the tweet with text and tm
        """
