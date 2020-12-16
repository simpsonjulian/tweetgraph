# from pyld import jsonld
import json
from rdflib import Graph, FOAF, RDF, Literal

g = Graph()
g.bind("foaf", FOAF)

data = open('tweets.jsonl').read()
json = [json.loads(jline) for jline in data.splitlines()]
for tweet in json:
    if tweet['entities']['user_mentions']:
        tweeter = Literal(tweet['user']['screen_name'])
        mention = Literal(tweet['entities']['user_mentions'][0]['screen_name'])
        if not mention == tweeter:
            g.add((tweeter, Literal("mentions"), mention))
            print("*")

print(g.serialize(format="turtle").decode("utf-8"))
g.serialize(format="ntriples", destination="tweets.rdf")
