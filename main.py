# from flask import Flask, render_template, jsonify


# from data_sources.tba import TheBlueAllianceConnector
# from data_sources.isa import IndianaScoutingAllianceConnector
# from llm_integration.llm_model import OLLAMAConnector
# from llm_integration.team_subjective_rating import TeamRatingGenerator
# from llm_integration.match_outcome_prediction import MatchPredictor
# from llm_integration.alliance_selection import AllianceSelectionAssistant
# from utils.config_manager import ConfigurationManager
# from utils.logger import Logger


# app = Flask(__name__)

# config = ConfigurationManager()
# logger = Logger(__name__)

# # Initialize data sources
# tba_api_key = config.get("TBA_TOKEN")
# tba_connector = TheBlueAllianceConnector(tba_api_key)

# isa_api_key = config.get("ISA_TOKEN")
# isa_connector = IndianaScoutingAllianceConnector(isa_api_key)

# # Initialize LLM model
# llm_model = config.get("OLLAMA_MODEL")
# llm = OLLAMAConnector(llm_model)

# # Initialize prediction and rating services
# team_rater = TeamRatingGenerator(llm)
# match_predictor = MatchPredictor(llm)
# alliance_assistant = AllianceSelectionAssistant(llm)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/team/<int:team_number>")
# def team_info(team_number):
#     event_code = "2025incmp"
#     tba_team_performance_metrics = tba_connector.get_team_performance_metrics(
#         team_number, event_code
#     )
#     tba_raw_event_data = tba_connector.get_event_matches(event_code, team_number)
#     isa_data = isa_connector.get_event_matches(event_code, team_number)
#     isa_notes = isa_connector.get_robot_notes(team_number, event_code)

#     if tba_team_performance_metrics:
#         # logger.info(f"Team {team_number} Metrics: {tba_team_performance_metrics}")

#         # Generate subjective team rating
#         logger.info(f"Generating Team rating...")
#         team_rating = team_rater.rate_team(
#             tba_team_performance_metrics, tba_raw_event_data, isa_data, isa_notes
#         )
#         output = f"Subjective Team Rating: {team_rating}"
#         logger.info(output)
#         return output

#     else:
#         output = (
#             f"Could not retrieve metrics for team {team_number} at event {event_code}"
#         )
#         logger.info(output)
#         return output


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, jsonify


from data_sources.tba import TheBlueAllianceConnector
from data_sources.isa import IndianaScoutingAllianceConnector
from llm_integration.llm_model import OLLAMAConnector
from llm_integration.team_subjective_rating import TeamRatingGenerator
from llm_integration.match_outcome_prediction import MatchPredictor
from llm_integration.alliance_selection import AllianceSelectionAssistant
from utils.config_manager import ConfigurationManager
from utils.logger import Logger


class FrcRatingApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.config = ConfigurationManager()
        self.logger = Logger(__name__)

        # Initialize data sources
        tba_api_key = self.config.get("TBA_TOKEN")
        self.tba_connector = TheBlueAllianceConnector(tba_api_key)

        isa_api_key = self.config.get("ISA_TOKEN")
        self.isa_connector = IndianaScoutingAllianceConnector(isa_api_key)

        # Initialize LLM model
        llm_model = self.config.get("OLLAMA_MODEL")
        self.llm = OLLAMAConnector(llm_model)

        # Initialize prediction and rating services
        self.team_rater = TeamRatingGenerator(self.llm)
        self.match_predictor = MatchPredictor(self.llm)
        self.alliance_assistant = AllianceSelectionAssistant(self.llm)

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/team/<int:team_number>", "team_info", self.team_info)

    def index(self):
        return render_template("index.html")

    def team_info(self, team_number):
        event_code = "2025incmp"
        tba_team_performance_metrics = self.tba_connector.get_team_performance_metrics(
            team_number, event_code
        )
        tba_raw_event_data = self.tba_connector.get_event_matches(
            event_code, team_number
        )
        isa_data = self.isa_connector.get_event_matches(event_code, team_number)
        isa_notes = self.isa_connector.get_robot_notes(team_number, event_code)

        if tba_team_performance_metrics:
            # Generate subjective team rating
            self.logger.info(f"Generating Team rating...")
            team_rating = self.team_rater.rate_team(
                tba_team_performance_metrics,
                tba_raw_event_data,
                isa_data,
                isa_notes,
            )
            output = f"Subjective Team Rating: {team_rating}"
            self.logger.info(output)
            return output

        else:
            output = f"Could not retrieve metrics for team {team_number} at event {event_code}"
            self.logger.info(output)
            return output

    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    frc_rating_app = FrcRatingApp()
    frc_rating_app.run()
