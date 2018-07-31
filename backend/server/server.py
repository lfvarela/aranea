# IMPORTANT DISCLAIMER
# As is, this backend will not handle multiple concurrent requests. It is just meant for visualization running in
# localhost.

import json
import os
import sys
import tweepy
from .keys import *
from networkx.readwrite import json_graph
from .TwitterGraph import TwitterGraph

from flask import Flask, request, g

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'))


def get_api():
    if not hasattr(g, 'api'):
        try:
            auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
            auth.set_access_token(twitter_access_token, twitter_access_secret)
            g.api = tweepy.API(auth)
        except:
            return None
    return g.api


@app.route('/name', methods=['GET'])
def name():
    id = request.args['id']
    api = get_api()
    if api:
        try:
            return api.get_user(id).screen_name
        except:
            return 'Bad request: user id not found', 400
    else:
        return 'Could not access Twitter API', 500


@app.route('/graph', methods=['GET'])
def graph():
    # graph_type is one of 'following' or 'followers'
    graph_type = request.args['graph_type']
    if graph_type != 'following' and graph_type != 'followers':
        return 'Bad Request: invalid graph_type', 400
    # Twitter username of the root node.
    try:
        root_node = request.args['root_node']
        degree = int(request.args['degree'])
        g.graph = TwitterGraph(root_node, degree, get_api(), graph_type == 'following')
    except:
        return 'Unexpected error: {}'.format(sys.exc_info()[0]), 400
    return json.dumps(json_graph.node_link_data(g.graph.getGraph())), 200


if __name__ == '__main__':
    app.run()
