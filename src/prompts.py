FEW_SHOT_EXAMPLES = {
    "General": (
        "Here are examples of high-quality responses:\n\n"
        "Task: Explain recursion\n"
        "Response: Recursion is when a function calls itself. "
        "Think of Russian dolls — each doll contains a smaller version of itself. "
        "A recursive function has a base case (the smallest doll) and a recursive case.\n\n"
        "Task: Summarize machine learning in one sentence\n"
        "Response: Machine learning is teaching computers to learn patterns from data "
        "instead of programming rules explicitly.\n"
    ),
    "Code": (
        "Here are examples of clear code explanations:\n\n"
        "Task: What does list comprehension do in Python?\n"
        "Response: List comprehension creates a new list by applying an expression to "
        "each item in an iterable — [x*2 for x in range(5)] gives [0,2,4,6,8]. "
        "It replaces for-loops in a single readable line.\n\n"
        "Task: Explain async/await\n"
        "Response: async/await lets code pause and wait for slow operations "
        "(like network calls) without blocking the rest of the program.\n"
    ),
    "Summarization": (
        "Here are examples of concise, accurate summaries:\n\n"
        "Original: The transformer architecture introduced in 2017 changed NLP forever "
        "by replacing recurrent networks with self-attention mechanisms.\n"
        "Summary: Transformers (2017) replaced RNNs with self-attention, revolutionizing NLP.\n\n"
        "Original: Python's GIL prevents multiple threads from executing Python bytecode simultaneously.\n"
        "Summary: Python's GIL limits true multi-threading for CPU-bound tasks.\n"
    ),
}

SYSTEM_PROMPTS = {
    "Zero-shot": "You are a helpful, concise assistant. Answer directly.",
    "Few-shot": "You are a helpful assistant. Follow the pattern shown in the examples.",
    "Chain-of-Thought": (
        "You are a careful, analytical assistant. "
        "Always reason step by step before concluding."
    ),
}

def build_zero_shot(task: str) -> list[dict]:
    return [{"role": "user", "content": task}]

def build_few_shot(task: str, domain: str) -> list[dict]:
    examples = FEW_SHOT_EXAMPLES.get(domain, FEW_SHOT_EXAMPLES["General"])
    content = examples + f"\n\nNow do the same:\n{task}"
    return [{"role": "user", "content": content}]

def build_cot(task: str) -> list[dict]:
    content = (
        f"{task}\n\n"
        "Think through this step by step before giving your final answer. "
        "Show your reasoning clearly."
    )
    return [{"role": "user", "content": content}]
