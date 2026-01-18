#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.1
Index Lenny's podcast transcripts into ChromaDB with metadata preservation
"""

import os
import sys
import yaml
import logging
import copy
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "paths": {
        "vector_db": "data/chroma_db",
        "logs": "logs",
        "corpora": [
            {"name": "lenny", "path": "episodes"},
        ],
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


def load_transcript_with_metadata(file_path: str) -> tuple[str, Dict[str, Any]]:
    """
    Load a transcript markdown file and separate frontmatter from content.
    
    Returns:
        tuple: (content, metadata_dict)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            transcript_text = parts[2].strip()
            
            # Convert all metadata values to strings or basic types for ChromaDB
            # ChromaDB only accepts: str, int, float, bool, or None
            cleaned_metadata = {}
            for key, value in frontmatter.items():
                if value is None:
                    cleaned_metadata[key] = None
                elif isinstance(value, (str, int, float, bool)):
                    cleaned_metadata[key] = value
                elif isinstance(value, list):
                    # Convert lists to comma-separated strings
                    cleaned_metadata[key] = ', '.join(str(v) for v in value)
                else:
                    # Convert everything else (dates, etc.) to strings
                    cleaned_metadata[key] = str(value)
            
            return transcript_text, cleaned_metadata
    
    # No frontmatter found
    return content, {}


def load_all_transcripts(episodes_dir: str = "episodes") -> List[Document]:
    """
    Load all transcripts from the episodes directory with metadata.
    
    Returns:
        List of LangChain Document objects with metadata attached
    """
    documents = []
    episodes_path = Path(episodes_dir)
    
    if not episodes_path.exists():
        raise FileNotFoundError(f"Episodes directory not found: {episodes_dir}")
    
    transcript_files = list(episodes_path.glob("*/transcript.md"))
    
    print(f"Found {len(transcript_files)} transcript files")
    print()
    
    # Use tqdm for progress bar
    for transcript_file in tqdm(transcript_files, desc="📚 Loading transcripts", unit="episode"):
        try:
            content, metadata = load_transcript_with_metadata(str(transcript_file))
            
            # Add source path to metadata
            metadata['source'] = str(transcript_file)
            
            # Create Document with content and metadata
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
                
        except Exception as e:
            print(f"  ⚠️  Warning: Failed to load {transcript_file}: {e}")
            continue
    
    return documents


def main():
    config = load_config()
    paths = config.get("paths", {})
    logs_dir = paths.get("logs", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_file = f"{logs_dir}/index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    corpora = paths.get("corpora") or []
    episodes_dir = "episodes"
    if isinstance(corpora, list) and corpora:
        first = corpora[0] or {}
        episodes_dir = first.get("path", episodes_dir)

    vector_db_path = paths.get("vector_db", "data/chroma_db")

    print("=" * 60)
    print("LennySan RAG-o-Matic v0.6 - Indexing")
    print("=" * 60)
    print()
    print(f"📋 Logging to: {log_file}")
    print("☕ Grab a coffee - this takes 5-10 minutes")
    print("💡 Your screen might dim but we'll keep working...")
    print()
    
    logger.info("Starting indexing process")
    logger.info(f"Log file: {log_file}")
    
    # Check if episodes directory exists
    if not os.path.exists(episodes_dir):
        print(f"❌ Error: episodes directory not found: {episodes_dir}")
        print("Make sure you're running this from the repo root")
        logger.error("Episodes directory not found")
        return 1
    
    print("📚 Loading transcript documents with metadata...")
    print()
    
    try:
        documents = load_all_transcripts(episodes_dir)
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        logger.error(f"Failed to load documents: {e}", exc_info=True)
        return 1
    
    print()
    print(f"✅ Loaded {len(documents)} episode transcripts")
    logger.info(f"Successfully loaded {len(documents)} transcripts")
    
    # Show sample metadata from first document
    if documents:
        sample_meta = documents[0].metadata
        print()
        print("📋 Sample metadata from first episode:")
        print(f"   Guest: {sample_meta.get('guest', 'N/A')}")
        print(f"   Title: {sample_meta.get('title', 'N/A')}")
        print(f"   Date: {sample_meta.get('publish_date', 'N/A')}")
        print(f"   Keywords: {', '.join(sample_meta.get('keywords', [])[:5])}...")
    
    print()
    print("✂️  Splitting into chunks...")
    print("   (Preserving metadata in each chunk)")
    
    # Split documents into chunks (metadata is preserved in each chunk)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Show progress during splitting
    chunks = []
    for doc in tqdm(documents, desc="✂️  Chunking", unit="episode"):
        doc_chunks = text_splitter.split_documents([doc])
        chunks.extend(doc_chunks)
    
    print()
    print(f"✅ Created {len(chunks)} chunks (metadata preserved in each)")
    print()
    
    print("🧠 Creating embeddings and indexing...")
    print("=" * 60)
    print("⏱️  This is the slow part (~5-10 minutes)")
    print("💤 Your Mac might sleep, but the process continues")
    print("📊 Processing ~{} chunks...".format(len(chunks)))
    print()
    
    # Create embeddings using a free, local model
    print("🔧 Loading embedding model (sentence-transformers)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'batch_size': 32}  # Removed show_progress_bar - causes conflict
    )
    print("✅ Embedding model loaded")
    print()
    
    # Create vector store with progress
    try:
        print("💾 Building vector database...")
        print("   (You'll see a progress bar for embedding generation)")
        print()
        logger.info(f"Creating vector store with {len(chunks)} chunks")
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=vector_db_path
        )
        
        logger.info("Vector store created successfully")
        
        print()
        print("=" * 60)
        print("✅ Indexing complete!")
        print("=" * 60)
        print(f"   📊 Indexed {len(chunks)} chunks from {len(documents)} episodes")
        print(f"   📋 Metadata preserved: guest, title, date, keywords, etc.")
        print(f"   💾 Database stored in: {vector_db_path}")
        print()
        print("🎉 You're ready to explore!")
        print()
        print("Try these queries:")
        print("   python explore.py 'What does Lenny say about pricing?'")
        print("   python explore.py 'How do you find product-market fit?'")
        print("   python explore.py 'What interview questions does Lenny ask?'")
        print()
        print("💡 Tip: Metadata enables rich queries like:")
        print("   - Filter by guest, topic, or date range (future versions)")
        print("   - See which episode an answer came from")
        print("   - Track when advice was given (context matters!)")
        print()
        
        logger.info("Indexing completed successfully")
        return 0
        
    except Exception as e:
        print()
        print(f"❌ Error creating vector store: {e}")
        print()
        print("Common fixes:")
        print("  - Ensure you have enough disk space (~500MB needed)")
        print("  - Check that data/chroma_db/ is writable")
        print("  - Try deleting data/chroma_db/ and running again")
        logger.error(f"Failed to create vector store: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit(main())
