import os
import chromadb

# Setup absolute paths to guarantee it works from any terminal directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../chroma_db")
CONFIG_PATH = os.path.join(BASE_DIR, "../sample_data/ci_configs/sample_workflow.yaml")
LOG_PATH = os.path.join(BASE_DIR, "../sample_data/logs/sample_build_logs.txt")

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="ci_context")

def build_store():
    """Reads the local config and log files and stores them as vectors."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = f.read()
        
        collection.add(
            documents=[config_data],
            metadatas=[{"source": "config", "type": "yaml"}],
            ids=["config_1"]
        )
        print("Successfully loaded CI config into ChromaDB.")
    except FileNotFoundError:
        print(f"Error: Could not find {CONFIG_PATH}.")

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            log_data = f.read()

        collection.add(
            documents=[log_data],
            metadatas=[{"source": "log", "type": "txt"}],
            ids=["log_1"]
        )
        print("Successfully loaded build logs into ChromaDB.")
    except FileNotFoundError:
        print(f"Error: Could not find {LOG_PATH}.")
        
    print("Retrieval Store build process complete.")

def retrieve_context(query: str, n_results: int = 2) -> str:
    """Searches ChromaDB for the most relevant configs and logs."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    docs = results.get("documents", [[]])
    if docs and len(docs) > 0:
        retrieved_docs = docs[0]
        return "\n---\n".join(retrieved_docs)
    return ""

if __name__ == "__main__":
    build_store()