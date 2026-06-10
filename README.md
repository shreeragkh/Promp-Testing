# Prompt Testing

A prompt engineering benchmarking tool that runs the same task through three prompting strategies side by side — Zero-shot, Few-shot, and Chain-of-Thought — and uses Claude as an LLM-as-judge to score each output automatically.

Built with Python, Streamlit, and the Anthropic Claude API.

---

## What it does

- Runs any task through all three strategies in a single click
- Scores each output on **accuracy** and **clarity** (1–10) using a separate LLM-as-judge call
- Declares a winner per run based on combined score
- Tracks all runs in a session history table with win counts
- Exports results as a CSV for offline analysis

---

## Project structure

```
prompt_testing/
│
├── app.py                  # Streamlit entry point — UI, layout, session state
│
├── core/
│   ├── config.py           # Model settings, system prompts, few-shot examples
│   ├── prompts.py          # Prompt builder functions (zero-shot, few-shot, CoT)
│   └── claude_client.py    # Anthropic API wrapper — call_claude(), judge_outputs()
│
├── requirements.txt
└── README.md
```

---

## Prompting strategies

| Strategy | What it does |
|---|---|
| Zero-shot | Sends the task directly with no examples or extra framing |
| Few-shot | Prepends 2 domain-specific input-output examples before the task |
| Chain-of-Thought | Appends "think step by step" instruction to the task |

Each strategy has its own role-based system prompt defined in `core/config.py`.

---

## Domains supported

Select a domain from the sidebar to switch the few-shot examples context:

- **General** — everyday explanations and definitions
- **Code** — programming concept explanations
- **Summarization** — condensing technical text into one-liners

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/shreeragkh/prompt-testing
cd prompt_testing
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**
```bash
export ANTHROPIC_API_KEY=your_key_here
```

**4. Run**
```bash
streamlit run app.py
```

---

## Requirements

```
streamlit
anthropic
pandas
```

Or install directly:
```bash
pip install streamlit anthropic pandas
```

---

## How LLM-as-judge works

After all three strategy outputs are generated, a separate Claude call is made with a structured scoring prompt. The judge receives the original task and all three outputs, then returns a JSON object with `accuracy`, `clarity`, and a short `reasoning` note for each strategy.

```json
{
  "Zero-shot":        {"accuracy": 7, "clarity": 8, "reasoning": "Direct but shallow"},
  "Few-shot":         {"accuracy": 8, "clarity": 9, "reasoning": "Matched example pattern well"},
  "Chain-of-Thought": {"accuracy": 9, "clarity": 7, "reasoning": "Thorough but verbose"}
}
```

The strategy with the highest combined score (accuracy + clarity) is declared the winner for that run.

---

## Benchmark results (sample — Code domain, 15 runs)

| Strategy | Avg Accuracy | Avg Clarity | Win count |
|---|---|---|---|
| Zero-shot | 7.1 | 7.4 | 2 |
| Few-shot | 7.8 | 8.2 | 5 |
| Chain-of-Thought | 8.6 | 7.1 | 8 |

Chain-of-Thought outperformed Zero-shot on 10/15 tasks in the Code domain. Export your own results via the CSV download button in the sidebar.

---

## Model

Uses `claude-haiku-4-5` by default — fast and cost-efficient for running multiple calls per experiment. Switch to Sonnet or Opus in `core/config.py`:

```python
MODEL = "claude-haiku-4-5-20251001"   # default
# MODEL = "claude-sonnet-4-20250514"  # higher quality
```

---

## Skills demonstrated

- Prompt Engineering — Zero-shot, Few-shot, Chain-of-Thought, Role-based system prompts
- LLM Evaluation — LLM-as-judge pattern, structured JSON output from Claude
- Anthropic Claude API — messages API, system prompts, multi-call orchestration
- Streamlit — session state, sidebar, columns, CSV export
- Python project structure — modular separation of config, prompts, and API logic

---

## Author

**Shreerag Namboothiri K H**
[GitHub](https://github.com/shreeragkh) · [LinkedIn](https://www.linkedin.com/in/shreeragkh)
