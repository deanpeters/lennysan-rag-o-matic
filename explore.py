#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.1
Simple CLI for querying Lenny's podcast corpus with metadata attribution
"""

import sys
import os
import warnings

# Suppress LangChain deprecation warnings for v0.1
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*was deprecated.*')

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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
    # Check for query argument
    if len(sys.argv) < 2:
        print("Usage: python explore.py 'Your question here'")
        print()
        print("Examples:")
        print("  python explore.py 'What does Lenny say about pricing?'")
        print("  python explore.py 'How do you find product-market fit?'")
        print("  python explore.py 'What are common mistakes in enterprise sales?'")
        return 1
    
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not found")
        print()
        print("Set your API key:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        print()
        print("Then reload your shell:")
        print("  source ~/.bashrc  (or source ~/.zshrc)")
        return 1
    
    # Check if vector DB exists
    if not os.path.exists("data/chroma_db"):
        print("❌ Error: Vector database not found")
        print()
        print("Run setup first:")
        print("  ./setup.sh")
        return 1
    
    query = " ".join(sys.argv[1:])
    
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
        
        # Create retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        # Use Claude Haiku for v0.1 (cheap testing)
        llm = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            temperature=0
        )
        
        # Create prompt template
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
        if source_docs:
            print("📚 Sources:")
            print(format_sources(source_docs))
            print()
        
        print("ℹ️  Using Claude Haiku (v0.1 proof of life)")
        print("   Cost: ~$0.001-0.005 per query")
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
