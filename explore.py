#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.6
Simple CLI for querying Lenny's podcast corpus with metadata attribution
"""

import sys
import os
import warnings
import argparse
import copy
import json
import urllib.request
import urllib.error
import yaml

# Suppress LangChain deprecation warnings for v0.6
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*was deprecated.*')
try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings('ignore', category=LangChainDeprecationWarning)
except Exception:
    pass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

DEFAULT_CONFIG = {
    "version": "0.6",
    "defaults": {
        "provider": "anthropic",
        "model": "haiku",
        "response_format": "direct_inferred_missing",
        "verbose": True,
    },
    "providers": {
        "anthropic": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "display_name": "Anthropic",
        },
        "openai": {
            "api_key_env": "OPENAI_API_KEY",
            "display_name": "OpenAI",
        },
    },
    "models": {
        "haiku": {
            "provider": "anthropic",
            "id": "claude-haiku-4-5-20251001",
            "label": "Claude Haiku 4.5 (cheapest)",
            "status": "active",
        },
        "sonnet-4": {
            "provider": "anthropic",
            "id": "claude-sonnet-4-20250514",
            "label": "Claude Sonnet 4 (balanced)",
            "status": "active",
        },
        "gpt-4o-mini": {
            "provider": "openai",
            "id": "gpt-4o-mini",
            "label": "GPT-4o mini (cheapest OpenAI)",
            "status": "active",
        },
        "gpt-4o": {
            "provider": "openai",
            "id": "gpt-4o",
            "label": "GPT-4o (quality OpenAI)",
            "status": "active",
        },
    },
    "paths": {
        "vector_db": "data/chroma_db",
    },
    "retrieval": {
        "search_type": "mmr",
        "k": 8,
        "fetch_k": 24,
    },
    "output": {
        "max_sources": 3,
        "response_format": "direct_inferred_missing",
    },
    "features": {
        "web_search": True,
    },
    "web_search": {
        "mode": "on",
        "provider": "serper",
        "endpoint": "https://google.serper.dev/search",
        "api_key_env": "SERPER_API_KEY",
        "max_results": 5,
        "timeout_sec": 10,
    },
}


def deep_merge(base: dict, override: dict) -> dict:
    if not isinstance(override, dict):
        return base
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str = "CONFIGS.yaml") -> dict:
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        if isinstance(user_config, dict):
            return deep_merge(config, user_config)
    except Exception:
        pass
    return config


def build_model_catalog(config: dict) -> dict:
    providers = config.get("providers", {})
    models = config.get("models", {})
    catalog = {}
    for key, data in models.items():
        provider = data.get("provider")
        model_id = data.get("id")
        if not provider or not model_id:
            continue
        label = data.get("label")
        if not label:
            display = providers.get(provider, {}).get("display_name", provider)
            label = f"{display} ({model_id})"
        catalog[key] = {
            "provider": provider,
            "model": model_id,
            "label": label,
        }
    return catalog


def print_model_list(model_catalog: dict):
    print("Available models:")
    for key, meta in model_catalog.items():
        print(f"  {key:12} -> {meta['model']} ({meta['label']})")


def web_search_config(config: dict) -> dict:
    ws = config.get("web_search", {}) or {}
    return {
        "mode": ws.get("mode", "on"),
        "provider": ws.get("provider", "serper"),
        "endpoint": ws.get("endpoint", "https://google.serper.dev/search"),
        "api_key_env": ws.get("api_key_env", "SERPER_API_KEY"),
        "max_results": int(ws.get("max_results", 5)),
        "timeout_sec": int(ws.get("timeout_sec", 10)),
    }


def search_serper(query: str, cfg: dict) -> list[dict]:
    payload = json.dumps({"q": query}).encode("utf-8")
    req = urllib.request.Request(
        cfg["endpoint"],
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": cfg["api_key_env_value"],
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout_sec"]) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return []

    results = []
    organic = data.get("organic", []) or []
    for item in organic[: cfg["max_results"]]:
        title = item.get("title") or ""
        link = item.get("link") or ""
        snippet = item.get("snippet") or ""
        if title or snippet or link:
            results.append({"title": title, "link": link, "snippet": snippet})
    return results


def format_web_results(results: list[dict]) -> str:
    lines = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "").strip()
        link = item.get("link", "").strip()
        snippet = item.get("snippet", "").strip()
        line = f"{i}. {title}"
        if snippet:
            line += f" — {snippet}"
        if link:
            line += f" ({link})"
        lines.append(line)
    return "\n".join(lines)


def format_web_sources(results: list[dict]) -> str:
    lines = []
    for item in results:
        link = (item.get("link") or "").strip()
        title = (item.get("title") or "").strip() or link
        if link:
            lines.append(f"• [{title}]({link})")
    return "\n".join(lines)


def direct_answer_text(answer: str) -> str:
    lower = answer.lower()
    start = lower.find("direct answer:")
    if start == -1:
        return ""
    start = start + len("direct answer:")
    end = lower.find("indirect but relevant insights", start)
    if end == -1:
        end = len(answer)
    return answer[start:end].strip()


def should_web_fallback(answer: str) -> bool:
    direct = direct_answer_text(answer).strip().lower()
    if not direct:
        return True
    if len(direct) < 40:
        return True
    weak_markers = [
        "not found",
        "not in provided context",
        "context is weak",
        "don't know",
        "do not know",
        "no specific",
        "cannot provide",
    ]
    return any(marker in direct for marker in weak_markers)


def resolve_web_search_default(features: dict, web_cfg: dict) -> str:
    mode = web_cfg.get("mode", "on")
    if isinstance(mode, str):
        mode = mode.lower()
    feature_val = features.get("web_search")
    if isinstance(feature_val, str):
        feature_val = feature_val.lower()
    if feature_val in ("on", "off", "always"):
        return feature_val
    if feature_val is False:
        return "off"
    if mode in ("on", "off", "always"):
        return mode
    return "on"


def build_llm(model_key: str, model_catalog: dict, providers: dict):
    meta = model_catalog[model_key]
    provider = meta["provider"]
    model_name = meta["model"]
    provider_meta = providers.get(provider, {})
    api_key_env = provider_meta.get("api_key_env")

    if not api_key_env:
        print(f"❌ Error: Provider '{provider}' is missing api_key_env in CONFIGS.yaml")
        return None, None

    if not os.environ.get(api_key_env):
        print(f"❌ Error: {api_key_env} not found")
        print()
        print("Set your API key:")
        print(f"  export {api_key_env}='sk-...'")
        print()
        print("Then reload your shell:")
        print("  source ~/.bashrc  (or source ~/.zshrc)")
        return None, None

    if provider == "anthropic":
        return ChatAnthropic(model=model_name, temperature=0), meta

    if provider == "openai":
        return ChatOpenAI(model=model_name, temperature=0), meta

    print(f"❌ Error: Unsupported provider: {provider}")
    return None, None

def format_sources(docs, max_sources: int = 3):
    """Format source documents with metadata into readable citations."""
    sources = []
    seen_episodes = set()
    
    for doc in docs:
        metadata = doc.metadata
        guest = metadata.get('guest', 'Unknown')
        title = metadata.get('title', 'Untitled')
        date = metadata.get('publish_date', 'Unknown date')
        youtube_url = metadata.get('youtube_url', '')
        
        # Create unique identifier to avoid duplicate citations
        episode_id = f"{guest}_{title}"
        
        if episode_id not in seen_episodes:
            seen_episodes.add(episode_id)
            citation = f"• {guest}: \"{title}\" ({date})"
            if youtube_url:
                citation += f"\n  {youtube_url}"
            sources.append(citation)
    
    return "\n".join(sources[:max_sources])


def format_docs(docs):
    """Format documents for context."""
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    config = load_config()
    model_catalog = build_model_catalog(config)
    providers = config.get("providers", {})
    defaults = config.get("defaults", {})
    model_choices = sorted(model_catalog.keys())
    default_model = defaults.get("model", "haiku")
    if default_model not in model_catalog and model_choices:
        default_model = model_choices[0]
    default_verbose = defaults.get("verbose", True)
    default_verbose_value = "on" if default_verbose else "off"
    features = config.get("features", {})
    web_cfg = web_search_config(config)
    web_search_default = resolve_web_search_default(features, web_cfg)
    web_search_default_value = web_search_default

    parser = argparse.ArgumentParser(
        description="Query Lenny's podcast corpus with model switching",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Your question in quotes (e.g., \"What does Lenny say about pricing?\")",
    )
    parser.add_argument(
        "--model",
        choices=model_choices,
        default=default_model,
        help="Model to use (see --list-models for options)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )
    parser.add_argument(
        "--verbose",
        choices=["on", "off"],
        default=default_verbose_value,
        help="Verbose output (default from CONFIGS.yaml)",
    )
    parser.add_argument(
        "--web-search",
        choices=["on", "off", "always"],
        default=web_search_default_value,
        help="Web search fallback (default from CONFIGS.yaml)",
    )

    args = parser.parse_args()

    if args.list_models:
        print_model_list(model_catalog)
        return 0

    if not args.question:
        parser.print_help()
        return 1

    verbose = args.verbose == "on"
    web_search_mode = args.web_search
    web_search_requested = web_search_mode != "off"
    web_search_force = web_search_mode == "always"
    web_search_enabled = web_search_requested
    api_key_env = web_cfg.get("api_key_env", "SERPER_API_KEY")
    api_key_value = os.environ.get(api_key_env)
    if web_search_enabled and not api_key_value:
        print(f"⚠️  Web search disabled: {api_key_env} not found")
        web_search_enabled = False

    def vprint(*print_args, **print_kwargs):
        if verbose:
            print(*print_args, **print_kwargs)
    
    # Check if vector DB exists
    vector_db_path = config.get("paths", {}).get("vector_db", "data/chroma_db")
    if not os.path.exists(vector_db_path):
        print("❌ Error: Vector database not found")
        print()
        print("Run setup first:")
        print("  ./setup.sh")
        return 1
    
    query = " ".join(args.question).strip()
    
    vprint()
    vprint("🔍 Searching Lenny's podcast corpus...")
    vprint(f"❓ Question: {query}")
    if web_search_requested:
        mode_label = "FORCED" if web_search_force else "AUTO"
        vprint(f"🌐 Web search fallback: {'ON' if web_search_enabled else 'OFF'} ({mode_label})")
    vprint()
    
    try:
        # Load embeddings (same model used for indexing)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load vector store
        vectorstore = Chroma(
            persist_directory=vector_db_path,
            embedding_function=embeddings
        )
        
        retrieval = config.get("retrieval", {})
        retriever = vectorstore.as_retriever(
            search_type=retrieval.get("search_type", "mmr"),
            search_kwargs={
                "k": retrieval.get("k", 8),
                "fetch_k": retrieval.get("fetch_k", 24),
            },
        )
        
        llm, model_meta = build_llm(args.model, model_catalog, providers)
        if llm is None:
            return 1
        
        # Create prompt template
        response_format = config.get("output", {}).get(
            "response_format", "direct_inferred_missing"
        )
        if response_format == "direct_inferred_missing":
            template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question.
Respond in three sections with these headings:
Direct answer:
Indirect but relevant insights (inferred):
What's missing:
In the Direct answer, give a best‑effort summary grounded in the context. If the context is weak, say so, but still summarize any relevant details you can find.

Context:
{context}

Question: {question}

Answer:"""
        else:
            template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question.
If you don't know the answer based on the context, just say so - don't make things up.

Context:
{context}

Question: {question}

Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Get source documents for attribution
        source_docs = retriever.invoke(query)
        doc_context = format_docs(source_docs)

        def run_answer(context: str) -> str:
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"context": context, "question": query})

        vprint("🤔 Thinking...")

        answer = run_answer(doc_context)
        web_results = []

        if web_search_enabled:
            if web_search_force:
                vprint("🌐 Running web search (forced)...")
                web_cfg["api_key_env_value"] = api_key_value
                if web_cfg.get("provider") == "serper":
                    web_results = search_serper(query, web_cfg)
                if web_results:
                    web_context = format_web_results(web_results)
                    combined_context = doc_context + "\n\nWeb results:\n" + web_context
                    answer = run_answer(combined_context)
                else:
                    vprint("⚠️  Web search returned no results")
            else:
                if should_web_fallback(answer):
                    vprint("🌐 Running web search fallback...")
                    web_cfg["api_key_env_value"] = api_key_value
                    if web_cfg.get("provider") == "serper":
                        web_results = search_serper(query, web_cfg)
                    if web_results:
                        web_context = format_web_results(web_results)
                        combined_context = doc_context + "\n\nWeb results:\n" + web_context
                        answer = run_answer(combined_context)
                    else:
                        vprint("⚠️  Web search returned no results")
                else:
                    vprint("ℹ️  Web search fallback not triggered (direct answer strong)")
        
        print()
        print("💡 Answer:")
        print("-" * 50)
        print(answer)
        print("-" * 50)
        print()
        
        # Show sources with metadata
        max_sources = config.get("output", {}).get("max_sources", 3)
        if source_docs:
            print("📚 Sources:")
            print(format_sources(source_docs, max_sources=max_sources))
            print()
        if web_results:
            print("🌐 Web Sources:")
            print(format_web_sources(web_results))
            print()
        
        vprint(f"ℹ️  Using {model_meta['model']} ({model_meta['label']})")
        vprint("   Cost: varies by model")
        vprint()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("If you're seeing API errors, check:")
        print("  - The correct API key is set for your selected model")
        print("  - You have API credits available")
        print()
        return 1

if __name__ == "__main__":
    exit(main())
