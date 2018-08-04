# from Aranea root directory
# source Vpy3/bin/activate
# pip install -r requirements.txt
# python ./scripts/one_off/pickle_to_JSON.py 
#
# manually rename output file to .JSON

import pickle
import networkx as nx
import json

PICKLE = './network_data/lfv-1-1.pickle'

def main():
    pickle_file = open(PICKLE,'rb')
    graph_obj = pickle.load(pickle_file)
    graph_nl = nx.node_link_data(graph_obj)

    with open('./network_data/lfv-1-1.json', 'w') as outfile:
        json.dump(graph_nl, outfile)
    
if __name__ == '__main__':
    main()