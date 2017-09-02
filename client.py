import tweepy
import json
# encoding: utf-8

class TwitterClient:
    """
    TO-DO : Model as singleton
            Have a sourceclient abstract class and make twitterclient extend               from it to       switch between sources later easily.
    """

    def __init__(self, listener):
        #Twitter API credentials
        #keys should be private

        self._consumer_key = "kqK6cNTbjXbB1dVV132cKQ4OL"
        self._consumer_secret = "W0hK9dH2ITU1lqT9J80s3n0QR2yWZdsMXzAIwUkZDHtE18OVEh"
        self._access_token = "903888577028689920-Yqpx4QaZqUpNZr5WvP1gd9umVdgMJbn"
        self._access_token_secret = "ch3SSIN8jOFNqGlx1JGQXnRuJkM88SP8xo1n7FARjZaft"

        self._listener = listener

        #authenticate
        try:
            self.auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            self.auth.set_access_token(self._access_token, self._access_token_secret)
        except:
            raise Exception("Authentication for Twitter API failed.")

    def stream_data(self, hashtags):
        print "streaming data:"
        stream = tweepy.Stream(self.auth, self._listener)

        #Hashtag to stream
        stream.filter(track=hashtags)

    def get_old_tweets(self, hashtags):
        api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        tweets =tweepy.Cursor(api.search,q=hashtags[0]).items()

        while True:
            tweet = tweets.next()
            self._listener.on_data(dict(tweet._json))

    def get_all_tweets(self,screen_name):
        self.auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        self.auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(self.auth)  

        new_tweets = api.user_timeline(screen_name = screen_name,count=200)      

        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            
            #save most recent tweets
            alltweets.extend(new_tweets)
            
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print "...%s tweets downloaded so far" % (len(alltweets))