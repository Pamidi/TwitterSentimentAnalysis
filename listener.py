import tweepy
import json
import pdb
from datetime import datetime
import time
from tweet import Tweet
import pickle

class TwitterListener(tweepy.StreamListener):
    """
    ABC  to Twitter Listener
    TO-DO : use abc module from python to make it abstract method
    """
    def __init__(self, cluster_engine):
        self.visited = dict()
        self.cluster_engine = cluster_engine

    def on_data(self, data):
        # Parsing
        if type(data) is not dict:
            #for streaming cases
            decoded = json.loads(data)
            text =  decoded['text']
            time_ =  datetime.fromtimestamp(float(decoded['timestamp_ms'])/1000.0)
        else:
            #for fetching old tweets
            decoded = data
            text = decoded['text']
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(decoded['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            time_ = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

        if (text not in self.visited):
            self.visited[text] = True
            print "received text:",text
            print "received time:",time_
        else:
            #already visited tweet. skipping for now
            return True

        self.handle_output_logging(decoded)
        #print "Writing tweets to file,CTRL+C to terminate the program"

        #run the clustering algorithm over the tweet
        #create a tweet object
        tweet = Tweet(text, time_, decoded)
        self.cluster_engine.process(tweet)

        self.cluster_engine.match_event_tree.display_tree()

        #pickle the root of the tree to save the state of the application
        """
        TO-DO : move to a key value store for saving the tree for multiple matches
        """
        print "pickling root.."
        with open("/home/xavier/Desktop/twitter/data/root.pkl","wb") as output_file:
            pickle.dump(self.cluster_engine.match_event_tree, output_file)
        time.sleep(1)
        return True

    def on_status(self, status):
        print status.text

    def on_error(self, status):
        print status.text

    def handle_output_logging(self, data):
        raise NotImplementedError("handle_output_logging is not implemented")


class ConsoleOutputListener(TwitterListener):
    """
    does not dump the tweet
    """

    def handle_output_logging(self, data):
        #print data
        pass

class FileOutputListener(TwitterListener):

    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

    def handle_output_logging(self, data):
         #open a file to store the status objects
        file = open(self.output_file_path, 'wb')
        #write json to file
        json.dump(data,file,sort_keys = True,indent = 4)
        #show progress
