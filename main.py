"""
Prompt A/B Tester — Streamlit + Claude API
Run: streamlit run main.py
Requires: pip install streamlit anthropic pandas python-dotenv
"""

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

from src.config import MODEL, CUSTOM_CSS
from src.prompts import (
    FEW_SHOT_EXAMPLES,
    SYSTEM_PROMPTS,
    build_zero_shot,
    build_few_shot,
    build_cot,
)
from src.llm import call_claude
from src.judge import judge_outputs

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prompt A/B Tester",
    page_icon="🧪",
    layout="wide",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []  # list of result dicts

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    domain = st.selectbox("Domain / few-shot context", list(FEW_SHOT_EXAMPLES.keys()))
    st.markdown("---")
    st.markdown(f"**Model:** {MODEL}")
    st.markdown("**Strategies:** Zero-shot · Few-shot · CoT")
    st.markdown("---")
    st.markdown(
        "**Tip:** Run 10+ tasks in one session, then export CSV "
        "to get real numbers for your resume bullet."
    )
    if st.session_state.history:
        df_export = pd.DataFrame(st.session_state.history)
        csv = df_export.to_csv(index=False)
        st.download_button(
            "⬇️ Download results CSV",
            data=csv,
            file_name="prompt_ab_results.csv",
            mime="text/csv",
        )
        if st.button("🗑️ Clear history"):
            st.session_state.history = []
            st.rerun()

# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("🧪 Prompt A/B Tester")
st.caption("Compare Zero-shot · Few-shot · Chain-of-Thought side by side with LLM-as-judge scoring")

task = st.text_area(
    "Enter a task for all three strategies",
    placeholder="e.g.  Explain how gradient descent works in simple terms",
    height=90,
)

run_col, _ = st.columns([1, 4])
with run_col:
    run = st.button("▶ Run all strategies", type="primary", use_container_width=True)

# ── Run experiment ────────────────────────────────────────────────────────────
if run:
    if not task.strip():
        st.warning("Enter a task first.")
    else:
        col1, col2, col3 = st.columns(3)
        outputs = {}
        latencies = {}

        strategies = {
            "Zero-shot": (build_zero_shot(task), SYSTEM_PROMPTS["Zero-shot"]),
            "Few-shot": (build_few_shot(task, domain), SYSTEM_PROMPTS["Few-shot"]),
            "Chain-of-Thought": (build_cot(task), SYSTEM_PROMPTS["Chain-of-Thought"]),
        }

        cols = [col1, col2, col3]
        placeholders = {}
        for col, (label, _) in zip(cols, strategies.items()):
            with col:
                st.markdown(f'<div class="strategy-tag">{label}</div>', unsafe_allow_html=True)
                placeholders[label] = st.empty()
                placeholders[label].info("Running…")

        for label, (messages, system) in strategies.items():
            try:
                output, latency = call_claude(messages, system)
            except Exception as e:
                output, latency = f"Error: {e}", 0.0
            outputs[label] = output
            latencies[label] = latency
            placeholders[label].markdown(output)

        # Judge
        with st.spinner("🤖 Judge scoring all three outputs…"):
            try:
                scores = judge_outputs(task, outputs)
            except Exception as e:
                st.error(f"Judge failed: {e}")
                scores = {}

        # Display scores under each column
        if scores:
            cols2 = st.columns(3)
            winner_label, winner_total = "", 0
            for col, label in zip(cols2, strategies.keys()):
                with col:
                    s = scores.get(label, {})
                    acc = s.get("accuracy", "?")
                    cla = s.get("clarity", "?")
                    note = s.get("reasoning", "")
                    total = (acc if isinstance(acc, int) else 0) + (cla if isinstance(cla, int) else 0)

                    def badge(score):
                        if isinstance(score, int):
                            if score >= 8: return "score-high"
                            if score >= 6: return "score-mid"
                            return "score-low"
                        return "score-mid"

                    st.markdown(
                        f'<span class="score-box {badge(acc)}">Accuracy {acc}/10</span>'
                        f'<span class="score-box {badge(cla)}">Clarity {cla}/10</span>',
                        unsafe_allow_html=True,
                    )
                    st.caption(f"⏱ {latencies.get(label, 0)}s · {note}")

                    if total > winner_total:
                        winner_total = total
                        winner_label = label

            st.markdown(
                f'<div class="winner-banner">🏆 Winner this round: <strong>{winner_label}</strong> '
                f'(combined score {winner_total}/20)</div>',
                unsafe_allow_html=True,
            )

            # Save to history
            row = {
                "task": task,
                "domain": domain,
            }
            for label in strategies:
                s = scores.get(label, {})
                row[f"{label}_output"] = outputs.get(label, "")
                row[f"{label}_accuracy"] = s.get("accuracy", "")
                row[f"{label}_clarity"] = s.get("clarity", "")
                row[f"{label}_latency_s"] = latencies.get(label, "")
            row["winner"] = winner_label
            st.session_state.history.append(row)

# ── History table ─────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.subheader(f"📊 Session results ({len(st.session_state.history)} runs)")

    summary_rows = []
    for r in st.session_state.history:
        summary_rows.append({
            "Task": r["task"][:60] + ("…" if len(r["task"]) > 60 else ""),
            "Domain": r["domain"],
            "Zero-shot acc": r.get("Zero-shot_accuracy"),
            "Few-shot acc": r.get("Few-shot_accuracy"),
            "CoT acc": r.get("Chain-of-Thought_accuracy"),
            "Winner": r.get("winner"),
        })

    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    # Win counts bar
    wins = pd.DataFrame(st.session_state.history)["winner"].value_counts()
    st.markdown("**Win count by strategy**")
    st.bar_chart(wins)