from rapidfuzz import fuzz
from configs.settings import (
    FUZZY_MATCH_THRESHOLD,
    PARTIAL_MATCH_THRESHOLD
)


class DecisionEngine:

    FUZZY_MATCH_THRESHOLD = FUZZY_MATCH_THRESHOLD

    def normalize(self, text):
        return text.lower().strip()
    
    def calculate_risk_score(
        self,
        candidate,
        confidence
    ):

        program = candidate.get(
            "program",
            ""
        ).lower()

        if "terror" in program:
            return "CRITICAL"

        if confidence >= 0.95:
            return "HIGH"

        if confidence >= 0.85:
            return "MEDIUM"

        return "LOW"


    def requires_human_review(
        self,
        confidence,
        risk_level
    ):

        if risk_level == "CRITICAL":
            return True

        if confidence < 0.90:
            return True

        return False

    def deterministic_decision(self, query, candidates):

        query_norm = self.normalize(query)

        for candidate in candidates:

            name = candidate.get("name", "")
            aliases = candidate.get("aliases", [])
            ids = candidate.get("ids", [])

            name_norm = self.normalize(name)

            # Exact match
            if query_norm == name_norm:
                return {
                    "decision": "MATCH",
                    "risk_level": self.calculate_risk_score(
                        candidate,
                        confidence=1.0
                    ),
                    "entity_number": candidate["ent_num"],
                    "matched_name": name,
                    "confidence": 1.0,
                    "reason": "Exact match with primary name."
                }

            # Alias match
            for alias in aliases:

                if query_norm == self.normalize(alias):

                    return {
                        "decision": "MATCH",
                        "risk_level": self.calculate_risk_score(
                            candidate,
                            confidence=1.0
                        ),
                        "entity_number": candidate["ent_num"],
                        "matched_name": name,
                        "confidence": 1.0,
                        "reason": f"Exact match with alias '{alias}'."
                    }

            # ID match
            for identifier in ids:

                if query_norm == self.normalize(identifier):

                    return {
                        "decision": "MATCH",
                        "risk_level": self.calculate_risk_score(
                            candidate,
                            confidence=1.0
                        ),
                        "entity_number": candidate["ent_num"],
                        "matched_name": name,
                        "confidence": 1.0,
                        "reason": f"Exact match with ID '{identifier}'."
                    }

            similarity = fuzz.token_sort_ratio(
                query_norm,
                name_norm
            )

            partial_similarity = fuzz.partial_ratio(
                query_norm,
                name_norm
            )

            if partial_similarity >= PARTIAL_MATCH_THRESHOLD:

                return {
                    "decision": "MATCH",
                    "risk_level": self.calculate_risk_score(
                        candidate,
                        confidence=1.0
                    ),
                    "entity_number": candidate["ent_num"],
                    "matched_name": name,
                    "confidence": round(partial_similarity / 100, 2),
                    "reason": f"High partial similarity ({partial_similarity})."
                }

            if similarity >= self.FUZZY_MATCH_THRESHOLD:

                return {
                    "decision": "MATCH",
                    "risk_level": self.calculate_risk_score(
                        candidate,
                        confidence=1.0
                    ),
                    "entity_number": candidate["ent_num"],
                    "matched_name": name,
                    "confidence": round(similarity / 100, 2),
                    "reason": f"High fuzzy similarity ({similarity})."
                }

        return {
            "decision": "NO_MATCH",
            "entity_number": None,
            "matched_name": None,
            "confidence": 0.0,
            "risk_level": "NONE",
            "reason": "No sufficient similarity found."
        }