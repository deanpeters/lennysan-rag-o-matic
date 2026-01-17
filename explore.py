#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.1
Simple CLI for querying Lenny's podcast corpus with metadata attribution
"""

import sys
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA

def format_sources(source_documents):
    """Format source documents with metadata into readable citations."""
    sources = []
    seen_episodes = set()
    
    for doc in source_documents:
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
        
        # Use Claude Haiku for v0.1 (cheap testing)
        llm = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            temperature=0
        )
        
        # Create QA chain with source documents returned
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": 5}  # Retrieve top 5 relevant chunks
            ),
            return_source_documents=True
        )
        
        # Get answer with sources
        print("🤔 Thinking...")
        result = qa_chain.invoke({"query": query})
        
        print()
        print("💡 Answer:")
        print("-" * 50)
        print(result["result"])
        print("-" * 50)
        print()
        
        # Show sources with metadata
        if result.get("source_documents"):
            print("📚 Sources:")
            print(format_sources(result["source_documents"]))
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
