
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
        
        while True:
            print("\n" + "="*40)
            print(" DOCUMENT SELECTION MENU")
            print("="*40)
            
            # List documents compact
            for i, doc in enumerate(docs):
                # Try to get a title or summary for better listing
                meta = doc.get('metadata', {})
                title = meta.get('title', 'No Title')
                print(f"{i+1}. [{doc['type'].upper()}] {title} (ID: {doc['id']})")
                
            print("\nEnter document number to inspect (or 'q' to quit)")
            choice = input("Selection > ").strip()
            
            if choice.lower() == 'q':
                print("Bye!")
                break
                
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(docs):
                    doc = docs[idx]
                    vec = embeddings[idx]
                    
                    print(f"\n[DEBUG] --- Inspecting Document #{idx+1} ---")
                    print(f"ID: {doc['id']}")
                    print(f"Type: {doc['type']}")
                    print(f"Full Content:\n---\n{doc['content']}\n---")
                    
                    print(f"\n[INFO] Embedding Vector Preview (Size: {len(vec)}):")
                    print(f"       {vec[:10]}")
                    print(f"       ... {len(vec)-10} more dimensions ...")
                    
                    input("\nPress Enter to continue...")
                else:
                    print("[ERROR] Invalid selection number.")
            except ValueError:
                print("[ERROR] Please enter a valid number.")

    except Exception as e:
        print(f"[ERROR] Error reading cache: {e}")

if __name__ == "__main__":
    try:
        inspect_cache()
    except KeyboardInterrupt:
        print("\nExiting...")
