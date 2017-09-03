# encoding: utf-8

def main():
    #just retrieve the pickled root of the Tree
    import pickle

    with open("/home/xavier/Desktop/root.pkl", "rb") as input_file:
        hierarchy_tree = pickle.load(input_file)

    #get the flattened leaf cluster events
    leaf_events = hierarchy_tree.collect_leaf_events()
    sorted(leaf_events)

    for event in leaf_events:
        print "event_name:",event.title
        print "median:time", event.median_timestamp
        for tweet in event.tweets_for_event:
            print "text:",tweet.text
            print "tweet_time:",tweet.ts

        print "\n"
        print "\n"

if __name__ == "__main__":
    main()
