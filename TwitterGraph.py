import tweepy
from keys import *
import networkx as nx
import tqdm

# TODO: Add followersGraph functionality

class TwitterGraph():
    def __init__(self, screen_name, degrees=1, api=None, followingGraph=True, pairGraph=False):
        self._setUpTweepy(api)
        self.screen_name = screen_name
        self.main_node_id = self.api.get_user(screen_name).id
        self.total_degrees = degrees
        self.pairGraph = pairGraph

        self.graph = nx.Graph()
        self.nodes_by_degree = [set([self.main_node_id])]  # nodes_added[1] is a list of all node_ids of degree 1 (nodes_added[0] is just a set containing the main node)
        self._computeGraph()

    def _setUpTweepy(self, api):
        '''
        Sets up self.api, object needed for accessing twitters api.
        '''
        if api is None:
            self.auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
            self.auth.set_access_token(twitter_access_token, twitter_access_secret)
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        else:
            self.api = api

    def _getFriendsIds(self, user_id):
        '''
        Returns a list<int> of user ids. Each id represents the twitter id of
        a friend of user_id. No duplicates.
        '''
        ids = []

        try:
            for page in tweepy.Cursor(self.api.friends_ids, id=user_id).pages():
                print('page len: {}'.format(len(page)))
                ids.extend(page)
        except tweepy.TweepError as err:
            print('TweepError: {}'.format(err))

        return ids

    def _addFriendsFromSet(self, node_ids):
        '''
        Gets all ids from set node_ids and for each n_id gets all friend_ids of x,
        and adds them to the graph, with an edge from x to each friend_id.
        '''
        print('Num nodes to process: {}'.format(len(node_ids)))

        degree_nodes = set()
        for node_id in tqdm.tqdm(node_ids):
            friends_ids = set(self._getFriendsIds(node_id))
            new_nodes_added = friends_ids - degree_nodes
            self.graph.add_nodes_from(new_nodes_added)
            self.graph.add_edges_from([(node_id, new_node) for new_node in new_nodes_added])
            degree_nodes = degree_nodes.union(new_nodes_added)
        self.nodes_by_degree.append(degree_nodes)

    def _getPairs(self, s):
        s = list(s)
        pairs = []
        for i, node in enumerate(s):
            new_pairs = [(node, n) for n in s[i+1:]]
            pairs.extend(new_pairs)
        return pairs

    def _computePairGraph(self):
        pairs = self._getPairs(self.nodes_by_degree[1])
        for p in tqdm.tqdm(pairs):
            friendship = self.api.show_friendship(source_id=p[0], target_id=p[1])
            if(friendship[0].following or friendship[0].followed_by):
                self.graph.add_edge(p[0], p[1])

    def _computeGraph(self):
        self.graph.add_node(self.main_node_id)
        if self.pairGraph: self.total_degrees = 1
        for d in range(self.total_degrees):
            self._addFriendsFromSet(self.nodes_by_degree[d])
        if self.pairGraph: self._computePairGraph()

    def getGraph(self):
        print('num nodes: {}'.format(self.graph.number_of_nodes()))
        print('num edges: {}'.format(self.graph.number_of_edges()))
        print('friends of main node: {}'.format(self.graph.degree[self.main_node_id]))
        return self.graph
