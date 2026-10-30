"""
Diagnostics and Decision Tracing module for RuleRoute Recommendation Engine.
Captures real-time deterministic rule evaluations into structured audit steps.
"""

from typing import List, Dict, Any


class DecisionTrace:
    """Collects chronological decision-making steps during rule execution."""

    def __init__(self):
        self._steps: List[Dict[str, Any]] = []

    def record(self, stage: str, action: str, result: str, status: str = "success") -> None:
        """
        Record an execution trace event.

        Args:
            stage: Stage name (e.g., 'Validation', 'Domain Routing', 'Language Evaluation', 'Project Matching')
            action: Specific condition tested or decision evaluated
            result: Outcome of the evaluation
            status: Status identifier ('success', 'info', 'warning', 'error')
        """
        step_number = len(self._steps) + 1
        self._steps.append({
            'step': step_number,
            'stage': stage,
            'action': action,
            'result': result,
            'status': status,
        })

    def to_list(self) -> List[Dict[str, Any]]:
        """Return the collected decision trace as a list of dictionaries."""
        return list(self._steps)

    def __len__(self) -> int:
        return len(self._steps)

    def __bool__(self) -> bool:
        """Always evaluate to True as a valid trace collector instance."""
        return True
