import os
import time
import streamlit as st
import anthropic
from dotenv import load_dotenv
from src.config import MODEL

load_dotenv()

@st.cache_resource
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("Set ANTHROPIC_API_KEY as an environment variable before running.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

client = get_client()

def call_claude(messages: list[dict], system: str) -> tuple[str, float]:
    start = time.time()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system,
        messages=messages,
    )
    elapsed = round(time.time() - start, 2)
    return resp.content[0].text.strip(), elapsed
