# encoding: utf-8

from listener import ConsoleOutputListener
from client import TwitterClient
from match import Team, Match
from cluster_engine import ClusteringEngine

def main():

    t1 = Team("IND")
    t2 = Team("SL")

    match = Match(t1, t2)
    match_hashtag = match.get_match_details()
    #create the engine
    ce = ClusteringEngine(match)

    #first create the listener
    listener = ConsoleOutputListener(ce)
    #create twitter client
    client = TwitterClient(listener)

    #client.get_old_tweets(hashtags)
    #client.stream_data(hashtags)
    #client.get_tweets_by_user('@tweetcricscore')
    client.get_all_tweets(match_hashtag)


if __name__ == "__main__":
    main()
