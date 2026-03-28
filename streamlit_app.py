import os
import uuid
from typing import Any

import requests
import streamlit as st


st.set_page_config(
    page_title="BUMBIRO",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DEFAULT_API_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000").rstrip("/")


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "api_url" not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL

    if "show_sources" not in st.session_state:
        st.session_state.show_sources = True

    if "backend_status" not in st.session_state:
        st.session_state.backend_status = None

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def check_backend(api_url: str) -> tuple[bool, str]:
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        response.raise_for_status()
        return True, "Connected"
    except requests.exceptions.RequestException as exc:
        return False, f"Unavailable: {exc}"


def call_query_api(api_url: str, query: str, session_id: str) -> dict[str, Any]:
    response = requests.post(
        f"{api_url}/query",
        json={
            "query": query,
            "session_id": session_id,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def clear_chat() -> None:
    st.session_state.messages = []


def new_chat() -> None:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []


def queue_prompt(prompt: str) -> None:
    st.session_state.pending_prompt = prompt


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## ZIM Constitution AI Assistant")

        if st.button("New chat", use_container_width=True):
            new_chat()
            st.rerun()

        if st.button("Clear messages", use_container_width=True):
            clear_chat()
            st.rerun()

        st.markdown("### Preferences")

        st.session_state.show_sources = st.toggle(
            "Show sources",
            value=st.session_state.show_sources,
        )

        st.markdown("---")
        st.markdown("### Try asking")

        example_prompts = [
           "What is the Constitution of Zimbabwe?",
           "Under what circumstances can the President be removed from office?",
           "When can the military be deployed?",
        ]

        for prompt in example_prompts:
            if st.button(prompt, use_container_width=True):
                queue_prompt(prompt)
                st.rerun()


def render_header() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }
        .app-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-top: 1.2rem;
        }
        .app-subtitle {
            color: #9aa0a6;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        .empty-state {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.2rem 1.2rem 0.8rem 1.2rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
            background: rgba(255,255,255,0.02);
        }
        </style>
        <div class="app-title">⚖️ BUMBIRO</div>
        <div class="app-subtitle">Learn about the Zimbabwean Constitution</div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <p style="margin-bottom: 0.4rem;">
                Ask questions about the Zimbabwean Constitution.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    suggestions = [
        "What is the Constitution of Zimbabwe?",
        "What is the role of Parliament?",
        "When is a person a Zimbabwean citizen by birth?",
        "Who/what is Bumbiro?",
    ]

    for i, prompt in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(prompt, use_container_width=True):
                queue_prompt(prompt)
                st.rerun()


def render_sources(sources: list[str]) -> None:
    if not sources or not st.session_state.show_sources:
        return

    with st.expander("Sources", expanded=False):
        for idx, source in enumerate(sources, start=1):
            st.markdown(f"**Source {idx}**")
            st.write(source)
            if idx < len(sources):
                st.markdown("---")


def render_chat() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                render_sources(message.get("sources", []))


def handle_query(user_query: str) -> None:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        try:
            with st.spinner("Thinking..."):
                result = call_query_api(
                    api_url=st.session_state.api_url,
                    query=user_query,
                    session_id=st.session_state.session_id,
                )

            answer = str(result.get("answer", "")).strip()
            sources = result.get("sources", [])

            if not isinstance(sources, list):
                sources = [str(sources)]

            if not answer:
                answer = "No answer was returned by the backend."

            response_placeholder.markdown(answer)
            render_sources(sources)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )

        except requests.exceptions.HTTPError as exc:
            error_message = f"API error: {exc}"
            response_placeholder.error(error_message)

            if exc.response is not None:
                try:
                    st.json(exc.response.json())
                except Exception:
                    st.code(exc.response.text)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )

        except requests.exceptions.RequestException as exc:
            error_message = f"Connection error: {exc}"
            response_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )

        except Exception as exc:
            error_message = f"Unexpected error: {exc}"
            response_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )


def main() -> None:
    init_session_state()
    render_sidebar()
    render_header()

    if not st.session_state.messages:
        render_welcome_state()

    render_chat()

    queued_prompt = st.session_state.pending_prompt
    if queued_prompt:
        st.session_state.pending_prompt = None
        handle_query(queued_prompt)
        st.rerun()

    user_query = st.chat_input("Message RAG Assistant")

    if user_query:
        handle_query(user_query)
        st.rerun()


if __name__ == "__main__":
    main()