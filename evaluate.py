import json
from retriever import (
    graph_lookup,
    hybrid_retrieve,
    deterministic_decision
)


def run_query(query):

    # Graph lookup
    graph_entity = graph_lookup(query)

    if graph_entity:

        return {
            "decision": "MATCH",
            "entity_number": graph_entity
        }

    # Hybrid retrieval
    candidates = hybrid_retrieve(query)

    result = deterministic_decision(
        query,
        candidates
    )

    return {
        "decision": result["decision"],
        "entity_number": result["entity_number"]
    }


# ----------------------------
# Precision@K
# ----------------------------
def precision_at_k(
    retrieved,
    relevant,
    k=5
):

    retrieved_k = retrieved[:k]

    relevant_count = sum(
        1
        for item in retrieved_k
        if item in relevant
    )

    return relevant_count / k


# ----------------------------
# Recall@K
# ----------------------------
def recall_at_k(
    retrieved,
    relevant,
    k=5
):

    retrieved_k = retrieved[:k]

    relevant_found = sum(
        1
        for item in relevant
        if item in retrieved_k
    )

    return relevant_found / len(relevant)


# ----------------------------
# Evaluation
# ----------------------------
def evaluate():

    with open(
        "evaluation_data_auto.json",
        "r"
    ) as f:

        test_data = json.load(f)

    total = len(test_data)

    correct = 0

    false_positive = 0

    false_negative = 0

    precision_scores = []

    recall_scores = []

    failed_cases = []

    for item in test_data:

        query = item["query"]

        true_label = item["label"]

        true_entity = item["entity_number"]

        prediction = run_query(query)

        predicted_label = prediction["decision"]

        predicted_entity = prediction["entity_number"]

        # ----------------------------
        # Retrieval Metrics
        # ----------------------------
        retrieved_entities = []

        if predicted_entity:

            retrieved_entities.append(
                str(predicted_entity)
            )

        relevant_entities = [str(true_entity)]

        precision_score = precision_at_k(
            retrieved_entities,
            relevant_entities,
            k=1
        )

        recall_score = recall_at_k(
            retrieved_entities,
            relevant_entities,
            k=1
        )

        precision_scores.append(
            precision_score
        )

        recall_scores.append(
            recall_score
        )

        # ----------------------------
        # Classification Metrics
        # ----------------------------
        if predicted_label == true_label:

            if predicted_label == "MATCH":

                if str(predicted_entity) == str(true_entity):

                    correct += 1

                else:

                    false_positive += 1

                    failed_cases.append({
                        "query": query,
                        "expected": true_entity,
                        "predicted": predicted_entity
                    })

            else:

                correct += 1

        else:

            if predicted_label == "MATCH":

                false_positive += 1

            else:

                false_negative += 1

            failed_cases.append({
                "query": query,
                "expected_label": true_label,
                "predicted_label": predicted_label
            })

    # ----------------------------
    # Final Metrics
    # ----------------------------
    accuracy = correct / total

    precision = (
        correct / (correct + false_positive)
        if (correct + false_positive) > 0
        else 0
    )

    recall = (
        correct / (correct + false_negative)
        if (correct + false_negative) > 0
        else 0
    )

    avg_precision_at_1 = (
        sum(precision_scores)
        / len(precision_scores)
    )

    avg_recall_at_1 = (
        sum(recall_scores)
        / len(recall_scores)
    )

    # ----------------------------
    # Report
    # ----------------------------
    print("\n=== Evaluation Report ===")

    print(f"Total Samples: {total}")

    print(f"Accuracy: {accuracy:.2f}")

    print(f"Precision: {precision:.2f}")

    print(f"Recall: {recall:.2f}")

    print(f"Precision@1: {avg_precision_at_1:.2f}")

    print(f"Recall@1: {avg_recall_at_1:.2f}")

    print(f"False Positives: {false_positive}")

    print(f"False Negatives: {false_negative}")

    # ----------------------------
    # Failure Analysis
    # ----------------------------
    print("\n=== Failure Analysis ===")

    for case in failed_cases[:10]:

        print(case)


if __name__ == "__main__":

    evaluate()