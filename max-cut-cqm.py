import networkx as nx
import dimod

from dimod import ConstrainedQuadraticModel
from dimod import Binary

class graph:
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict
# Get the keys of the dictionary
    def getNodes(self):
        return list(self.gdict.keys())
# Find the distinct list of edges
    def getEdges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if (nxtvrtx, vrtx) not in edgename:
                    edgename.append((vrtx, nxtvrtx))
        return edgename


# Create the dictionary with graph elements
graph_elements = { 
   1 : [2, 3],
   2 : [1, 4],
   3 : [1, 4, 5],
   4 : [2, 3, 6],
   5 : [3, 6],
   6 : [4, 5]
}
g = graph(graph_elements)
print(g.getNodes())
print(g.getEdges())

# x[i] = 0 if node[i] is in Set0
# #[i] = 1 otherwise
x = {n: Binary(n) for n in g.getNodes()}

cqm = ConstrainedQuadraticModel()

cqm.set_objective(-sum(x[i] + x[j] - 2 * x[i] * x[j] for (i,j) in g.getEdges()))

num_nodes = len(g.getNodes())
cqm.add_constraint(sum(x[i] for i in g.getNodes()) - (num_nodes / 2) == 1, label=f'subest_equal_size')
bqm, invert = dimod.cqm_to_bqm(cqm)

from dwave.system import DWaveSampler,AutoEmbeddingComposite
sampler = DWaveSampler(DWAVE_API_TOKEN="DEV-75e04bc20be5cf5bc8a7d7924d08952738e2cefe")
embedding_sampler = AutoEmbeddingComposite(sampler)
sampleset = embedding_sampler.sample(bqm,num_reads = 100)
for smpl, energy in sampleset.data(['sample','energy']):
    print(smpl, energy)


print("SOLVER DONE") 

