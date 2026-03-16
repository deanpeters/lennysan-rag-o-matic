"""
LennySan RAG-o-Matic v0.9 — Browser UI
Run with: streamlit run app.py
"""

import os
import re
import warnings
import streamlit as st

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*was deprecated.*")
try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except Exception:
    pass

from explore import (
    load_config,
    build_model_catalog,
    build_llm,
    web_search_config,
    resolve_web_search_default,
    run_web_search,
    format_web_results,
    format_web_sources,
    format_sources,
    format_docs,
    parse_answer_sections,
    direct_is_missing,
    run_deanifried,
    should_web_fallback,
    docker_available,
    searxng_ping,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="LennySan RAG-o-Matic",
    page_icon="🎙️",
    layout="centered",
)

# ── Load config once ─────────────────────────────────────────────────────────

@st.cache_resource
def get_config():
    return load_config()

@st.cache_resource
def get_model_catalog(config):
    return build_model_catalog(config)

@st.cache_resource
def get_vectorstore(vector_db_path):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=vector_db_path, embedding_function=embeddings)

config = get_config()
model_catalog = get_model_catalog(config)
providers = config.get("providers", {})
retrieval = config.get("retrieval", {})
vector_db_path = config.get("paths", {}).get("vector_db", "data/chroma_db")

# ── Friendly model labels ─────────────────────────────────────────────────────

FRIENDLY_LABELS = {
    "haiku":      "Fast & cheap — Claude Haiku",
    "sonnet-4":   "Balanced — Claude Sonnet 4",
    "gpt-4o-mini":"Fast & cheap — GPT-4o mini",
    "gpt-4o":     "Quality — GPT-4o",
}

def friendly(key):
    return FRIENDLY_LABELS.get(key, key)

model_keys = list(model_catalog.keys())
model_display = [friendly(k) for k in model_keys]
default_model_key = config.get("defaults", {}).get("model", "haiku")
default_index = model_keys.index(default_model_key) if default_model_key in model_keys else 0

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Options")

    selected_display = st.selectbox(
        "Which AI to use",
        options=model_display,
        index=default_index,
        help="Haiku and GPT-4o mini are cheaper. Sonnet and GPT-4o give richer answers.",
    )
    selected_model_key = model_keys[model_display.index(selected_display)]

    web_search_on = st.checkbox(
        "Also search the web",
        value=False,
        help="When checked, the app will supplement the podcast corpus with current web results if the corpus answer is thin.",
    )

    deanifried_on = st.checkbox(
        "Dean-i-fried voice",
        value=False,
        help="Rewrites the answer in Dean Peters' voice — vivid, opinionated, and a little absurd. Best for sharing, not research.",
    )

    if deanifried_on:
        platform_options = {
            "Just reading here": "cli",
            "Twitter / X": "x",
            "LinkedIn": "linkedin",
            "Reddit": "reddit",
            "Substack": "substack",
        }
        platform_display = st.selectbox(
            "Writing for",
            options=list(platform_options.keys()),
            help="Shapes the length and tone of the Dean-i-fried response.",
        )
        deanifried_platform = platform_options[platform_display]
    else:
        deanifried_platform = "cli"

    st.divider()
    response_style = st.radio(
        "Response style",
        options=["Full analysis", "Direct answer only"],
        index=0,
        help=(
            "**Full analysis** — breaks the answer into Direct answer, "
            "Related insights, and What's missing.\n\n"
            "**Direct answer only** — a single plain response, no sections."
        ),
    )

    st.divider()
    with st.expander("❓ What do these mean?"):
        st.markdown(
            """
**Full analysis** breaks every answer into three parts:

- **Direct answer** — what the corpus explicitly says about your question, grounded in real transcript excerpts.
- **Related insights** — adjacent ideas and patterns from the corpus that are relevant but not a direct answer. Labeled as inferred so you know it's a step removed.
- **What's missing** — an honest note about where the corpus is thin or silent on your topic.

---

**Direct answer only** skips the breakdown and gives you a single, plain response. Faster to read; less nuance.

---

**Dean-i-fried voice** takes whatever the model found and rewrites it in Dean Peters' voice — vivid, opinionated, a little absurd. Think of it as a synthesis for sharing, not for research. It always appears *below* the analysis so you see both.

---

**Also search the web** adds current web results when the corpus answer is thin. Useful for topics that have evolved since the episodes were recorded.
"""
        )

    st.caption("Powered by Lenny Rachitsky's podcast corpus, built by the RAG-o-Matic project.")

# ── Main area ─────────────────────────────────────────────────────────────────

st.title("🎙️ LennySan RAG-o-Matic")
st.caption("Ask anything about Lenny Rachitsky's podcast. Answers are grounded in real transcript excerpts.")

question = st.text_area(
    label="Your question",
    placeholder="Ask anything about Lenny's podcast — pricing, growth, hiring, leadership...",
    height=100,
    label_visibility="collapsed",
)

ask_clicked = st.button("Ask Lenny", type="primary", use_container_width=True)

# ── Preflight checks ──────────────────────────────────────────────────────────

def check_ready():
    """Return (ok, message) before running a query."""
    if not os.path.exists(vector_db_path):
        return False, (
            "The podcast index hasn't been built yet. "
            "Open a terminal, navigate to this folder, and run: `./setup.sh`"
        )
    meta = model_catalog.get(selected_model_key, {})
    provider = meta.get("provider")
    provider_meta = providers.get(provider, {})
    api_key_env = provider_meta.get("api_key_env")
    if api_key_env and not os.environ.get(api_key_env):
        return False, (
            f"Your API key for **{provider_meta.get('display_name', provider)}** isn't set up yet. "
            f"In your terminal run: `export {api_key_env}='sk-...'` then restart the app."
        )
    return True, ""

# ── Export builder ───────────────────────────────────────────────────────────

def build_export_markdown(question, answer, response_style, deanifried_text,
                          source_docs, web_results, model_label, max_sources):
    from datetime import date
    lines = []
    lines.append(f"# LennySan RAG-o-Matic — Query Export")
    lines.append(f"")
    lines.append(f"**Date:** {date.today().isoformat()}")
    lines.append(f"**Model:** {model_label}")
    lines.append(f"**Response style:** {response_style}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Question")
    lines.append(f"")
    lines.append(question)
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    if response_style == "Full analysis":
        sections = parse_answer_sections(answer)
        direct = sections.get("direct", "").strip()
        indirect = sections.get("indirect", "").strip()
        missing = sections.get("missing", "").strip()
        if any([direct, indirect, missing]):
            if direct:
                lines.append(f"## Direct answer")
                lines.append(f"")
                lines.append(direct)
                lines.append(f"")
            if indirect:
                lines.append(f"## Related insights (inferred)")
                lines.append(f"")
                lines.append(indirect)
                lines.append(f"")
            if missing:
                lines.append(f"## What's missing")
                lines.append(f"")
                lines.append(missing)
                lines.append(f"")
        else:
            lines.append(f"## Answer")
            lines.append(f"")
            lines.append(answer)
            lines.append(f"")
    else:
        lines.append(f"## Answer")
        lines.append(f"")
        lines.append(answer)
        lines.append(f"")

    if deanifried_text:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Dean-i-fried")
        lines.append(f"")
        lines.append(deanifried_text.strip())
        lines.append(f"")

    if source_docs:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Sources")
        lines.append(f"")
        seen = set()
        count = 0
        for doc in source_docs:
            if count >= max_sources:
                break
            m = doc.metadata
            guest = m.get("guest", "Unknown")
            title = m.get("title", "Untitled")
            date_str = m.get("publish_date", "")
            url = m.get("youtube_url", "")
            eid = f"{guest}_{title}"
            if eid in seen:
                continue
            seen.add(eid)
            count += 1
            date_part = f" · {date_str}" if date_str else ""
            if url:
                lines.append(f"- **{guest}** — [{title}]({url}){date_part}")
            else:
                lines.append(f"- **{guest}** — {title}{date_part}")
        lines.append(f"")

    if web_results:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Web sources")
        lines.append(f"")
        for item in web_results:
            link = item.get("link", "")
            title = item.get("title", link)
            snippet = item.get("snippet", "")
            if link:
                entry = f"- [{title}]({link})"
                if snippet:
                    entry += f" — {snippet}"
                lines.append(entry)
        lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Generated by [LennySan RAG-o-Matic](https://github.com/deanpeters/lennysan-rag-o-matic)*")

    return "\n".join(lines)


# ── Query logic ───────────────────────────────────────────────────────────────

def run_query(question, model_key, response_style, web_search_on, deanifried_on, deanifried_platform):
    ok, msg = check_ready()
    if not ok:
        st.error(msg)
        return

    web_cfg = web_search_config(config)
    api_key_value = None
    web_enabled = False
    web_notice = ""

    if web_search_on:
        provider = web_cfg.get("provider", "api")
        api_key_env = web_cfg.get("api_key_env", "SERPER_API_KEY")
        if provider == "api":
            api_key_value = os.environ.get(api_key_env)
            if api_key_value:
                web_enabled = True
            else:
                web_notice = "Web search is off — no Serper API key found."
        elif provider == "docker":
            ok_docker, reason = docker_available()
            if ok_docker:
                ping_ok, ping_reason = searxng_ping(web_cfg)
                if ping_ok:
                    web_enabled = True
                else:
                    web_notice = f"Web search is off — SearXNG not reachable ({ping_reason})."
            else:
                web_notice = f"Web search is off — Docker not available ({reason})."

    vectorstore = get_vectorstore(vector_db_path)
    retriever = vectorstore.as_retriever(
        search_type=retrieval.get("search_type", "mmr"),
        search_kwargs={
            "k": retrieval.get("k", 8),
            "fetch_k": retrieval.get("fetch_k", 24),
        },
    )

    llm, model_meta = build_llm(model_key, model_catalog, providers)
    if llm is None:
        st.error("Couldn't connect to the AI model. Check that your API key is set correctly.")
        return

    if response_style == "Full analysis":
        template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question.
Respond in three sections with these exact headings:
Direct answer:
Indirect but relevant insights (inferred):
What's missing:

Rules:
- No bullet points in prose. Use sentences and short paragraphs.
- Minimums are not targets. If the context supports more, go longer. Do not pad with filler.
- Prefer substance over brevity. Use additional sentences when they add clarity, nuance, or helpful detail.
- Direct answer: 2-6 sentences (more if context is rich). Give a best-effort summary grounded in the context. If the context is weak, say so, but still summarize any relevant details you can find.
- Direct answer must include at least two concrete details from the context (names, examples, outcomes, quotes, or actions). If the context does not provide two details, explicitly say that and explain what is missing.
- Indirect insights: 3-6 sentences with at least two distinct insights grounded in the context.
- What's missing: 1-3 sentences describing gaps or absent information.

Context:
{context}

Question: {question}

Answer:"""
    else:
        template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question clearly and directly.
If you don't know the answer based on the context, say so honestly — don't make things up.
Write in plain prose. No bullet points. No section headings. 3-6 sentences.

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    source_docs = retriever.invoke(question)
    doc_context = format_docs(source_docs)

    def run_answer(context):
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"context": context, "question": question})

    with st.spinner("Searching the corpus..."):
        answer = run_answer(doc_context)

    web_results = []
    if web_enabled:
        if should_web_fallback(answer):
            with st.spinner("Corpus answer was thin — searching the web too..."):
                web_results, _ = run_web_search(question, web_cfg, api_key_value)
                if web_results:
                    web_context = format_web_results(web_results)
                    combined = doc_context + "\n\nWeb results:\n" + web_context
                    with st.spinner("Incorporating web results..."):
                        answer = run_answer(combined)

    deanifried_text = ""
    if deanifried_on:
        sections = parse_answer_sections(answer)
        direct_text = sections.get("direct", "")
        indirect_text = sections.get("indirect", "") or answer.strip()
        if direct_is_missing(direct_text):
            direct_text = ""
        web_context = format_web_results(web_results) if web_results else ""
        with st.spinner("Dean-i-frying..."):
            deanifried_text = run_deanifried(
                llm=llm,
                direct=direct_text,
                indirect=indirect_text,
                web=web_context,
                platform=deanifried_platform,
            )

    # ── Display answer ────────────────────────────────────────────────────────

    st.divider()

    if response_style == "Full analysis":
        sections = parse_answer_sections(answer)
        direct = sections.get("direct", "").strip()
        indirect = sections.get("indirect", "").strip()
        missing = sections.get("missing", "").strip()
        parsed_ok = any([direct, indirect, missing])

        if parsed_ok:
            if direct:
                st.markdown("### 💡 Direct answer")
                st.markdown(direct)
            if indirect:
                with st.expander("📎 Related insights (inferred)", expanded=True):
                    st.markdown(indirect)
            if missing:
                with st.expander("🔍 What's missing from the corpus"):
                    st.markdown(missing)
        else:
            # Parsing failed — show raw answer so nothing is lost
            st.markdown("### 💡 Answer")
            st.markdown(answer)
    else:
        st.markdown("### 💡 Answer")
        st.markdown(answer)

    if deanifried_text:
        st.divider()
        st.markdown("### 🎭 Dean-i-fried")
        st.caption("A synthesis of the answer above, written in Dean Peters' voice.")
        st.markdown(deanifried_text.strip())

    # ── Sources ───────────────────────────────────────────────────────────────

    max_sources = config.get("output", {}).get("max_sources", 3)
    if source_docs:
        st.divider()
        st.markdown("### 📚 Sources")
        seen = set()
        count = 0
        for doc in source_docs:
            if count >= max_sources:
                break
            m = doc.metadata
            guest = m.get("guest", "Unknown")
            title = m.get("title", "Untitled")
            date = m.get("publish_date", "")
            url = m.get("youtube_url", "")
            eid = f"{guest}_{title}"
            if eid in seen:
                continue
            seen.add(eid)
            count += 1
            date_str = f" · {date}" if date else ""
            if url:
                st.markdown(f"**{guest}** — [{title}]({url}){date_str}")
            else:
                st.markdown(f"**{guest}** — {title}{date_str}")

    if web_results:
        st.divider()
        st.markdown("### 🌐 Web sources")
        for item in web_results:
            link = item.get("link", "")
            title = item.get("title", link)
            snippet = item.get("snippet", "")
            if link:
                st.markdown(f"[{title}]({link})")
                if snippet:
                    st.caption(snippet)

    if web_notice:
        st.info(web_notice)

    st.caption(f"Answer generated by {model_meta['label']}")

    # ── Export ────────────────────────────────────────────────────────────────

    st.divider()
    md = build_export_markdown(
        question=question,
        answer=answer,
        response_style=response_style,
        deanifried_text=deanifried_text,
        source_docs=source_docs,
        web_results=web_results,
        model_label=model_meta["label"],
        max_sources=max_sources,
    )
    slug = question[:40].strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    filename = f"lenny-{slug}.md"
    st.download_button(
        label="⬇️ Download as Markdown",
        data=md,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )

# ── Trigger ───────────────────────────────────────────────────────────────────

if ask_clicked:
    if not question.strip():
        st.warning("Type a question first.")
    else:
        run_query(question.strip(), selected_model_key, response_style, web_search_on, deanifried_on, deanifried_platform)
