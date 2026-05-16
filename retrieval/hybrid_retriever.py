import json
from rank_bm25 import BM25Okapi
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from configs.settings import (
    EMBEDDING_MODEL,
    VECTOR_DB_DIR,
    BM25_CORPUS_PATH
)


class HybridRetriever:

    def __init__(self):


        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            persist_directory="vector_db",
            embedding_function=self.embedding_model
        )

        with open("bm25_corpus.json", "r") as f:
            data = json.load(f)

        corpus = data["corpus"]

        self.metadata = data["metadata"]

        tokenized_corpus = [
            doc.lower().split()
            for doc in corpus
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)
    
    def expand_query(self, query):

        query = query.lower()

        expansions = {
            "bank": "financial institution banking corporation",
            "company": "corporation enterprise business",
            "terror": "terrorist terrorism extremist",
            "ship": "vessel tanker cargo maritime",
        }

        expanded_terms = [query]

        for key, value in expansions.items():

            if key in query:

                expanded_terms.append(value)

        return " ".join(expanded_terms)

    def hybrid_retrieve(self,query,k=5, entity_type=None):

        vector_docs = self.vector_store.similarity_search(expanded_query, k=k)

        vector_candidates = []

        for rank, doc in enumerate(vector_docs):

            metadata = doc.metadata.copy()

            metadata["vector_score"] = 1 / (rank + 1)

            vector_candidates.append(metadata)

        expanded_query = self.expand_query(query)

        tokenized_query = expanded_query.split()

        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        bm25_candidates = []

        for rank, idx in enumerate(top_indices):

            metadata = self.metadata[idx].copy()

            metadata["bm25_score"] = scores[idx]

            bm25_candidates.append(metadata)

        combined = vector_candidates + bm25_candidates

        for candidate in combined:

            vector_score = candidate.get("vector_score", 0)

            bm25_score = candidate.get("bm25_score", 0)

            candidate["hybrid_score"] = (
                0.7 * vector_score
                +
                0.3 * bm25_score
            )
        unique_candidates = {}

        for candidate in combined:

            ent_num = candidate["ent_num"]

            if ent_num not in unique_candidates:
                unique_candidates[ent_num] = candidate
        
        if entity_type:

            final_candidates = [

                c for c in final_candidates

                if entity_type.lower()
                in c.get("program", "").lower()
            ]

        final_candidates.sort(
            key=lambda x: x.get("hybrid_score", 0),
            reverse=True
        )

        return final_candidates