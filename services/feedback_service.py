import json
import os


class FeedbackService:

    def __init__(self):

        self.feedback_file = "feedback_log.json"

        if not os.path.exists(
            self.feedback_file
        ):

            with open(
                self.feedback_file,
                "w"
            ) as f:

                json.dump([], f)

    def log_feedback(
        self,
        query,
        decision,
        reviewer_feedback
    ):

        with open(
            self.feedback_file,
            "r"
        ) as f:

            data = json.load(f)

        data.append({

            "query": query,

            "decision": decision,

            "reviewer_feedback": reviewer_feedback
        })

        with open(
            self.feedback_file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )
    
    def identify_learning_candidates(
        self,
        decisions
    ):

        learning_candidates = []

        for decision in decisions:

            confidence = decision.get(
                "confidence",
                1.0
            )

            requires_review = decision.get(
                "requires_review",
                False
            )

            if confidence < 0.90 or requires_review:

                learning_candidates.append(
                    decision
                )

            return learning_candidates