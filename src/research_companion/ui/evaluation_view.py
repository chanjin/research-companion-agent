# src/research_companion/ui/evaluation_view.py

import streamlit as st


def render_check(
    check,
) -> None:

    icon = (
        "✅"
        if check.passed
        else "❌"
    )

    with st.expander(
        (
            f"{icon} "
            f"{check.category.upper()} — "
            f"{check.name}"
        )
    ):

        st.markdown(
            f"**Rule ID:** {check.rule_id}"
        )

        st.markdown(
            f"**Passed:** {check.passed}"
        )

        st.markdown(
            f"**Score:** {check.score:.2f}"
        )

        st.markdown(
            f"**Severity:** {check.severity}"
        )

        st.markdown(
            "**Result**"
        )

        st.write(
            check.message
        )

        if check.evidence:

            st.markdown(
                "**Evidence**"
            )

            for item in check.evidence:

                st.write(
                    f"- {item}"
                )


def render_evaluation_report(
    report,
) -> None:

    st.markdown(
        "## Specification Evaluation"
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "Overall",
        (
            "PASS"
            if report.overall_pass
            else "FAIL"
        ),
    )

    col2.metric(
        "Score",
        f"{report.overall_score:.2f}",
    )

    col3.metric(
        "Checks",
        len(report.checks),
    )

    if report.violations:

        st.error(
            (
                f"{len(report.violations)} "
                "specification violation(s) detected."
            )
        )

        for violation in (
            report.violations
        ):

            st.write(
                f"- {violation}"
            )

    elif report.warnings:

        st.warning(
            (
                f"{len(report.warnings)} "
                "warning(s) detected."
            )
        )

    else:

        st.success(
            "All specification checks passed."
        )

    if report.warnings:

        st.markdown(
            "### Warnings"
        )

        for warning in report.warnings:

            st.write(
                f"- {warning}"
            )

    st.markdown(
        "### Detailed Checks"
    )

    for check in report.checks:

        render_check(
            check
        )


def render_evaluation_view(
    observability,
    evaluation_service,
) -> None:

    st.subheader(
        "Specification-based Agent Evaluation"
    )

    st.caption(
        (
            "Evaluate an Agent Run against "
            "Mission, Workflow, Evidence, "
            "Authority and Governance rules."
        )
    )

    runs = (
        observability.list_runs(
            limit=50
        )
    )

    if not runs:

        st.info(
            "No agent runs are available."
        )

        return

    options = {
        (
            f"{run.started_at} | "
            f"{run.status} | "
            f"{run.research_question[:60]}"
        ): run.run_id
        for run in runs
    }

    selected_label = st.selectbox(
        "Select Run",
        options=list(
            options.keys()
        ),
        key=(
            "evaluation_run_select"
        ),
    )

    run_id = options[
        selected_label
    ]

    if st.button(
        "Evaluate Run",
        type="primary",
        key="evaluate_run_button",
    ):

        try:

            report = (
                evaluation_service
                .evaluate_run(
                    run_id
                )
            )

            st.session_state[
                "evaluation_report"
            ] = report

            st.session_state[
                "evaluation_run_id"
            ] = run_id

        except Exception as error:

            st.error(
                f"Evaluation failed: {error}"
            )

            return

    report = st.session_state.get(
        "evaluation_report"
    )

    evaluated_run_id = (
        st.session_state.get(
            "evaluation_run_id"
        )
    )

    if (
        report is not None
        and evaluated_run_id
        == run_id
    ):

        render_evaluation_report(
            report
        )