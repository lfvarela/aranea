from TwitterGraph import TwitterGraph
import pickle

TG = TwitterGraph('LuisferVarela', degrees=2, pairGraph=True)
graph = TG.getGraph()

with open('filename.pickle', 'wb') as f:
    pickle.dump(graph, f)
