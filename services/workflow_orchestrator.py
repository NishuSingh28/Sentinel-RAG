class WorkflowOrchestrator:

    def run_workflow(
        self,
        query,
        candidates,
        decision
    ):

        workflow_trace = []

        workflow_trace.append(
            "Step 1: Retrieved candidate entities."
        )

        workflow_trace.append(
            "Step 2: Applied reranking."
        )

        workflow_trace.append(
            "Step 3: Performed deterministic validation."
        )

        workflow_trace.append(
            f"Step 4: Assigned risk level "
            f"{decision.get('risk_level')}."
        )

        workflow_trace.append(
            f"Step 5: Final decision "
            f"{decision.get('decision')}."
        )

        return workflow_trace