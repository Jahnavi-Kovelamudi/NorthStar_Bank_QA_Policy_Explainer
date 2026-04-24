import os
import time
import requests
import streamlit as st

DEFAULT_BACKEND_URL = "https://northstar-bank-qa-policy-explainer-155760379722.us-central1.run.app"

st.set_page_config(
    page_title="NorthStar Bank QA Policy Explainer",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}
.hero {
    background: linear-gradient(135deg, #0f172a, #1d4ed8);
    color: white;
    padding: 1.4rem 1.6rem;
    border-radius: 18px;
    margin-bottom: 1rem;
}
.answer-box {
    background: white;
    border: 1px solid #dbe4f0;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06);
}
.small-note {
    color: #475569;
    font-size: 0.95rem;
}
.file-chip {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    margin: 0.2rem 0.25rem 0.2rem 0;
    border-radius: 999px;
    background: #e2e8f0;
    color: #0f172a;
    font-size: 0.85rem;
}
.time-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin: 0.35rem 0 0.85rem 0;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: #eef4ff;
    color: #334155;
    font-size: 0.85rem;
    border: 1px solid #dbe4f0;
}
.time-icon {
    font-size: 0.95rem;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

if "question" not in st.session_state:
    st.session_state.question = ""

sample_questions = [
    "What is the difference between checking and savings accounts?",
    "I clicked a suspicious link and now I see an unfamiliar debit card transaction.",
    "Why was my credit card charged a late fee?",
    "How should I respond to an unauthorized card transaction?"
]

with st.sidebar:
    st.title("Controls")

    mode = st.radio(
        "Response mode",
        ["Presentation", "Explainability"],
        help="Presentation uses /ask. Explainability uses /assist."
    )

    backend_base_url = st.text_input(
        "Backend base URL",
        value=os.getenv("BACKEND_BASE_URL", DEFAULT_BACKEND_URL)
    ).strip().rstrip("/")

    st.markdown("### Example prompts")
    for i, q in enumerate(sample_questions):
        if st.button(q, key=f"sample_{i}"):
            st.session_state.question = q

st.markdown("""
<div class="hero">
    <h1 style="margin-bottom: 0.3rem;">NorthStar Bank QA Policy Explainer</h1>
    <div style="font-size: 1.02rem;">
        Banking-support multi-agent assistant with secure guardrails, targeted retrieval,
        domain routing, final answer generation, and critique.
    </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([2.1, 1])

with left:
    st.subheader("Ask your question")
    question = st.text_area(
        "Banking question",
        key="question",
        height=150,
        placeholder="Example: I clicked a suspicious link and now I see an unfamiliar debit card transaction."
    )

with right:
    st.subheader("Current mode")
    if mode == "Presentation":
        st.info("Calls /ask and shows only the user-facing answer.")
    else:
        st.info("Calls /assist and shows answer + planner + retrieval + critic + trace.")

    st.markdown(
        '<div class="small-note">Use Presentation mode for a simple demo. '
        'Use Explainability mode to justify why the system produced the answer.</div>',
        unsafe_allow_html=True
    )

col_a, col_b = st.columns([1, 1])

with col_a:
    submit_clicked = st.button("Get Response", type="primary", use_container_width=True)

with col_b:
    if st.button("Clear", use_container_width=True):
        st.session_state.question = ""
        st.rerun()

if submit_clicked:
    if not backend_base_url:
        st.error("Please enter the backend base URL in the sidebar.")
    elif not question.strip():
        st.warning("Please enter a banking-related question.")
    else:
        endpoint = "/ask" if mode == "Presentation" else "/assist"
        full_url = f"{backend_base_url}{endpoint}"

        st.caption(f"Calling: {full_url}")

        try:
            with st.spinner("Contacting backend..."):
                start_time = time.perf_counter()
                response = requests.post(
                    full_url,
                    json={"question": question},
                    timeout=90
                )
                end_time = time.perf_counter()
                elapsed_seconds = end_time - start_time

            st.markdown(
                f"""
                <div class="time-pill">
                    <span class="time-icon">⏱️</span>
                    <span>Answered in {elapsed_seconds:.2f} sec</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if response.status_code != 200:
                st.error(f"Backend returned status {response.status_code}")
                st.code(response.text)
            else:
                data = response.json()

                if mode == "Presentation":
                    answer = data.get("answer", "No answer returned.")

                    st.markdown("## Final Answer")
                    st.markdown(
                        f'<div class="answer-box">{answer}</div>',
                        unsafe_allow_html=True
                    )

                else:
                    answer = data.get("final_answer", "No final answer returned.")
                    planner = data.get("planner", {})
                    matched_files = data.get("matched_files", [])
                    domain_outputs = data.get("domain_outputs", [])
                    critic_feedback = data.get("critic_feedback", {})
                    trace = data.get("trace", [])
                    question_echo = data.get("question", "")

                    st.markdown("## Final Answer")
                    st.markdown(
                        f'<div class="answer-box">{answer}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown("## Explainability")

                    ex1, ex2 = st.columns(2)

                    with ex1:
                        with st.expander("Planner output", expanded=True):
                            st.json(planner)

                        with st.expander("Matched files", expanded=True):
                            if matched_files:
                                for f in matched_files:
                                    st.markdown(
                                        f"<span class='file-chip'>{f}</span>",
                                        unsafe_allow_html=True
                                    )
                            else:
                                st.info("No matched files returned.")

                        with st.expander("Trace", expanded=False):
                            if trace:
                                st.write(" → ".join(trace))
                            else:
                                st.info("No trace returned.")

                    with ex2:
                        with st.expander("Domain outputs", expanded=True):
                            st.json(domain_outputs)

                        with st.expander("Critic feedback", expanded=True):
                            st.json(critic_feedback)

                    with st.expander("Full backend response", expanded=False):
                        st.json(data)

                    with st.expander("Question sent to backend", expanded=False):
                        st.write(question_echo)

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")