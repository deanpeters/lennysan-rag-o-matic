#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.1
Simple CLI for querying Lenny's podcast corpus with metadata attribution
"""

import sys
import os
import warnings
import argparse

# Suppress LangChain deprecation warnings for v0.1
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

MODEL_CATALOG = {
    "haiku": {
        "provider": "anthropic",
        "model": "claude-haiku-4-5-20251001",
        "label": "Claude Haiku 4.5 (cheapest)",
    },
    "sonnet-4": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-20250514",
        "label": "Claude Sonnet 4 (balanced)",
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "label": "GPT-4o mini (cheapest OpenAI)",
    },
    "gpt-4o": {
        "provider": "openai",
        "model": "gpt-4o",
        "label": "GPT-4o (quality OpenAI)",
    },
}


def print_model_list():
    print("Available models:")
    for key, meta in MODEL_CATALOG.items():
        print(f"  {key:12} -> {meta['model']} ({meta['label']})")


def build_llm(model_key: str):
    meta = MODEL_CATALOG[model_key]
    provider = meta["provider"]
    model_name = meta["model"]

    if provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("❌ Error: ANTHROPIC_API_KEY not found")
            print()
            print("Set your API key:")
            print("  export ANTHROPIC_API_KEY='sk-ant-...'")
            print()
            print("Then reload your shell:")
            print("  source ~/.bashrc  (or source ~/.zshrc)")
            return None, None
        return ChatAnthropic(model=model_name, temperature=0), meta

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found")
            print()
            print("Set your API key:")
            print("  export OPENAI_API_KEY='sk-...'")
            print()
            print("Then reload your shell:")
            print("  source ~/.bashrc  (or source ~/.zshrc)")
            return None, None
        return ChatOpenAI(model=model_name, temperature=0), meta

    print(f"❌ Error: Unsupported provider: {provider}")
    return None, None

def format_sources(docs):
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
    
    return "\n".join(sources[:3])  # Show top 3 sources


def format_docs(docs):
    """Format documents for context."""
    return "\n\n".join(doc.page_content for doc in docs)


def main():
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
        choices=sorted(MODEL_CATALOG.keys()),
        default="haiku",
        help=(
            "Model to use. Choices:\n"
            "  haiku | sonnet-4 | gpt-4o-mini | gpt-4o"
        ),
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )

    args = parser.parse_args()

    if args.list_models:
        print_model_list()
        return 0

    if not args.question:
        parser.print_help()
        return 1
    
    # Check if vector DB exists
    if not os.path.exists("data/chroma_db"):
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
            persist_directory="data/chroma_db",
            embedding_function=embeddings
        )
        
        # Create retriever (MMR improves diversity; higher k improves recall)
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8, "fetch_k": 24}
        )
        
        llm, model_meta = build_llm(args.model)
        if llm is None:
            return 1
        
        # Create prompt template
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
        if source_docs:
            print("📚 Sources:")
            print(format_sources(source_docs))
            print()
        
        print(f"ℹ️  Using {model_meta['model']} ({model_meta['label']})")
        print("   Cost: varies by model")
        print()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("If you're seeing API errors, check:")
        print("  - Your ANTHROPIC_API_KEY is set correctly")
        print("  - You have API credits available")
        print()
        return 1

if __name__ == "__main__":
    exit(main())
