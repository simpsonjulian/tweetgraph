# from pyld import jsonld
import json

# from rdflib import Graph, FOAF, RDF, Li?teral
from graphqlclient import GraphQLClient

client = GraphQLClient('https://kindly-death.us-west-2.aws.cloud.dgraph.io/graphql')

data = open('tweets.jsonl').read()
json_data = [json.loads(jline) for jline in data.splitlines()]


def upload_to_slash(query):
    response = json.loads(client.execute(query))
    print(repr(response))
    try:
        if response['data']:
            print("Uploaded")
        else:
            print("Error: {}".format(response))
    except KeyError:
        print(query)

    return response


def tweet_fragment(user, tweet):
    return '''
     addTweet(input: {{ content: {}, user: {{ handle: "{}" }} }}) {{
        tweet {{
          content
        }}
      }}
    '''.format(json.dumps(tweet['content']).replace('"', '\\"'), user['handle'])


def get_query(user, tweets):
    query = '''
    mutation addTweets {{
      addUser(input: {{handle: "{}", screen_name: "{}" }}) {{
        user {{
          handle
        }}
      }}
  '''.format(user['handle'], user['screen_name'])

    for tweet in tweets:
        query += tweet_fragment(user, tweet)
    query += '}'
    return query


def gather_tweets_by_user():
    for tweet in json_data:

        handle = tweet['user']['screen_name']
        screen_name = tweet['user']['name']
        content_ = tweet['full_text']
        tweet_id = tweet['id']

        user = {"handle": handle, "screen_name": screen_name}

        users[screen_name] = user

        tweet = {"id": tweet_id, "content": content_}

        user_tweets = [tweet]

        if screen_name in data:
            tweets = data[screen_name]
            tweets += user_tweets
            data[screen_name] = tweets
        else:
            data[screen_name] = user_tweets


data = {}
users = {}

gather_tweets_by_user()

for handle in data:
    print("=====")
    upload_to_slash(get_query(users[handle], data[handle]))
