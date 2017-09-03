#Tree structure
#1.match
#2.toss, wicket, boundary, powerplay, drinks, innings_break,
#3.four, six, ith wicket
#4. ith four, ith six
import heapq

class Event:
    """
    represents each event in the event hierarchy
    """
    #IN MILLISECONDS
    NODE_SPLIT_TIMESTAMP_THRESHOLD = 2000

    def __init__(self, title, keywords = [], children = None, is_dynamic = False):
        self.title = title
        self.keywords = keywords
        self.children = children
        self.median_timestamp = 0
        #list of tweets for this cluster
        self.tweets_for_event = []
        self.minHeap, self.maxHeap = [], []

        #to control nodes like wickets, century, six, fours etc.
        self.is_dynamic = is_dynamic

    def find_new_median(self, tweet):
        if self.median_timestamp%2==0:
            heapq.heappush(self.maxHeap, -1*tweet.ts)
            self.N+=1
            if len(self.minHeap)==0:
                return
            if -1*self.maxHeap[0]>self.minHeap[0]:
                toMin=-1*heapq.heappop(self.maxHeap)
                toMax=heapq.heappop(self.minHeap)
                heapq.heappush(self.maxHeap, -1*toMax)
                heapq.heappush(self.minHeap, toMin)
        else:
            toMin=-1*heapq.heappushpop(self.maxHeap, -1*tweet.ts)
            heapq.heappush(self.minHeap, toMin)
            self.median_timestamp+=1

    def getMedian(self):
        if self.median_timestamp%2==0:
            return (-1*self.maxHeap[0]+self.minHeap[0])/2.0
        else:
            return -1*self.maxHeap[0]

    def __repr__(self):
        print self.title

    def __str__(self):
        print self.title

class EventHierarchy:
    """
    Each match has an appropriate event hierarchy

    for special rule handling per match, extend this class
    and create a new hierarchy propogation logic, and have the match class
    contain the modified tree
    """
    def __init__(self, root):
        self.root = root

    def _propogate_tweet(nd, tokens, tweet):
        #if no tokens, return
        if not tokens:
            return

        if not nd:
            return

        #handle leaf nodes, here we need to store the tweet
        #and calculate the median of the list
        if (not nd.is_dynamic) and (not nd.children):
            #calculate the new median
            nd.median_timestamp = nd.find_new_median(tweet)

            nd.tweets_for_event.append(tweet)
            return

        if (nd.is_dynamic):
            #this means we are at a node, that might get an additional child
            #compare the median timestamp of the last child with the new tweets
            #timestamp. if it exceeds a threshold, create a new node, else
            #update the median of the last cluster group
            #if no child or tweet.tm outside threshold
            if (not nd.children) or (tweet.tm - nd.median_timestamp > Event.NODE_SPLIT_TIMESTAMP_THRESHOLD):
                #add new node
                #create new Event node
                new_node_name = nd.title + '_' + str(len(nd.children) + 1)
                cnd = Event(new_node_name, keywords = nd.keywords)
                nd.children.append(cnd)
            else:
                #calculate the new median
                nd.children[-1].median_timestamp = nd.children[-1].find_new_median(tweet)
                nd.children[-1].tweets_for_event.append(tweet)
            return

        #else for any of the child that contain they token, take the path
        for child in nd.childen:
            #if any of the token match the children take the path
            if bool(set(tokens) and set(child.keywords)):
                #take this path
                self._propogate_tweet(child, tokens, tweet)

    def propogate_tweet(self, tokens, tweet):
        """
        flow through all the paths where the tokens apply

        #certain exceptions to be explicitly handled here
        modify per requirement of the match
        """
        #handling precedence of words(just a basic model)
        tkns = []
        if  'toss' in tokens:
            tkns+= ['toss']

        if 'six' in tokens:
            tkns+= ['six']

        if 'four' in tokens:
            tkns+= ['four']

        if ('wicket' in tokens) or ('out' in tokens) or ('lbw' in tokens) or ('caught' in tokens) or ('bowled' in tokens):
            #if boundary, don't consider this as a wicket
            if ('six' not in tkns) and ('four' not in tkns):
                tkns+= ['wicket']

        if ('century' in tokens) or ('hundred' in tokens) or ('100' in tokens):
            if 'wicket' not in tkns:
                tkns+= ['']

        if ('fifty' in tokens) or ('50' in tokens) or ('half century' in tokens):
            tkns += 'fifty'

        if 'powerplay' in tokens:
            tkns+= ['powerplay']

        if 'hat-trick' in tokens:
            tkns+= ['hat-trick']

        if 'maiden' in tokens:
            tkns+= ['maiden']

        if 'drinks' in tokens:
            tkns+= ['drinks']

        if 'innings' in tokens or 'break' in tokens:
            tkns+= ['innings']

        self._propogate_tweet(self.root, tkns, tweet)

    def _aggregate_keyword_for_node(self, nd):
        if not nd:
            return []

        #if node is a leaf node, return
        if not nd.children:
            return []

        import pdb; pdb.set_trace()

        print "title:",nd.title

        #else propogate the value of its children
        agg_keywords = nd.keywords
        for child in nd.children:
            agg_keywords = agg_keywords + self._aggregate_keyword_for_node(child)

        nd.keywords = agg_keywords
        return agg_keywords

    def aggregate_keyword_for_nodes(self):
        #aggregate and set the keyword across nodes
        #simply DFS traversal and update the keywords for nodes
        self._aggregate_keyword_for_node(self.root)
