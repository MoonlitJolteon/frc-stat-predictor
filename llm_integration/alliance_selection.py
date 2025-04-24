import json


class AllianceSelectionAssistant:
    """Assists in alliance selection using LLM and team data."""

    def __init__(self, llm_model):
        self.llm_model = llm_model

    def generate_pick_list(self, teams_data, strategy):
        teams_data_str = json.dumps(
            teams_data
        )  # Serialize the list of dictionaries to a string
        prompt = f"Given the following teams data: {teams_data_str} and pick strategy: {pick_strategy}, generate an alliance pick list."
        return self.query_ollama(prompt)
