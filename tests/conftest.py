# tests/conftest.py

import pytest


@pytest.fixture
def sample_paper():
    return {
        "title": "Test Paper on Agent Role Boundaries",
        "authors": [
            "Alice Kim",
            "Bob Lee",
        ],
        "abstract": (
            "This paper studies role boundaries, "
            "authority constraints, and behavioral control "
            "in autonomous AI agents."
        ),
        "published": "2026-01-01T00:00:00+00:00",
        "url": "https://example.com/paper",
        "pdf_url": "https://example.com/paper.pdf",
    }


@pytest.fixture
def duplicate_papers():
    return [
        {
            "title": "Agent Role Boundaries",
            "relevance_score": 3,
        },
        {
            "title": "agent role boundaries",
            "relevance_score": 5,
        },
        {
            "title": "Autonomous Agent Governance",
            "relevance_score": 4,
        },
    ]


@pytest.fixture
def valid_analysis():
    return {
        "research_problem": (
            "Autonomous agents may act outside "
            "their intended operational boundaries."
        ),
        "research_gap": (
            "Existing work does not sufficiently study "
            "explicit job-based authority boundaries."
        ),
        "research_objective": (
            "Evaluate whether explicit role and authority "
            "constraints improve agent control."
        ),
        "method": (
            "Agents with different authority constraints "
            "are compared experimentally."
        ),
        "dataset": (
            "Synthetic agent interaction scenarios."
        ),
        "experiment": (
            "The experiment compares constrained and "
            "unconstrained agent configurations."
        ),
        "results": (
            "Explicit constraints reduced unauthorized actions."
        ),
        "contribution": (
            "The paper proposes a role-bound agent "
            "control architecture."
        ),
        "limitations": (
            "Evaluation is limited to synthetic scenarios."
        ),
        "relevance_to_current_rq": (
            "The paper directly addresses whether explicit "
            "agent boundaries can reduce unintended behavior."
        ),
    }