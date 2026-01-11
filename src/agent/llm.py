from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    """Initialize and return configured ChatOllama instance."""
    return ChatOllama(
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
        model=os.getenv('OLLAMA_MODEL', 'qwen3:8b'),  # qwen3:8b recommended for better reasoning
        temperature=float(os.getenv('OLLAMA_TEMPERATURE', '0.7'))
    )


def validate_ollama_connection():
    """Check if Ollama is running and accessible."""
    try:
        llm = get_llm()
        # Simple test invocation
        llm.invoke("test")
        return True
    except Exception as e:
        print(f"Error: Ollama not accessible - {e}")
        print("Make sure Ollama is running: ollama serve")
        return False
