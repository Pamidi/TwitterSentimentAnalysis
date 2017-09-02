import tweepy
import json

class TwitterListener(tweepy.StreamListener):
    """
    ABC  to Twitter Listener
    TO-DO : use abc module from python to make it abstract method
    """
    def on_data(self, data):
        # Parsing
        decoded = json.loads(data)

        self.handle_output_logging(decoded)
        print "Writing tweets to file,CTRL+C to terminate the program"

        return True


    def on_error(self, status):
        print status

    def handle_output_logging(self, data):
        raise NotImplementedError("handle_output_logging is not implemented")


class ConsoleOutputListener(TwitterListener):
    """
    does not dump the tweet
    """

    def handle_output_logging(self, data):
        print data


class FileOutputListener(TwitterListener):

    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

    def handle_output_logging(self, data):
         #open a file to store the status objects
        file = open(self.output_file_path, 'wb')
        #write json to file
        json.dump(data,file,sort_keys = True,indent = 4)
        #show progress
