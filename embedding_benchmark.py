from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time


models = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2"
]


queries = [
    "osama",
    "bank cuba",
    "terror organization"
]


documents = [
    "BIN LADIN, Usama bin Muhammad bin Awad",
    "Banco Nacional de Cuba",
    "AL QA'IDA terrorist organization"
]


for model_name in models:

    print(f"\nTesting Model: {model_name}")

    model = SentenceTransformer(model_name)

    start = time.time()

    query_embeddings = model.encode(
        queries
    )

    doc_embeddings = model.encode(
        documents
    )

    latency = time.time() - start

    similarities = cosine_similarity(
        query_embeddings,
        doc_embeddings
    )

    print("\nSimilarity Matrix:")

    print(similarities)

    print(f"\nLatency: {latency:.2f} sec")