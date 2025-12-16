
import pickle
import os
import numpy as np
import sys

# Add backend directory to path to handle potential import issues
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def inspect_cache():
    cache_path = os.path.join("backend", "rag_cache.pkl")
    
    if not os.path.exists(cache_path):
        print(f"[ERROR] Cache file not found at: {cache_path}")
        print("Please run the backend first to generate the cache.")
        return

    print(f"[INFO] Loading cache from: {cache_path}")
    
    try:
        with open(cache_path, 'rb') as f:
            data = pickle.load(f)
            
        docs = data['documents']
        embeddings = data['embeddings']
        
        print(f"\n[OK] Cache Loaded Successfully")
        print(f"[INFO] Total Documents: {len(docs)}")
        print(f"[INFO] Embedding Matrix Shape: {embeddings.shape}")
        print(f"       (This means {embeddings.shape[0]} documents, each having {embeddings.shape[1]} dimensions)")
        
        if len(docs) > 0:
            print("\n[DEBUG] --- Inspecting First Document ---")
            print(f"ID: {docs[0]['id']}")
            print(f"Type: {docs[0]['type']}")
            print(f"Content Preview: {docs[0]['content'][:100]}...")
            
            vec = embeddings[0]
            print(f"\n[INFO] Embedding Vector (First 10 values):")
            print(f"       {vec[:10]}")
            print(f"       ... and {len(vec)-10} more numbers ...")
            
            print(f"\n[HELP] WHAT IS THIS?")
            print("       These numbers are the 'semantic meaning' of text.")
            print("       Similar texts will have similar lists of numbers.")

    except Exception as e:
        print(f"[ERROR] Error reading cache: {e}")

if __name__ == "__main__":
    inspect_cache()
