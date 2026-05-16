import pickle
from configs.settings import KNOWLEDGE_GRAPH_PATH


class GraphService:

    def __init__(self):
        with open("KNOWLEDGE_GRAPH_PATH", "rb") as f:
            self.graph = pickle.load(f)

    def graph_lookup(self, query):

        query_clean = query.strip()

        if query_clean in self.graph.nodes:

            node_type = self.graph.nodes[query_clean].get("type")

            if node_type in ["alias", "id"]:

                neighbors = list(self.graph.neighbors(query_clean))

                for n in neighbors:

                    if self.graph.nodes[n].get("type") == "entity":
                        return n

            if node_type == "entity":
                return query_clean

        return None