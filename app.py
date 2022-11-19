from flask import Flask, request, render_template, redirect, url_for
import json
import TwitterAccess
from sources import *

# template_folder is relative to where the main flask run .py file is (/api/app.py)
app = Flask(__name__)  # , template_folder='../templates', static_url_path="/")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query_input']
    print(f"USER QUERY: {user_query}")

    # Hold the selected news sources to explicitly search if user selected any.
    list_of_news_accounts_to_search = []

    # Names of check box HTML boxes
    news_source_names = ["ny_times", "fox_news", "Guardian", "MSNBC", "Politico", "ABC_News", "CBS_News", "Vice_News"]

    # Go through each HTML checkbox and append the ones that have been selected, if any, to the
    #  list_of_news_accounts_to_search list.
    for news_source_name in news_source_names:
        if request.form.get(news_source_name) is not None:
            list_of_news_accounts_to_search.append(news_source_name)

    if list_of_news_accounts_to_search:
        print(f"Only searching the following News source Twitter account(s): {list_of_news_accounts_to_search}")
        tweets_to_display = news_tweets(user_query=user_query, news_sources=list_of_news_accounts_to_search)
    else:
        print(f"No explicit news source(s) selected, so searching all of twitter...")
        tweets_to_display = tweets(user_query=user_query)

    return render_template("results.html", tweet_list=tweets_to_display, query=user_query)


@app.route('/upvote')
def upvote_post():
    # TODO: Enter logic to take the tweet and put it in user DB
    print("here")
    return "nothing"


@app.route('/tweets', methods=['GET', 'POST'])
def tweets(user_query):
    api = TwitterAccess.TwitterClient()
    if request.method == 'POST':
        '''Getting the query results from Twitter and returning it to the api caller'''
        tweets = api.get_tweets(query=user_query, count=50)
        return tweets


@app.route('/tweets/news', methods=['GET', 'POST'])
def news_tweets(user_query=None, news_sources=[]):
    if user_query:
        query = user_query
    else:
        query = request.form['query_input']

    api = TwitterAccess.TwitterClient()
    if request.method == 'POST':
        '''Getting the query results from Twitter and returning it to the api caller'''
        tweets = api.query_twitter_users(query=query, count=50, user_list=news_sources)
        return tweets


@app.route('/user/<username>')
def show_user_profile(username=None):
    # username=None ensures the code run even when no name is provided
    return render_template('user-profile.html', username=username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return str(post_id)


def clean_tweets(tweet_list):
    """
    Takes in a list of returned tweets from the Twitter api, cleans, adn returns them.
    :param tweet_list: list of dictionary tweets
    :return: list of clean tweets
    """


def login_user():
    return "You are logged in"


def serve_login_page():
    return "Please log in"
