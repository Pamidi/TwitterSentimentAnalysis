import tweepy
# encoding: utf-8

class TwitterClient:
    """
    TO-DO : Model as singleton
            Have a sourceclient abstract class and make twitterclient extend               from it to       switch between sources later easily.
    """

    def __init__(self, listener):
        #Twitter API credentials
        #keys should be private

        self._consumer_key = "8zmH980xpX6J5expJcIDurA6z"
        self._consumer_secret = "GuoWM8HF5pKTkMkEWZiLUsNKX10AR63r2cHMcSHhpBDJb9Sh6R"
        self._access_token = "903884578170875904-90jIoYZpnwAou8MS8bqdU3Rfmnshwz9"
        self._access_token_secret = "JFYV2fM3IYNxWQOPTV6qYihAJyoNcNn9QuYfLYKpuXKvN"

        self._listener = listener

        #authenticate
        try:
            self.auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            self.auth.set_access_token(self._access_token, self._access_token_secret)
        except:
            raise Exception("Authentication for Twitter API failed.")


    def stream_data(self, hashtags):
        stream = tweepy.Stream(self.auth, self._listener)

        #Hashtag to stream
        stream.filter(track=hashtags)
