class MatchPredictor:
    """Predicts match outcomes using LLM."""

    def __init__(self, llm_model):
        self.llm_model = llm_model

    def predict_outcome(self, blue_alliance_data, red_alliance_data):
        prompt = f"Given blue alliance data: {blue_alliance_data} and red alliance data: {red_alliance_data}, predict the match outcome."
        return self.query_ollama(prompt)
