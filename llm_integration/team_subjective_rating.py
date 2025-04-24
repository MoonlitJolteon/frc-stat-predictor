class TeamRatingGenerator:
    """Generates subjective team ratings using LLM predictions"""

    def __init__(self, llm_model):
        self.llm_model = llm_model

    def rate_team(
        self,
        perfomance_metrics: dict,
        raw_event_data: dict,
        isa_data: dict,
        isa_notes: dict,
    ) -> str | None:
        """Rates a team based on available data"""
        return self.llm_model.query_ollama(
            prompt=f"The following First Robotics Competition (FRC), data comes from three different sources covering the exact same team and event, please cross reference them to identify possible problems. ```{perfomance_metrics}```, ```{raw_event_data}```, ```{isa_data}``` Do note that while the data source is the same for all three, the presentation of the data doesn't match up perfectly. I also have the following notes about the team in the data: ```{isa_notes}```Once you've done so, please use the data you have collected and referenced to give a comprehensive subjective rating to the team. This is not an interactive conversation, so please give an output that covers everything that you think the user may want in a single message including examples to support the conclusions. THE DATA ONLY CONTAINS ONE TEAM, OUTPUT MUST BE IN HTML FORMAT."
        )
