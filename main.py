# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from TweetDownloader import TweetDownloader

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    downloader = TweetDownloader(credentials='credentials/twitter_keys.yaml')

    tweets, places, authors = downloader.get_tweets('Marcelo',
                                                             lang='en',
                                                             place='US',
                                                             max_tweets=10,
                                                             include_replies=False,
                                                             start_time='07/17/2021',
                                                             end_time='07/21/2021')


