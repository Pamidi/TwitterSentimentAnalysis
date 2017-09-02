#Tree structure
#1.match
#2.toss, wicket, boundary, powerplay, drinks, innings_break,
#3.four, six, ith wicket
#4. ith four, ith six

class Event:
    """
    represents each event in the event hierarchy
    """
    def __init__(self, title, keywords = None, children = []):
        self.title = title
        self.keywords = keywords
        self.children = children
        self.median_timestamp = None
        self.tweets_for_event = []

    def __repr__(self):
        print self.title

    def __str__(self):
        print self.title

class EventHierarchy:
    def __init__(self, root):
        self.root = root

    def _aggregate_keyword_for_node(self, nd):
        if not nd:
            return []

        #if node is a leaf node, return
        if not nd.children:
            return []

        #else propogate the value of its children
        agg_keywords = root.keywords
        for child in nd.children:
            agg_keywords = agg_keywords + self._aggregate_keyword_for_node(child)

        nd.keywords = agg_keywords
        return agg_keywords

    def aggregate_keyword_for_nodes(self):
        #aggregate and set the keyword across nodes
        #simply DFS traversal and update the keywords for nodes
        self._aggregate_keyword_for_node(self.root)
