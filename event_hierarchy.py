#Tree structure
#1.match
#2.toss, wicket, boundary, powerplay, drinks, innings_break,
#3.four, six, ith wicket
#4. ith four, ith six
import heapq
import time

class Event:
    """
    represents each event in the event hierarchy
    """
    #IN MILLISECONDS
    NODE_SPLIT_TIMESTAMP_THRESHOLD = 2000 * 70

    def __init__(self, title, keywords = None, children = None, is_dynamic = False):
        self.title = title
        self.keywords = keywords if keywords else []
        self.children = children if children else []
        self.median_timestamp = 0
        #list of tweets for this cluster
        self.tweets_for_event = []
        self.minHeap, self.maxHeap = [], []

        #to control nodes like wickets, century, six, fours etc.
        self.is_dynamic = is_dynamic

    def adjust_median_util_heaps(self, tweet):
        tweet_ts = time.mktime(tweet.ts.timetuple())
        n = 0 if not self.tweets_for_event else len(self.tweets_for_event)

        self.tweets_for_event.append(tweet)

        if n%2==0:
            heapq.heappush(self.maxHeap, -1*tweet_ts)
            n+=1
            if len(self.minHeap)==0:
                return
            if -1*self.maxHeap[0]>self.minHeap[0]:
                toMin=-1*heapq.heappop(self.maxHeap)
                toMax=heapq.heappop(self.minHeap)
                heapq.heappush(self.maxHeap, -1*toMax)
                heapq.heappush(self.minHeap, toMin)
        else:
            toMin=-1*heapq.heappushpop(self.maxHeap, -1*tweet_ts)
            heapq.heappush(self.minHeap, toMin)
            n+=1

    def getMedian(self):
        n = 0 if not self.tweets_for_event else len(self.tweets_for_event)

        if n%2==0:
            return (-1*self.maxHeap[0]+self.minHeap[0])/2.0
        else:
            return -1*self.maxHeap[0]

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

class EventHierarchy:
    """
    Each match has an appropriate event hierarchy

    for special rule handling per match, extend this class
    and create a new hierarchy propogation logic, and have the match class
    contain the modified tree
    """
    def __init__(self, root):
        self.root = root


    def _display_tree(self, nd):
        if not nd:
            return

        #print this node if it has tweets
        if nd.tweets_for_event:
            print "NODE:", nd.title
            for twt in nd.tweets_for_event:
                print "tweet text:",twt.text
                print "tweet time:",twt.ts
            print "NODE median timestamp:", nd.median_timestamp
            print ""

        #if this node has no children, return
        if not nd.children:
            return

        for child in nd.children:
            self._display_tree(child)

    def display_tree(self):
        self._display_tree(self.root)

    def _propogate_tweet(self, nd, tokens, tweet):
        #if no tokens, return
        if not tokens:
            return

        if not nd:
            return

        #handle leaf nodes, here we need to store the tweet
        #and calculate the median of the list
        if (not nd.is_dynamic) and (not nd.children):
            #calculate the new median
            nd.adjust_median_util_heaps(tweet)
            nd.median_timestamp = nd.getMedian()

            return

        if (nd.is_dynamic):
            #this means we are at a node, that might get an additional child
            #compare the median timestamp of the last child with the new tweets
            #timestamp. if it exceeds a threshold, create a new node, else
            #update the median of the last cluster group
            #if no child or tweet.tm outside threshold
            tweet_ts =  time.mktime(tweet.ts.timetuple())

            if (not nd.children) or (tweet_ts - nd.median_timestamp > Event.NODE_SPLIT_TIMESTAMP_THRESHOLD):
                #add new node
                #create new Event node
                new_node_name = nd.title + '_' + str(len(nd.children) + 1)
                cnd = Event(new_node_name, keywords = nd.keywords)
                cnd.adjust_median_util_heaps(tweet)
                cnd.median_timestamp = cnd.getMedian()
                nd.children.append(cnd)

            elif tweet_ts - nd.median_timestamp < Event.NODE_SPLIT_TIMESTAMP_THRESHOLD:
                #find the first bucket which place
                cur = len(nd.children)-1
                while cur>=0:
                    #check if this cur accomodates the tweet
                    if abs(tweet_ts - nd.children[cur].median_timestamp) <= Event.NODE_SPLIT_TIMESTAMP_THRESHOLD:
                        break
                    cur = cur - 1

                #cur is either -1 or a number
                if cur == -1:
                    #create  a new node and update the title for each event nodes
                    new_node_name = nd.title + '_' + str(1)
                    cnd = Event(new_node_name, keywords = nd.keywords)
                    cnd.adjust_median_util_heaps(tweet)
                    cnd.median_timestamp = cnd.getMedian()
                    nd.children = [cnd] + nd.children

                    #update the name for all nodes from index 1
                    for index, value in enumerate(nd.children[1:]):
                        nd.children[index+1].title = nd.title + '_' + str(index + 1)

                else:
                    #add it to the existing node

                    #calculate the new median
                    nd.children[cur].adjust_median_util_heaps(tweet)
                    nd.children[cur].median_timestamp = nd.children[cur].getMedian()

            else:
                #calculate the new median
                nd.children[-1].adjust_median_util_heaps(tweet)
                nd.children[-1].median_timestamp = nd.children[-1].getMedian()
            return

        #else for any of the child that contain they token, take the path
        for child in nd.children:
            #if any of the token match the children take the path
            if bool(set(tokens) & set(child.keywords)):
                #take this path
                self._propogate_tweet(child, tokens, tweet)

    def propogate_tweet(self, tokens, tweet):
        """
        flow through all the paths where the tokens apply

        #certain exceptions to be explicitly handled here
        modify per requirement of the match
        """
        #handling precedence of words(just a basic model)
        #wicket and boundary means boundary
        if ('wicket' in tokens) or ('out' in tokens) or ('lbw' in tokens) or ('caught' in tokens) or ('bowled' in tokens):
            #if boundary, don't consider this as a wicket
            if ('six' in tokens) or ('four' in tokens):
                try:
                    for word in ['wicket','out','lbw','caught','bowled']:
                        tokens.remove(word)
                except:
                    pass

        #century and come with wicket
        if ('century' in tokens) or ('hundred' in tokens):
            if 'wicket' in tkns:
                tokens.remove('wicket')

        #century and come with wicket
        if ('fifty' in tokens) or ('half century' in tokens):
            if 'wicket' in tokens:
                tokens.remove('wicket')

        self._propogate_tweet(self.root, tokens, tweet)

    def _aggregate_keyword_for_node(self, nd):
        if not nd:
            return []

        #if node is a leaf node, return
        if not nd.children:
            return nd.keywords

        #else propogate the value of its children
        agg_keywords = nd.keywords
        for child in nd.children:
            agg_keywords = agg_keywords + self._aggregate_keyword_for_node(child)

        nd.keywords = agg_keywords
        print "title:",nd.title
        print "keywords:",nd.keywords

        return agg_keywords

    def aggregate_keyword_for_nodes(self):
        #aggregate and set the keyword across nodes
        #simply DFS traversal and update the keywords for nodes
        self._aggregate_keyword_for_node(self.root)
