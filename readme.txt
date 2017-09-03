SUMMARY

Components
  TwitterClient
  ClusteringEngine

  Event
  EventHierarchy

  Listener components
  Match
  Team
  Tweet

How to use this code??
  1. refer main.py to see the system workflow. (the event tree is pickled every 1 sec for now)
  2. refer dump_twitter_classified_data.py to read the pickled tree object to get the sorted event list
     and print them.(make sure to change the pickled file path)

Notes:
  System design:
    Events are modelled as a hierarchy(with certain static nodes and certain dynamic nodes).
    eg: Level 1 represents the match itself
        level 2 can be toss event, boundary, player_specific, wicket etc
        level 3 can be four event, six event etc.
        level 4 can be 1st four event, 2nd four event etc.

    Advantage of such a model is that , all the tweets related to wicket are under one handle. and so on...
    At any point of time, we can work with the tree structure to arrive at more meaningful data
    For the sake of this exercise, we are not computing the median timestamp for nodes other than leaf nodes(we
    can of course compute it any time in the system)

    Ideally, each match should have a tree for itself, (as certain matches might involve special handling
    eg: Sachins' retirement)

    After loading the static nodes and the edges from database, we have to aggregate the valid words across all nodes

    Now TwitterClient interacts with Twitter to stream the data. For testing, I tried using the timeline tweets of a
    livecommentary twitter bot.

    Each tweet is run over the clustering engine , which classifies it . Here we can use a trained data model to
    improve the accuracy. However, I have went with a naive word/simple checks based classification to arrive
    at the cluster
    Remember that, each tweet can flow through multiple paths in the hierarchy.
    eg: Sachins' wicket can flow through the node for Sachin as well as the node for wicket

    Algorithms used
    1. For finding the median of a streaming set of data, sorting is a not a viable option, as memory will be a
    constrant. I have used the technique of using a max_heap and min_heap to find the median in log(n) time_
    2. Dynamic node creation:
        To cluster tweets of an event together(challenging for dynamic nodes like ith wicket), I have used
        a threshold width check with respect to the timestamp of the node to determine whether to create a
        new dynamic node or add the tweet to the existing cluster.
        Challenge here is that the tweets are not necessarily arriving at the sorted timestamp. Hence, you
        need to dynamically rearrange the event nodes(and name them accordingly) to maintain integrity.
        This will however scale, since we can assume a max. tweet delay of 5 minutes and since you are starting
        your check from right side of the children list.

    Time complexity of the system:
      Time for processing a tweet will be
          log(n) + number_of_nodes_in_match_tree(max->600 considering one event per ball ,and event Event flows through every node)

    Output format:
      I will be giving a pickled dump of the sorted list of Event objects.  You will have handle to the following attributes
      in each element of the list.
          title                      #name of the event
          keywords                   #keywords applicable to this node
          children                   #children events(which will be empty for leaf events)
          median_timestamp           #median timestamp of tweets in this cluster
          #liast of tweets for this cluster
          tweets_for_event           #list of tweets for this cluster

  Scope for improvement:
    1.feed a set of training data to improve accuracy of the Model
    2.Use Redis cache to store the tree object of each match in DB.(update this structure after every few
    tweet processing)
    3.Store the match specific event hierarchy strucute in database for better maintanence
    4.Create Interfaces for CacheClient, TwitterClient etc.
    5.Use singleton pattern wherever required.
    6.Better documentation
    7.Have a package structure to organize the code.(did not get time to do this!)
