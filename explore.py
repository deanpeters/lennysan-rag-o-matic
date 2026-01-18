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
from langchain_core.runnables import RunnablePassthrough

DEFAULT_CONFIG = {
    "version": "0.6",
    "defaults": {
        "provider": "anthropic",
        "model": "haiku",
        "response_format": "direct_inferred_missing",
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
    model_choices = sorted(model_catalog.keys())
    default_model = config.get("defaults", {}).get("model", "haiku")
    if default_model not in model_catalog and model_choices:
        default_model = model_choices[0]

    parser = argparse.ArgumentParser(
        description="Query Lenny's podcast corpus with model switching",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "question",
        nargs=argparse.REMAINDER,
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

    args = parser.parse_args()

    if args.list_models:
        print_model_list(model_catalog)
        return 0

    if not args.question:
        parser.print_help()
        return 1
    
    # Check if vector DB exists
    vector_db_path = config.get("paths", {}).get("vector_db", "data/chroma_db")
    if not os.path.exists(vector_db_path):
        print("❌ Error: Vector database not found")
        print()
        print("Run setup first:")
        print("  ./setup.sh")
        return 1
    
    query = " ".join(args.question).strip()
    
    print()
    print("🔍 Searching Lenny's podcast corpus...")
    print(f"❓ Question: {query}")
    print()
    
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
        
        # Build RAG chain
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        print("🤔 Thinking...")
        
        # Get answer
        answer = rag_chain.invoke(query)
        
        # Get source documents for attribution
        source_docs = retriever.invoke(query)
        
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
        
        print(f"ℹ️  Using {model_meta['model']} ({model_meta['label']})")
        print("   Cost: varies by model")
        print()
        
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
