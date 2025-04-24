import json
import requests


class OLLAMAConnector:
    """
    Abstract class to interact with a local LLM using Ollama for predictions.
    """

    def __init__(
        self, model_name: str, ollama_base_url: str = "http://localhost:11434"
    ):
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url

    def query_ollama(self, prompt: str):
        """
        Helper function to query the Ollama API.
        """
        url = f"{self.ollama_base_url}/api/generate"
        data = {
            "prompt": prompt,
            "model": self.model_name,
            "stream": False,  # Set to False to get the full response at once
        }
        try:
            response = requests.post(url, json=data, stream=False)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error querying Ollama: {e}")
            return None
