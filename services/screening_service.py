def screen(self, query):

    import uuid

    trace_id = str(uuid.uuid4())

    reasoning_trace = []

    self.logger.info(
        f"[TRACE {trace_id}] "
        f"Screening query: {query}"
    )

    timings = {}

    start_total = time.time()

    # ----------------------------
    # Graph Lookup
    # ----------------------------
    start_graph = time.time()

    graph_entity = (
        self.graph_service.graph_lookup(query)
    )

    reasoning_trace.append(
        "Performed graph lookup."
    )

    timings["graph_lookup_ms"] = (
        time.time() - start_graph
    ) * 1000

    if graph_entity:

        timings["total_ms"] = (
            time.time() - start_total
        ) * 1000

        return {
            "trace_id": trace_id,
            "decision": "MATCH",
            "entity_number": graph_entity,
            "confidence": 1.0,
            "risk_level": "HIGH",
            "reason": "Graph alias/entity lookup match.",
            "latency": timings,
            "reasoning_trace": reasoning_trace
        }

    # ----------------------------
    # Hybrid Retrieval
    # ----------------------------
    start_retrieval = time.time()

    candidates = self.retriever.hybrid_retrieve(
        query
    )

    reasoning_trace.append(
        f"Retrieved {len(candidates)} "
        f"candidates using hybrid retrieval."
    )

    timings["hybrid_retrieval_ms"] = (
        time.time() - start_retrieval
    ) * 1000

    # ----------------------------
    # Quick Similarity Check
    # ----------------------------
    query_norm = query.lower().strip()

    top_candidate = candidates[0]

    name_norm = (
        top_candidate.get("name", "")
        .lower()
        .strip()
    )

    quick_similarity = fuzz.token_sort_ratio(
        query_norm,
        name_norm
    )

    # ----------------------------
    # Fast Decision Path
    # ----------------------------
    if quick_similarity >= 92:

        decision = (
            self.decision_engine
            .deterministic_decision(
                query,
                candidates
            )
        )

        reasoning_trace.append(
            "Skipped reranker due to high "
            "initial similarity."
        )

        timings["rerank_ms"] = 0

        timings["decision_logic_ms"] = 0

        timings["total_ms"] = (
            time.time() - start_total
        ) * 1000

        decision["latency"] = timings

        decision["reasoning_trace"] = (
            reasoning_trace
        )

        decision["trace_id"] = trace_id

        workflow_trace = (
            self.workflow_orchestrator
            .run_workflow(
                query,
                candidates,
                decision
            )
        )

        decision["workflow_trace"] = (
            workflow_trace
        )

        return decision

    # ----------------------------
    # Cross-Encoder Reranking
    # ----------------------------
    start_rerank = time.time()

    reranked = self.reranker.rerank(
        query,
        candidates
    )

    reasoning_trace.append(
        "Applied cross-encoder reranking."
    )

    timings["rerank_ms"] = (
        time.time() - start_rerank
    ) * 1000

    # ----------------------------
    # Final Decision
    # ----------------------------
    start_decision = time.time()

    decision = (
        self.decision_engine
        .deterministic_decision(
            query,
            reranked
        )
    )

    reasoning_trace.append(
        f"Final decision: "
        f"{decision['decision']}."
    )

    timings["decision_logic_ms"] = (
        time.time() - start_decision
    ) * 1000

    timings["total_ms"] = (
        time.time() - start_total
    ) * 1000

    decision["latency"] = timings

    decision["reasoning_trace"] = (
        reasoning_trace
    )

    decision["trace_id"] = trace_id

    workflow_trace = (
        self.workflow_orchestrator
        .run_workflow(
            query,
            reranked,
            decision
        )
    )

    decision["workflow_trace"] = (
        workflow_trace
    )

    return decision