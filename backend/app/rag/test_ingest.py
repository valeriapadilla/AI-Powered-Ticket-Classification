#!/usr/bin/env python3
"""
Simple script to test the ingest module and create the vector database.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "app"))

# Set up environment
os.chdir(current_dir)

# Import and run the ingest
try:
    print("Starting ingest process...")
    
    # Import the ingest module
    from backend.app.rag.ingest_tickets import *
    
    print("✅ Ingest completed successfully!")
    print("📁 Vector database created in ./vector_store")
    print(f"📊 Processed {len(docs)} documents into {len(chunks)} chunks")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed all dependencies:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error during ingest: {e}")
    import traceback
    traceback.print_exc() 