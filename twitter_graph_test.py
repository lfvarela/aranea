from TwitterGraph import TwitterGraph
import pickle

TG = TwitterGraph('LuisferVarela', degrees=1, pairGraph=False)
graph = TG.getGraph()

with open('graph.pickle', 'wb') as f:
    pickle.dump(graph, f)
