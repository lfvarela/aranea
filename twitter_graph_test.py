from TwitterGraph import TwitterGraph
import pickle

TG = TwitterGraph('LuisferVarela', degrees=2, pairGraph=True)

graph = TG.getGraph()
pickle.dump(graph, 'graph.pickle')
