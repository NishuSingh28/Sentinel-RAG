from sentence_transformers import CrossEncoder
from configs.settings import CROSS_ENCODER_MODEL


class CrossEncoderReranker:

    def __init__(self):
        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    def rerank(self, query, candidates):

        pairs = [(query, c.get("name", "")) for c in candidates]

        scores = self.cross_encoder.predict(pairs)

        scored = []

        for candidate, score in zip(
            candidates,
            scores
        ):

            hybrid_score = candidate.get(
                "hybrid_score",
                0
            )

            final_score = (
                0.7 * score
                +
                0.3 * hybrid_score
            )

            candidate["rerank_score"] = final_score

            scored.append(
                (candidate, final_score)
            )

        scored.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return [c for c, score in scored]