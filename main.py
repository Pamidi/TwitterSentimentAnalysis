# encoding: utf-8

from listener import ConsoleOutputListener
from client import TwitterClient

def main():
    #first create the listener
    listener = ConsoleOutputListener()

    #create twitter client
    client = TwitterClient(listener)
    hashtags = ['#WARKSvsNOTTS']

    client.get_old_tweets(hashtags)
    #client.stream_data(hashtags)

if __name__ == "__main__":
    main()
